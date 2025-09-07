from __future__ import annotations

import csv
import json
import os
import random
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple, Union


# ----------------------------
# Card utilities
# ----------------------------

RANKS: List[str] = [
    "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"
]


def card_point(rank: str) -> int:
    if rank == "A":
        return 1
    if rank in ("10", "J", "Q", "K"):
        return 0
    try:
        return int(rank)
    except ValueError:
        raise ValueError(f"Invalid rank: {rank}")


def hand_total(cards: List[str]) -> int:
    return sum(card_point(r) for r in cards) % 10


def player_draws(player_total: int) -> bool:
    return 0 <= player_total <= 5


def banker_draws(banker_total: int, player_third_value: Optional[int]) -> bool:
    if player_third_value is None:
        return banker_total <= 5
    if 0 <= banker_total <= 2:
        return True
    if banker_total == 3:
        return player_third_value != 8
    if banker_total == 4:
        return 2 <= player_third_value <= 7
    if banker_total == 5:
        return 4 <= player_third_value <= 7
    if banker_total == 6:
        return player_third_value in (6, 7)
    if banker_total == 7:
        return False
    return False


@dataclass
class Card:
    rank: str

    @property
    def point(self) -> int:
        return card_point(self.rank)


@dataclass
class Hand:
    cards: List[Card]

    def total(self) -> int:
        return sum(c.point for c in self.cards) % 10


@dataclass
class Shoe:
    decks: int
    rng: random.Random
    cards: List[Card] = None
    shuffle_count: int = 0

    def __post_init__(self):
        self.reset()

    def reset(self) -> None:
        deck: List[Card] = []
        for _ in range(self.decks):
            for r in RANKS:
                for _s in range(4):
                    deck.append(Card(rank=r))
        self.cards = deck
        self.rng.shuffle(self.cards)
        self.shuffle_count += 1

    def draw(self) -> Card:
        try:
            return self.cards.pop()
        except IndexError:
            raise RuntimeError("Shoe is empty; cannot draw.")

    @property
    def cards_left(self) -> int:
        return len(self.cards)


class Strategy:
    def decide(self) -> Optional[str]:
        raise NotImplementedError

    def observe_outcome(self, outcome: str) -> None:
        pass


def _opposite(side: str) -> str:
    return "banker" if side == "player" else "player"


class FlipOppositeWaitStrategy(Strategy):
    def __init__(self):
        self.last_winner: Optional[str] = None
        self.streak: int = 0
        self.waiting_due_to_streak: bool = False
        self.just_switched: bool = False

    def decide(self) -> Optional[str]:
        if self.last_winner is None:
            return None
        if self.just_switched:
            self.just_switched = False
            return _opposite(self.last_winner)
        if self.waiting_due_to_streak:
            return None
        if self.streak <= 1:
            return _opposite(self.last_winner)
        return None

    def observe_outcome(self, outcome: str) -> None:
        if outcome == "tie":
            return
        if self.last_winner is None:
            self.last_winner = outcome
            self.streak = 1
            self.waiting_due_to_streak = False
            self.just_switched = False
            return
        if outcome == self.last_winner:
            self.streak += 1
            if self.streak >= 2:
                self.waiting_due_to_streak = True
        else:
            self.last_winner = outcome
            self.streak = 1
            if self.waiting_due_to_streak:
                self.just_switched = True
            self.waiting_due_to_streak = False


class AlwaysBankerStrategy(Strategy):
    def decide(self) -> Optional[str]:
        return "banker"


class AlwaysPlayerStrategy(Strategy):
    def decide(self) -> Optional[str]:
        return "player"


class AlternateStrategy(Strategy):
    def __init__(self):
        self.next_side = "player"

    def decide(self) -> Optional[str]:
        side = self.next_side
        self.next_side = "banker" if self.next_side == "player" else "player"
        return side


class RandomStrategy(Strategy):
    def __init__(self, rng: random.Random):
        self.rng = rng

    def decide(self) -> Optional[str]:
        return self.rng.choice(["player", "banker"])


def build_strategy(name: str, rng: random.Random) -> Strategy:
    name = name.lower()
    if name == "flip-opposite-wait":
        return FlipOppositeWaitStrategy()
    if name == "always-banker":
        return AlwaysBankerStrategy()
    if name == "always-player":
        return AlwaysPlayerStrategy()
    if name == "alternate":
        return AlternateStrategy()
    if name == "random":
        return RandomStrategy(rng)
    raise ValueError(f"Unknown strategy: {name}")


