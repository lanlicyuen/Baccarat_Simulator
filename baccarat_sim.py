#!/usr/bin/env python3
"""
百家乐（Punto Banco）模拟器 / CLI

运行示例（建议加 --silent 以提速）：
    python baccarat_sim.py --bankroll 100000 --bet 100 --hands 50000 --decks 8 --seed 42 --csv ./out/report.csv --silent

本脚本作为命令行入口，核心逻辑在 baccarat_core.py 中实现。
"""
import os
import argparse
import sys
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
import math
from baccarat_core import (
    RunParams,
    simulate_hands,
    save_csv,
    save_json,
)



def print_summary(stats: Dict[str, Any], csv_path: str, json_path: str) -> None:
    def pct(x: float) -> str:
        return f"{x*100:.2f}%"

    print("\n===== Simulation Summary =====")
    print(f"Strategy: {stats['strategy']}; Bet: {stats['bet_size']}; Decks: {stats['decks']}; Penetration: {stats['penetration']}")
    print(f"Hands: {stats['hands']}; Bet hands: {stats['bet_hands']}; Observe: {stats['observe_hands']}; Pushes: {stats['push_hands']}")
    print(
        f"Player/Banker/Tie: {stats['player_wins']}/{stats['banker_wins']}/{stats['ties']} "
        f"({pct(stats['outcome_distribution']['player']['pct'])}/"
        f"{pct(stats['outcome_distribution']['banker']['pct'])}/"
        f"{pct(stats['outcome_distribution']['tie']['pct'])})"
    )
    hr = stats["strategy_hit_rate"]
    hr_s = f"{hr*100:.2f}%" if hr is not None else "N/A"
    print(f"Hit rate: {hr_s}; Commission: {stats['commission_total']:.2f}")
    print(
        f"Bankroll: start {stats['initial_bankroll']:.2f} -> end {stats['final_bankroll']:.2f}; "
        f"Profit: {stats['total_profit']:+.2f}; ROI: {stats['roi']*100:.3f}%"
    )
    print(f"Avg cards/hand: {stats['avg_cards_per_hand']:.3f}; Cards dealt total: {stats['cards_dealt_total']}")
    print(f"Shoe reshuffles: {stats['shoe_reshuffles']}")
    print(f"CSV: {csv_path}")
    print(f"JSON: {json_path}")


def _ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)


# ----------------------
# CLI and validation
# ----------------------

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Baccarat (Punto Banco) simulator")
    parser.add_argument("--bankroll", type=float, required=False, help="初始本金（必填）")
    parser.add_argument("--bet", type=float, required=False, help="每注金额（必填）")
    parser.add_argument("--hands", type=int, required=False, help="总局数（100–100000）")
    parser.add_argument("--decks", type=int, default=8, choices=[6, 8], help="副牌数（6或8，默认8）")
    parser.add_argument("--penetration", type=int, default=52, help="渗透阈值（默认52张）")
    parser.add_argument(
        "--strategy",
        type=str,
        default="flip-opposite-wait",
        choices=[
            "flip-opposite-wait",
            "always-banker",
            "always-player",
            "alternate",
            "random",
        ],
        help="下注策略",
    )
    parser.add_argument("--seed", type=int, default=None, help="随机种子（可选）")
    parser.add_argument("--csv", dest="csv_path", type=str, default=None, help="CSV 报表输出路径")
    parser.add_argument("--json", dest="json_path", type=str, default=None, help="JSON 汇总输出路径")
    parser.add_argument("--silent", action="store_true", help="仅保存报表与汇总，不在控制台打印每局")
    parser.add_argument("--run-tests", action="store_true", help="运行内置单元测试并退出")

    args = parser.parse_args(argv)

    if args.run_tests:
        return args

    # Required checks
    missing = []
    if args.bankroll is None:
        missing.append("--bankroll")
    if args.bet is None:
        missing.append("--bet")
    if args.hands is None:
        missing.append("--hands")
    if missing:
        parser.error(f"缺少参数：{' '.join(missing)}")

    if not (100 <= int(args.hands) <= 100000):
        parser.error("--hands 必须在 100 到 100000 之间")
    if args.bet <= 0 or args.bankroll <= 0:
        parser.error("--bet 和 --bankroll 必须为正数")
    if args.penetration < 1:
        parser.error("--penetration 必须为正整数")
    return args


# ----------------------
# Unit tests (embedded) import from core
# ----------------------

import unittest
from baccarat_core import card_point, hand_total as hand_total_mod10, player_draws as should_player_draw, banker_draws as banker_should_draw, RunParams


class TestPointsAndTotals(unittest.TestCase):
    def test_card_points(self):
        self.assertEqual(card_point("A"), 1)
        self.assertEqual(card_point("2"), 2)
        self.assertEqual(card_point("9"), 9)
        self.assertEqual(card_point("10"), 0)
        self.assertEqual(card_point("J"), 0)
        self.assertEqual(card_point("Q"), 0)
        self.assertEqual(card_point("K"), 0)

    def test_total_mod10(self):
        self.assertEqual(hand_total_mod10(["A", "9"]), 0)
        self.assertEqual(hand_total_mod10(["5", "7"]), 2)


class TestPlayerRules(unittest.TestCase):
    def test_player_draw_rules(self):
        for t in range(0, 6):
            self.assertTrue(should_player_draw(t))
        for t in (6, 7):
            self.assertFalse(should_player_draw(t))


class TestBankerRules(unittest.TestCase):
    def test_banker_when_player_stands(self):
        for b in range(0, 6):
            self.assertTrue(banker_should_draw(b, None))
        for b in (6, 7):
            self.assertFalse(banker_should_draw(b, None))

    def test_banker_total_3(self):
        for pv in range(0, 10):
            expected = (pv != 8)
            self.assertEqual(banker_should_draw(3, pv), expected)

    def test_banker_total_4(self):
        for pv in range(0, 10):
            expected = 2 <= pv <= 7
            self.assertEqual(banker_should_draw(4, pv), expected)

    def test_banker_total_5(self):
        for pv in range(0, 10):
            expected = 4 <= pv <= 7
            self.assertEqual(banker_should_draw(5, pv), expected)

    def test_banker_total_6(self):
        for pv in range(0, 10):
            expected = pv in (6, 7)
            self.assertEqual(banker_should_draw(6, pv), expected)

    def test_simulate_generator_minimal(self):
        from baccarat_core import simulate_hands
        params = RunParams(bankroll=1000, bet=10, hands=5, decks=8, penetration=52, strategy="always-player", seed=1)
        gen = simulate_hands(params, yield_per_hand=True)
        events = list(gen)
        self.assertEqual(len(events), 5)


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)
    if args.run_tests:
        suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        sys.exit(0 if result.wasSuccessful() else 1)

    now = datetime.now()
    ts = now.strftime("%Y%m%d_%H%M%S")
    csv_path = args.csv_path or os.path.join(os.getcwd(), "out", f"baccarat_report_{ts}.csv")
    json_path = args.json_path or os.path.join(os.getcwd(), "out", f"baccarat_summary_{ts}.json")

    params = RunParams(
        bankroll=float(args.bankroll),
        bet=float(args.bet),
        hands=int(args.hands),
        decks=int(args.decks),
        penetration=int(args.penetration),
        strategy=str(args.strategy),
        seed=args.seed,
        csv_path=csv_path,
        json_path=json_path,
    )

    # run and collect all events quickly
    events = []
    for ev in simulate_hands(params, yield_per_hand=True):
        events.append(ev)
        if not args.silent:
            print(
                f"#{ev.hand_no} {ev.timestamp} bet={ev.bet_side or '-'} amt={ev.bet_amount:.2f} "
                f"P={ev.player_cards}({ev.player_total}) B={ev.banker_cards}({ev.banker_total}) -> {ev.outcome} "
                f"win={ev.win_amount:+.2f} bank={ev.bankroll_after:.2f} left={ev.shoe_cards_left} comm={ev.commission_paid:.2f}"
            )

    # derive summary similar to previous stats using last event and counters from JSON save in core
    # we need to recompute summary via yield_per_hand=False path for consistency
    _, summary = simulate_hands(params, yield_per_hand=False)

    save_csv(events, csv_path, params)
    save_json(summary, json_path)

    # Print concise summary
    stats = {
        **summary.params,
        "strategy": summary.params["strategy"],
        "bet_size": summary.params["bet_size"],
        "decks": summary.params["decks"],
        "penetration": summary.params["penetration"],
        "hands": summary.params["hands"],
        "initial_bankroll": summary.initial_bankroll,
        "final_bankroll": summary.final_bankroll,
        "total_profit": summary.total_profit,
        "total_wagered": summary.total_wagered,
        "bet_hands": summary.bet_hands,
        "observe_hands": summary.observe_hands,
        "push_hands": summary.push_hands,
        "wins": summary.wins,
        "losses": summary.losses,
        "commission_total": summary.commission_total,
        "player_wins": summary.player_wins,
        "banker_wins": summary.banker_wins,
        "ties": summary.ties,
        "avg_cards_per_hand": summary.avg_cards_per_hand,
        "cards_dealt_total": summary.cards_dealt_total,
        "shoe_reshuffles": summary.shoe_reshuffles,
        "strategy_hit_rate": summary.strategy_hit_rate,
        "outcome_distribution": summary.outcome_distribution,
    }
    print_summary(stats, csv_path, json_path)


if __name__ == "__main__":
    main()