class BaccaratGame:
    def __init__(self, shoe: Shoe):
        self.shoe = shoe

    def deal_one_hand(self) -> Dict[str, Any]:
        player_hand = Hand(cards=[self.shoe.draw(), self.shoe.draw()])
        banker_hand = Hand(cards=[self.shoe.draw(), self.shoe.draw()])

        player_total_ = player_hand.total()
        banker_total_ = banker_hand.total()

        # Naturals
        if player_total_ in (8, 9) or banker_total_ in (8, 9):
            outcome = _compare_totals(player_total_, banker_total_)
            return {
                "player_cards": [c.rank for c in player_hand.cards],
                "banker_cards": [c.rank for c in banker_hand.cards],
                "player_total": player_total_,
                "banker_total": banker_total_,
                "outcome": outcome,
                "cards_dealt": 4,
            }

        player_third_value: Optional[int] = None
        if player_draws(player_total_):
            pc3 = self.shoe.draw()
            player_hand.cards.append(pc3)
            player_third_value = pc3.point
            player_total_ = player_hand.total()

        if banker_total_ not in (8, 9):
            if banker_draws(banker_total_, player_third_value):
                bc3 = self.shoe.draw()
                banker_hand.cards.append(bc3)
                banker_total_ = banker_hand.total()

        outcome = _compare_totals(player_total_, banker_total_)
        return {
            "player_cards": [c.rank for c in player_hand.cards],
            "banker_cards": [c.rank for c in banker_hand.cards],
            "player_total": player_total_,
            "banker_total": banker_total_,
            "outcome": outcome,
            "cards_dealt": len(player_hand.cards) + len(banker_hand.cards),
        }


def _compare_totals(pt: int, bt: int) -> str:
    if pt > bt:
        return "player"
    if bt > pt:
        return "banker"
    return "tie"


@dataclass
class RunParams:
    bankroll: float
    bet: float
    hands: int
    decks: int = 8
    penetration: int = 52
    strategy: str = "flip-opposite-wait"
    seed: Optional[int] = None
    csv_path: Optional[str] = None
    json_path: Optional[str] = None
    # 连输：固定百分比增加（相对基础注）
    loss_progression_pct: float = 0.0
    # 连输：固定百分比减少（相对基础注）
    loss_progression_dec_pct: float = 0.0
    # 开始加注的连输阈值：达到该连输次数后才开始按百分比放大（默认1表示第一手输后就放大）
    loss_progression_start: int = 1
    # 连输结束（赢一局）后的注码调整：'reset' 回到基础注；'persist' 保持加大后的注码
    loss_progression_win_mode: str = "reset"
    # 连赢：支持加注或减注（相对基础注）
    win_progression_inc_pct: float = 0.0  # 连赢时增加百分比
    win_progression_dec_pct: float = 0.0  # 连赢时减少百分比
    win_progression_start: int = 1       # 从第几次连赢开始生效
    # 连赢被打断（输一局）后的注码调整：'reset' 回到基础注；'persist' 保持调整后的注码
    win_progression_loss_mode: str = "reset"


@dataclass
class HandEvent:
    timestamp: str
    hand_no: int
    bet_side: Optional[str]
    bet_amount: float
    player_cards: List[str]
    banker_cards: List[str]
    player_total: int
    banker_total: int
    outcome: str
    win_amount: float
    bankroll_after: float
    shoe_cards_left: int
    commission_paid: float
    cumulative_win: float


@dataclass
class RunSummary:
    params: Dict[str, Any]
    initial_bankroll: float
    final_bankroll: float
    total_profit: float
    total_wagered: float
    roi: float
    bet_hands: int
    observe_hands: int
    push_hands: int
    wins: int
    losses: int
    commission_total: float
    player_wins: int
    banker_wins: int
    ties: int
    avg_cards_per_hand: float
    cards_dealt_total: int
    shoe_reshuffles: int
    strategy_hit_rate: Optional[float]
    outcome_distribution: Dict[str, Dict[str, float]]


def _simulate_hands_iter(params: RunParams) -> Iterator[HandEvent]:
    rng = random.Random(params.seed)
    shoe = Shoe(decks=params.decks, rng=rng)
    strat = build_strategy(params.strategy, rng)

    now = datetime.now()
    hand_time = now
    bankroll = float(params.bankroll)

    bet_hands = 0
    observe_hands = 0
    push_hands = 0
    wins = 0
    losses = 0
    commission_total = 0.0
    player_wins = 0
    banker_wins = 0
    ties = 0
    cards_dealt_total = 0
    shoe_reshuffles = 1
    total_wagered = 0.0

    game = BaccaratGame(shoe)

    cumulative_win = 0.0
    loss_streak = 0  # 连输次数（只统计已下注且输的手；和局不变，赢则清零）
    win_streak = 0   # 连赢次数（只统计已下注且赢的手；和局不变，输则清零）
    last_bet_outcome: Optional[str] = None  # 'win' | 'loss' | None（含首次或只观望情况）
    # 持续倍率分别独立管理
    loss_persist_multiplier = 1.0
    win_persist_multiplier = 1.0

    for hand_no in range(1, params.hands + 1):
        # reshuffle if penetration reached or insufficient cards for next hand
        if shoe.cards_left < 6 or shoe.cards_left <= params.penetration:
            shoe.reset()
            shoe_reshuffles += 1

        bet_side = strat.decide()
        # progressive bet sizing based on last outcome (loss or win)
        base_bet = float(params.bet)
        if bet_side:
            multiplier = 1.0
            # 1) 连输加注
            if last_bet_outcome == "loss":
                loss_start = max(1, int(getattr(params, "loss_progression_start", 1) or 1))
                loss_active = loss_streak >= loss_start
                loss_inc = max(0.0, float(getattr(params, "loss_progression_pct", 0.0)))
                loss_dec = max(0.0, float(getattr(params, "loss_progression_dec_pct", 0.0)))
                if loss_active and loss_inc > 0:
                    loss_effective = 1.0 + (loss_inc/100.0)
                elif loss_active and loss_dec > 0:
                    loss_effective = max(0.0, 1.0 - (loss_dec/100.0))
                else:
                    loss_effective = 1.0
                if (params.loss_progression_win_mode or "reset") in ("persist", "ignore"):
                    # 按方向持久化：>1 取最大，<1 取最小
                    if loss_effective >= 1.0:
                        multiplier = max(loss_persist_multiplier, loss_effective)
                    else:
                        multiplier = min(loss_persist_multiplier, loss_effective)
                else:
                    multiplier = loss_effective
            # 2) 连赢加/减注
            elif last_bet_outcome == "win":
                win_start = max(1, int(getattr(params, "win_progression_start", 1) or 1))
                win_active = win_streak >= win_start
                inc_pct = max(0.0, float(getattr(params, "win_progression_inc_pct", 0.0)))
                dec_pct = max(0.0, float(getattr(params, "win_progression_dec_pct", 0.0)))
                # 若 inc 与 dec 均设置，优先使用 inc（加注优先）
                if win_active and inc_pct > 0:
                    win_effective = 1.0 + (inc_pct/100.0)
                elif win_active and dec_pct > 0:
                    win_effective = max(0.0, 1.0 - (dec_pct/100.0))
                else:
                    win_effective = 1.0
                if (params.win_progression_loss_mode or "reset") in ("persist", "ignore"):
                    # 按方向持久化：>1 取最大，<1 取最小
                    if win_effective >= 1.0:
                        multiplier = max(win_persist_multiplier, win_effective)
                    else:
                        multiplier = min(win_persist_multiplier, win_effective)
                else:
                    multiplier = win_effective
            # 无最近结果或仅观望后第一注 => 使用基础注
            bet_amount = round(max(0.0, base_bet * multiplier), 2)
        else:
            bet_amount = 0.0
        # bankroll check for betting; if insufficient, treat as observe
        if bet_side and bankroll < bet_amount:
            bet_side = None
            bet_amount = 0.0

        if bet_side:
            bet_hands += 1
            total_wagered += bet_amount
        else:
            observe_hands += 1

        result = game.deal_one_hand()
        outcome = result["outcome"]
        cards_dealt_total += result["cards_dealt"]

        if outcome == "player":
            player_wins += 1
        elif outcome == "banker":
            banker_wins += 1
        else:
            ties += 1

        win_amount = 0.0
        commission_paid = 0.0
        if bet_side:
            if outcome == "tie":
                push_hands += 1
                # 和局不改变任何连赢/连输
            elif bet_side == outcome:
                if outcome == "player":
                    win_amount = bet_amount
                else:
                    commission_paid = bet_amount * 0.05
                    win_amount = bet_amount - commission_paid
                    commission_total += commission_paid
                wins += 1
                # 更新连赢/连输状态
                loss_streak = 0
                win_streak += 1
                last_bet_outcome = "win"
                # 连输持久倍率在赢后根据模式复位
                if (params.loss_progression_win_mode or "reset") == "reset":
                    loss_persist_multiplier = 1.0
                # 更新连赢持久倍率（当选择 persist 时）
                win_start = max(1, int(getattr(params, "win_progression_start", 1) or 1))
                inc_pct = max(0.0, float(getattr(params, "win_progression_inc_pct", 0.0)))
                dec_pct = max(0.0, float(getattr(params, "win_progression_dec_pct", 0.0)))
                win_active = win_streak >= win_start
                if win_active and inc_pct > 0:
                    win_effective = 1.0 + (inc_pct/100.0)
                elif win_active and dec_pct > 0:
                    win_effective = max(0.0, 1.0 - (dec_pct/100.0))
                else:
                    win_effective = 1.0
                if (params.win_progression_loss_mode or "reset") in ("persist", "ignore"):
                    if win_effective >= 1.0:
                        win_persist_multiplier = max(win_persist_multiplier, win_effective)
                    else:
                        win_persist_multiplier = min(win_persist_multiplier, win_effective)
            else:
                win_amount = -bet_amount
                losses += 1
                # 更新连赢/连输状态
                win_streak = 0
                loss_streak += 1
                last_bet_outcome = "loss"
                # 连赢持久倍率在输后根据模式复位
                if (params.win_progression_loss_mode or "reset") == "reset":
                    win_persist_multiplier = 1.0
                # 更新连输持久倍率（当选择 persist 时）
                loss_inc = max(0.0, float(getattr(params, "loss_progression_pct", 0.0)))
                loss_dec = max(0.0, float(getattr(params, "loss_progression_dec_pct", 0.0)))
                loss_start = max(1, int(getattr(params, "loss_progression_start", 1) or 1))
                loss_active = loss_streak >= loss_start
                if loss_active and loss_inc > 0:
                    loss_effective = 1.0 + (loss_inc/100.0)
                elif loss_active and loss_dec > 0:
                    loss_effective = max(0.0, 1.0 - (loss_dec/100.0))
                else:
                    loss_effective = 1.0
                if (params.loss_progression_win_mode or "reset") in ("persist", "ignore"):
                    if loss_effective >= 1.0:
                        loss_persist_multiplier = max(loss_persist_multiplier, loss_effective)
                    else:
                        loss_persist_multiplier = min(loss_persist_multiplier, loss_effective)

        bankroll += win_amount
        cumulative_win += win_amount

        event = HandEvent(
            timestamp=hand_time.isoformat(),
            hand_no=hand_no,
            bet_side=bet_side,
            bet_amount=round(bet_amount, 2),
            player_cards=result["player_cards"],
            banker_cards=result["banker_cards"],
            player_total=result["player_total"],
            banker_total=result["banker_total"],
            outcome=outcome,
            win_amount=round(win_amount, 2),
            bankroll_after=round(bankroll, 2),
            shoe_cards_left=shoe.cards_left,
            commission_paid=round(commission_paid, 2),
            cumulative_win=round(cumulative_win, 2),
        )
        # Always yield in iterator mode
        yield event

        strat.observe_outcome(outcome)
        hand_time += timedelta(seconds=1)

    avg_cards = (cards_dealt_total / params.hands) if params.hands > 0 else 0.0
    roi = ( (bankroll - float(params.bankroll)) / total_wagered ) if total_wagered > 0 else 0.0
    attempts = bet_hands - push_hands
    hit_rate = (wins / attempts) if attempts > 0 else None

    summary = RunSummary(
        params={
            "hands": params.hands,
            "decks": params.decks,
            "penetration": params.penetration,
            "seed": params.seed,
            "strategy": params.strategy,
            "bet_size": params.bet,
            "loss_progression_pct": params.loss_progression_pct,
            "loss_progression_dec_pct": getattr(params, "loss_progression_dec_pct", 0.0),
            "loss_progression_start": params.loss_progression_start,
            "loss_progression_win_mode": params.loss_progression_win_mode,
            "win_progression_inc_pct": getattr(params, "win_progression_inc_pct", 0.0),
            "win_progression_dec_pct": getattr(params, "win_progression_dec_pct", 0.0),
            "win_progression_start": getattr(params, "win_progression_start", 1),
            "win_progression_loss_mode": getattr(params, "win_progression_loss_mode", "reset"),
            "csv_path": params.csv_path,
            "json_path": params.json_path,
        },
        initial_bankroll=float(params.bankroll),
        final_bankroll=round(bankroll, 2),
        total_profit=round(bankroll - float(params.bankroll), 2),
        total_wagered=round(total_wagered, 2),
        roi=roi,
        bet_hands=bet_hands,
        observe_hands=observe_hands,
        push_hands=push_hands,
        wins=wins,
        losses=losses,
        commission_total=round(commission_total, 2),
        player_wins=player_wins,
        banker_wins=banker_wins,
        ties=ties,
        avg_cards_per_hand=avg_cards,
        cards_dealt_total=cards_dealt_total,
        shoe_reshuffles=shoe_reshuffles,
        strategy_hit_rate=hit_rate,
        outcome_distribution={
            "player": {"count": player_wins, "pct": player_wins / params.hands},
            "banker": {"count": banker_wins, "pct": banker_wins / params.hands},
            "tie": {"count": ties, "pct": ties / params.hands},
        },
    )
    # In generator semantics, return the summary as StopIteration.value
    return summary


def simulate_hands(params: RunParams, yield_per_hand: bool = True):
    """Simulation API.

    - When yield_per_hand=True: returns an iterator of HandEvent (streaming).
    - When yield_per_hand=False: runs the whole simulation and returns (events, summary).
    """
    gen = _simulate_hands_iter(params)
    if yield_per_hand:
        # return the iterator directly for streaming consumption
        return gen
    # batch mode: collect all events and capture the final summary from StopIteration.value
    events: List[HandEvent] = []
    try:
        while True:
            ev = next(gen)
            events.append(ev)
    except StopIteration as stop:
        summary = stop.value
    return events, summary


def save_csv(events: List[HandEvent], path: str, params: Optional[Union[RunParams, Dict[str, Any]]] = None) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)
    fields = [
        "timestamp",
        "hand_no",
        "bet_side",
        "bet_amount",
        "player_cards",
        "banker_cards",
        "player_total",
        "banker_total",
        "outcome",
        "win_amount",
        "bankroll_after",
        "shoe_cards_left",
        "commission_paid",
        "cumulative_win",
    ]
    # Optional run parameters to include as constant columns per row
    param_payload: Dict[str, Any] = {}
    if params is not None:
        if isinstance(params, RunParams):
            param_payload = {
                "strategy": params.strategy,
                "bet_size": params.bet,
                "decks": params.decks,
                "penetration": params.penetration,
                "seed": params.seed,
                "loss_progression_pct": getattr(params, "loss_progression_pct", 0.0),
                "loss_progression_dec_pct": getattr(params, "loss_progression_dec_pct", 0.0),
                "loss_progression_start": getattr(params, "loss_progression_start", 1),
                "loss_progression_win_mode": getattr(params, "loss_progression_win_mode", "reset"),
                "win_progression_inc_pct": getattr(params, "win_progression_inc_pct", 0.0),
                "win_progression_dec_pct": getattr(params, "win_progression_dec_pct", 0.0),
                "win_progression_start": getattr(params, "win_progression_start", 1),
                "win_progression_loss_mode": getattr(params, "win_progression_loss_mode", "reset"),
            }
        else:
            param_payload = {k: params.get(k) for k in [
                "strategy","bet_size","decks","penetration","seed",
                "loss_progression_pct","loss_progression_dec_pct","loss_progression_start","loss_progression_win_mode",
                "win_progression_inc_pct","win_progression_dec_pct","win_progression_start","win_progression_loss_mode"
            ] if k in params}
        # extend fields preserving order
        fields.extend(list(param_payload.keys()))
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for e in events:
            row = asdict(e)
            # player_cards/banker_cards should be JSON strings in CSV
            row["player_cards"] = json.dumps(row["player_cards"], ensure_ascii=False)
            row["banker_cards"] = json.dumps(row["banker_cards"], ensure_ascii=False)
            # add params as constant columns per row if provided
            row.update(param_payload)
            writer.writerow(row)


def save_json(summary: Union[RunSummary, Dict[str, Any]], path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)
    payload = asdict(summary) if isinstance(summary, RunSummary) else summary
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
