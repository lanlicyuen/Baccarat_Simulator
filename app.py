from __future__ import annotations

import json
import time
import os
from dataclasses import asdict
from typing import List, Optional

import pandas as pd
import streamlit as st
import altair as alt

from baccarat_core import RunParams, simulate_hands, save_csv, save_json


def ensure_authenticated():
    """检查密码验证，如果未认证则显示登录页面"""
    # 检查URL参数是否有logout
    query_params = st.query_params
    if "logout" in query_params:
        st.session_state.authenticated = False
        # 清除URL参数
        st.query_params.clear()
        st.rerun()
    
    # 检查是否已认证
    if st.session_state.get("authenticated", False):
        return True
    
    # 获取密码（仅从环境变量，无默认值）
    correct_password = os.environ.get("ACCESS_PASSWORD")
    if not correct_password:
        st.error("❌ ACCESS_PASSWORD environment variable not set. Please configure password in docker-compose.yml or .env file.")
        st.stop()
    
    # 设置页面配置（在显示登录界面之前）
    st.set_page_config(
        page_title="Baccarat Simulator - Login", 
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # 注入CSS样式 - 酷炫的霓虹玻璃效果
    st.markdown("""
    <style>
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 背景动画 */
    .stApp {
        background: linear-gradient(-45deg, #1a1a2e, #16213e, #0f3460, #533483);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* 粒子效果背景 */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #eee, transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.3), transparent),
            radial-gradient(1px 1px at 90px 40px, #fff, transparent),
            radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.3), transparent),
            radial-gradient(2px 2px at 160px 30px, #fff, transparent);
        background-repeat: repeat;
        background-size: 200px 100px;
        animation: sparkle 20s linear infinite;
        pointer-events: none;
        z-index: 1;
    }
    
    @keyframes sparkle {
        0% { transform: translateY(0px); }
        100% { transform: translateY(-100px); }
    }
    
    /* 主容器居中 */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
        max-width: 500px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        min-height: 90vh;
    }
    
    /* Logo容器 - 独立于主容器之上 */
    .logo-container {
        text-align: center;
        margin-bottom: 40px;
        z-index: 15;
        position: relative;
    }
    
    /* 标题样式 - 移到logo容器 */
    .auth-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: bold;
        background: linear-gradient(45deg, #00f0ff, #ff00f0, #f0ff00, #ff0080);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientText 3s ease infinite;
        margin: 0;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
    }
    
    @keyframes gradientText {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* 副标题 - 移到logo容器 */
    .auth-subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.0rem;
        margin: 10px 0 0 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    /* 登录容器：直接美化 Streamlit 的 form 容器作为玻璃卡片 */
    div[data-testid="stForm"] {
        position: relative;
        z-index: 10;
        max-width: 520px;
        width: 100%;
        margin: 0 auto;
        padding: 40px !important;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        animation: glowing 2s ease-in-out infinite alternate;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* 让 form 内部也水平垂直置中 */
    div[data-testid="stForm"] form {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 16px;
    }
    
    @keyframes glowing {
        0% { box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2), 0 0 20px rgba(83, 52, 131, 0.5); }
        100% { box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2), 0 0 40px rgba(83, 52, 131, 0.8); }
    }
    
    /* 输入框和按钮容器 */
    .login-form {
        display: flex;
        flex-direction: column;
        gap: 20px;
        align-items: center;
        max-width: 300px;
        margin: 0 auto;
    }
    
    /* 表单样式 */
    .stForm { border: none !important; background: transparent !important; }
    
    /* 输入框容器 */
    .stTextInput {
        width: 100% !important;
        max-width: 250px !important;
        margin: 0 auto !important; /* 居中输入框容器 */
    }
    
    /* 霓虹边框效果（透明输入框） */
    .stTextInput > div > div > input {
        background: transparent !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        color: white !important;
        font-size: 1.1rem !important;
        padding: 12px 20px !important;
        text-align: center !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 
            0 4px 15px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
        width: 250px !important;
        max-width: 250px !important;
        margin: 0 auto 10px auto !important; /* 居中具体输入 */
    }

    /* placeholder 更清晰 */
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.8) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border: 2px solid #00f0ff !important;
        box-shadow: 
            0 4px 15px rgba(0, 0, 0, 0.2),
            0 0 20px rgba(0, 240, 255, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        transform: translateY(-2px) !important;
        outline: none !important;
    }

    /* 移除浏览器默认的红色错误/焦点描边 */
    .stTextInput > div:focus-within {
        outline: none !important;
        box-shadow: none !important;
    }
    .stTextInput input:focus,
    .stTextInput input:focus-visible,
    .stTextInput input:invalid,
    .stTextInput input:focus:invalid {
        outline: none !important;
        box-shadow: none !important;
    }
    .stTextInput > div {
        border: none !important; /* 去掉外层边框，防止出现红色描边 */
    }
    
    /* 按钮样式 */
    .stFormSubmitButton > button,
    .stButton > button {
        background: linear-gradient(45deg, #ff0080, #ff8c00, #40e0d0) !important;
        background-size: 300% 300% !important;
        border: none !important;
        border-radius: 15px !important;
        color: white !important;
        font-size: 1.0rem !important;
        font-weight: bold !important;
        padding: 12px 20px !important;
        transition: all 0.3s ease !important;
        box-shadow: 
            0 4px 15px rgba(255, 0, 128, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        animation: buttonGlow 2s ease-in-out infinite alternate !important;
        width: 100% !important; /* 按钮填满容器 */
        max-width: 250px !important;
        height: 50px !important;
        cursor: pointer !important;
        white-space: nowrap !important; /* 防止文字换行 */
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    /* 让提交按钮容器在表单中居中，固定容器宽度与输入框一致 */
    .stFormSubmitButton {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 250px !important;   /* 与输入框宽度一致 */
        margin: 4px auto 0 auto !important; /* 居中 */
    }
    .stFormSubmitButton > div { /* 有些版本外层还会包一层 div */
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }

    /* 移除密码输入框右侧的“眼睛”按钮及其深色背景，避免视觉偏移 */
    .stTextInput button,
    .stTextInput [role="button"] {
        display: none !important;
    }
    .stTextInput > div {
        background: transparent !important;
        box-shadow: none !important;
    }
    
    @keyframes buttonGlow {
        0% { 
            background-position: 0% 50%;
            box-shadow: 0 4px 15px rgba(255, 0, 128, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        }
        100% { 
            background-position: 100% 50%;
            box-shadow: 0 4px 25px rgba(255, 0, 128, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        }
    }
    
    .stFormSubmitButton > button:hover,
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 
            0 8px 25px rgba(255, 0, 128, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    }
    
    /* 移除Streamlit默认样式 */
    .stTextInput > label {
        display: none !important;
    }
    
    .stForm > div {
        gap: 20px !important;
    }
    
    /* 隐藏不必要的元素 */
    .stDeployButton {
        display: none !important;
    }
    
    /* 隐藏"Press Enter to submit form"提示文字 */
    div[data-testid="stForm"] div[data-testid="InputInstructions"],
    div[data-testid="InputInstructions"],
    div[role="alert"]:not(.stAlert),
    small:contains("Press Enter to submit form"),
    span:contains("Press Enter to submit form"),
    p:contains("Press Enter to submit form") {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* 更广泛的隐藏规则 */
    div[data-testid="stForm"] small,
    div[data-testid="stForm"] .instructions,
    [class*="instruction"],
    [class*="hint"],
    [data-testid*="instruction"] {
        display: none !important;
    }
    
    /* 列布局优化 */
    .row-widget.stHorizontal {
        justify-content: center !important;
    }
    
    /* 错误信息样式 */
    .stAlert {
        background: rgba(255, 82, 82, 0.1) !important;
        border: 1px solid rgba(255, 82, 82, 0.3) !important;
        border-radius: 10px !important;
        color: #ff6b6b !important;
        backdrop-filter: blur(10px) !important;
        text-align: center !important;
    }
    
    /* 版权信息样式 */
    .copyright {
        text-align: center;
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.85rem;
        margin-top: 30px;
        padding: 15px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        background: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
        backdrop-filter: blur(5px);
    }
    
    .copyright a {
        color: #00f0ff;
        text-decoration: none;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .copyright a:hover {
        color: #ff00f0;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }
    
    /* 浮动光点效果 */
    .floating-orbs {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        pointer-events: none;
        z-index: 2;
    }
    
    .orb {
        position: absolute;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.8), rgba(0, 240, 255, 0.4));
        animation: float 20s infinite linear;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.6);
    }
    
    @keyframes float {
        0% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100px) rotate(360deg);
            opacity: 0;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 创建浮动光点背景效果
    st.markdown("""
    <div class="floating-orbs">
        <div class="orb" style="width: 6px; height: 6px; left: 10%; animation-delay: 0s; animation-duration: 15s;"></div>
        <div class="orb" style="width: 4px; height: 4px; left: 20%; animation-delay: 5s; animation-duration: 18s;"></div>
        <div class="orb" style="width: 8px; height: 8px; left: 30%; animation-delay: 2s; animation-duration: 20s;"></div>
        <div class="orb" style="width: 5px; height: 5px; left: 40%; animation-delay: 8s; animation-duration: 22s;"></div>
        <div class="orb" style="width: 7px; height: 7px; left: 50%; animation-delay: 1s; animation-duration: 19s;"></div>
        <div class="orb" style="width: 4px; height: 4px; left: 60%; animation-delay: 6s; animation-duration: 17s;"></div>
        <div class="orb" style="width: 6px; height: 6px; left: 70%; animation-delay: 3s; animation-duration: 21s;"></div>
        <div class="orb" style="width: 5px; height: 5px; left: 80%; animation-delay: 7s; animation-duration: 16s;"></div>
        <div class="orb" style="width: 8px; height: 8px; left: 90%; animation-delay: 4s; animation-duration: 23s;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Logo容器 - 在主容器上方
    st.markdown('''
    <div class="logo-container">
        <h1 class="auth-title">🎰 Baccarat Simulator</h1>
        <p class="auth-subtitle">✨ Please enter access password to continue ✨</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # 登录表单（使用 Streamlit 原生 form；通过 CSS 对 div[data-testid="stForm"] 做玻璃样式）
    # 使用form来支持Enter键登录
    with st.form("login_form", clear_on_submit=False):
        # 密码输入框
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password...",
            key="password_input",
            label_visibility="collapsed",
        )

        # 登录按钮 - 放入中间列，强制几何居中
        col_left, col_mid, col_right = st.columns([1, 1, 1])
        with col_mid:
            submitted = st.form_submit_button("🚀 Enter System", use_container_width=True)

        # 处理登录逻辑
        if submitted:
            if password == correct_password:
                st.session_state.authenticated = True
                st.session_state.password_attempts = 0
                st.success("🎉 Authentication successful! Entering system...")
                time.sleep(1)
                st.rerun()
            else:
                st.session_state.password_attempts = st.session_state.get("password_attempts", 0) + 1
                st.error("❌ Incorrect password, please try again")
                if st.session_state.password_attempts >= 3:
                    st.warning("⚠️ Multiple failed attempts, please check your password")
    
    # 版权信息
    st.markdown('''
    <div class="copyright">
        © 2025 Copyright belongs to <a href="https://1plabs.pro" target="_blank">1plabs.pro</a>
    </div>
    ''', unsafe_allow_html=True)
    
    st.stop()  # 阻止页面继续渲染


def _safe_rerun():
    # Streamlit >= 1.25 provides st.rerun; older versions had experimental_rerun
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()


def render_sidebar_branding():
    """Render a small branding area in the sidebar: logo + copyright.

    Logo source priority:
      1) LOGO_URL env (remote or data URL)
      2) LOGO_PATH env (absolute or relative to CWD)
      3) data/logo.png (mounted by default via docker-compose)
    """
    logo_url = os.environ.get("LOGO_URL")
    logo_path = os.environ.get("LOGO_PATH") or os.path.join("data", "logo.png")
    copyright_text = os.environ.get("COPYRIGHT_TEXT", "© 2025 1plabs.pro")

    st.sidebar.markdown("""
    <div style="text-align:center; margin-top: 4px; margin-bottom: 10px;">
    <style>
    .brand-logo img { border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.25); }
    .brand-copy { color: rgba(255,255,255,0.6); font-size: 12px; margin-top: 6px; }
    </style>
    </div>
    """, unsafe_allow_html=True)

    # Logo
    try:
        if logo_url:
            st.sidebar.image(logo_url, use_container_width=True, output_format="PNG")
        elif os.path.exists(logo_path):
            st.sidebar.image(logo_path, use_container_width=True)
        else:
            st.sidebar.markdown("<div style='text-align:center; opacity:0.8;'>Baccarat Simulator</div>", unsafe_allow_html=True)
    except Exception:
        st.sidebar.markdown("<div style='text-align:center; opacity:0.8;'>Baccarat Simulator</div>", unsafe_allow_html=True)

    # Copyright
    st.sidebar.markdown(
        f"<div class='brand-copy' style='text-align:center;'>{copyright_text}</div>",
        unsafe_allow_html=True,
    )


def _run_batch(params: RunParams):
    """Run a full simulation and return (events, summary), compatible with both
    old and new simulate_hands APIs.

    If simulate_hands returns a generator (legacy), we'll exhaust it and
    capture the final StopIteration.value as summary.
    """
    res = simulate_hands(params, yield_per_hand=False)
    if isinstance(res, tuple):
        return res
    # Legacy path: res is a generator
    events = []
    gen = res
    try:
        while True:
            events.append(next(gen))
    except StopIteration as stop:
        summary = stop.value
    return events, summary

# 移除原本的st.set_page_config，因为现在在main函数中设置

CSV_COLUMNS = [
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


def to_df(events) -> pd.DataFrame:
    rows = []
    for e in events:
        d = asdict(e)
        d["player_cards"] = json.dumps(d["player_cards"], ensure_ascii=False)
        d["banker_cards"] = json.dumps(d["banker_cards"], ensure_ascii=False)
        rows.append(d)
    return pd.DataFrame(rows, columns=CSV_COLUMNS)


def render_summary(summary, rebate_pct: float = 0.0):
    total_wagered = summary.total_wagered
    rebate_amt = round(total_wagered * rebate_pct, 2)
    profit_with_rebate = round(summary.total_profit + rebate_amt, 2)
    roi_with_rebate = (profit_with_rebate / total_wagered) if total_wagered > 0 else 0.0

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Initial 初始本金", f"{summary.initial_bankroll:,.2f}")
    c2.metric("Final 期末本金", f"{summary.final_bankroll:,.2f}", f"{summary.total_profit:+,.2f}")
    c3.metric("ROI 投资回报率", f"{summary.roi*100:.2f}%")
    c4.metric("Commission 佣金", f"{summary.commission_total:,.2f}")
    c5.metric("Turnover 流水", f"{total_wagered:,.2f}")

    c6, c7, c8, c9, c10 = st.columns(5)
    c6.metric("Bet hands 下注局数", f"{summary.bet_hands}")
    c7.metric("Observe 观望局数", f"{summary.observe_hands}")
    c8.metric("Pushes 和局下注", f"{summary.push_hands}")
    hr = summary.strategy_hit_rate
    c9.metric("Hit rate 胜率", f"{hr*100:.2f}%" if hr is not None else "N/A")
    c10.metric("Rebate 返水", f"{rebate_amt:,.2f}")

    c11, c12 = st.columns(2)
    c11.metric("Profit+Rebate 含返水收益", f"{profit_with_rebate:+,.2f}")
    c12.metric("ROI(含返)", f"{roi_with_rebate*100:.2f}%")

    st.write(
        f"Outcomes 结果: Player 闲 {summary.player_wins} ({summary.outcome_distribution['player']['pct']*100:.2f}%), "
        f"Banker 庄 {summary.banker_wins} ({summary.outcome_distribution['banker']['pct']*100:.2f}%), "
        f"Tie 和 {summary.ties} ({summary.outcome_distribution['tie']['pct']*100:.2f}%)"
    )


def _save_settings_to_file(payload: dict, filename: str = "ui_settings.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        st.sidebar.success(f"已保存到 {filename}")
    except Exception as e:
        st.sidebar.error(f"保存失败: {e}")


def _settings_sidebar_io(section_title: str, mode: str, values: dict):
    """Render a small Save/Load block in the sidebar.

    values will be embedded into a JSON along with mode and autorun flag.
    """
    with st.sidebar.expander(section_title, expanded=False):
        autorun = st.checkbox("载入后自动运行", value=False, key=f"{mode}_autorun")
        # Download JSON
        payload = {"mode": mode, "autorun": autorun, **values}
        json_bytes = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        st.download_button("下载设定JSON", data=json_bytes, file_name=f"baccarat_{mode}_settings.json", mime="application/json")

        c1, c2 = st.columns(2)
        if c1.button("保存到本地文件"):
            _save_settings_to_file(payload)
        uploaded = c2.file_uploader("载入设定JSON", type=["json"], key=f"{mode}_upload")
        if uploaded is not None:
            try:
                data = json.loads(uploaded.read().decode("utf-8"))
                # apply common
                if "mode" in data:
                    st.session_state["mode_radio"] = "播放模式" if data["mode"] == "play" else "极速模式"
                # stuff specific keys back into session for widgets
                for k, v in data.items():
                    keyname = f"{mode}_{k}"
                    if keyname in st.session_state:
                        st.session_state[keyname] = v
                st.session_state[f"{mode}_loaded_payload"] = data
                _safe_rerun()
            except Exception as e:
                st.sidebar.error(f"载入失败: {e}")


def page_play_mode():
    st.sidebar.header("Playback Settings")
    bankroll = st.sidebar.number_input("bankroll 初始本金", min_value=1.0, value=10000.0, step=100.0, key="play_bankroll")
    bet = st.sidebar.number_input("bet", min_value=0.01, value=200.0, step=10.0, key="play_bet")
    hands = st.sidebar.number_input("hands 局数", min_value=1, value=1000, step=100, key="play_hands")
    decks = st.sidebar.selectbox("decks 副牌数", options=[6, 8], index=1, key="play_decks")
    penetration = st.sidebar.number_input("penetration 渗透阈值", min_value=1, value=52, step=1, key="play_penetration")
    strategy = st.sidebar.selectbox(
        "strategy 策略",
        options=["flip-opposite-wait", "always-banker", "always-player", "alternate", "random"],
        index=0,
        key="play_strategy",
    )
    seed_str = st.sidebar.text_input("seed 随机种子 (可选)", key="play_seed_str")
    seed = int(seed_str) if seed_str.strip().isdigit() else None
    speed_sec = st.sidebar.slider("speed_sec 每局速度(秒)", min_value=0.0, max_value=60.0, value=0.3, step=0.1, key="play_speed")
    auto_scroll = st.sidebar.checkbox("auto scroll 自动滚动到最新", value=True, key="play_auto_scroll")
    rebate_pct = st.sidebar.number_input("rebate 返水比例(%)", min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="play_rebate_pct")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🎯 连输/连赢注码设置**")
    loss_prog_pct = st.sidebar.number_input("loss progression 连输加注(%)", min_value=0.0, max_value=200.0, value=0.0, step=1.0, key="play_loss_prog")
    # 新增：连输减注(%)
    loss_prog_dec_pct = st.sidebar.number_input("loss progression 连输减注(%)", min_value=0.0, max_value=99.0, value=0.0, step=1.0, key="play_loss_prog_dec")
    loss_prog_start = st.sidebar.number_input("从第几连输开始加注", min_value=1, max_value=20, value=1, step=1, key="play_loss_prog_start")
    loss_win_mode = st.sidebar.selectbox("赢后注码调整", options=["reset", "persist", "ignore"], index=0, key="play_loss_win_mode")
    st.sidebar.markdown("---")
    win_inc_pct = st.sidebar.number_input("win progression 连赢加注(%)", min_value=0.0, max_value=200.0, value=0.0, step=1.0, key="play_win_inc_pct")
    win_dec_pct = st.sidebar.number_input("win progression 连赢减注(%)", min_value=0.0, max_value=99.0, value=0.0, step=1.0, key="play_win_dec_pct")
    win_prog_start = st.sidebar.number_input("从第几连赢开始生效", min_value=1, max_value=20, value=1, step=1, key="play_win_prog_start")
    win_loss_mode = st.sidebar.selectbox("输后注码调整(针对连赢设置)", options=["reset", "persist", "ignore"], index=0, key="play_win_loss_mode")
    
    # 加注计算说明
    if loss_prog_pct > 0:
        increased_bet = bet * (1 + loss_prog_pct/100)
        st.sidebar.markdown(f"""
        <div style='background: rgba(255,165,0,0.1); padding: 10px; border-radius: 5px; font-size: 12px;'>
        <b>📊 连输加注示例 (基础: {bet:.0f})</b><br>
        • 正常下注: {bet:.0f}<br>
        • 连输时下注: {increased_bet:.0f} (固定增加{loss_prog_pct:.0f}%)<br>
        • 无论连输几次，都是: {increased_bet:.0f}<br>
        <small>📝 计算公式: 基础下注 × (1 + {loss_prog_pct:.0f}%) = {bet:.0f} × {1 + loss_prog_pct/100:.2f} = {increased_bet:.0f}</small>
        </div>
        """, unsafe_allow_html=True)

    if win_inc_pct > 0 or win_dec_pct > 0:
        if win_inc_pct > 0:
            win_bet = bet * (1 + win_inc_pct/100)
            extra = f"连赢加注: {win_bet:.0f} (+{win_inc_pct:.0f}%)"
        else:
            win_bet = bet * (1 - win_dec_pct/100)
            extra = f"连赢减注: {win_bet:.0f} (-{win_dec_pct:.0f}%)"
        st.sidebar.markdown(f"""
        <div style='background: rgba(135,206,250,0.15); padding: 10px; border-radius: 5px; font-size: 12px;'>
        <b>📊 连赢调整示例 (基础: {bet:.0f})</b><br>
        • 正常下注: {bet:.0f}<br>
        • {extra}<br>
        <small>📝 从第 {win_prog_start} 次连赢开始生效；当选择“persist”时会在输之前保持调整后的注码</small>
        </div>
        """, unsafe_allow_html=True)

    # Save/Load settings utilities
    _settings_sidebar_io(
        "保存/载入设定",
        mode="play",
        values={
            "bankroll": bankroll,
            "bet": bet,
            "hands": hands,
            "decks": decks,
            "penetration": penetration,
            "strategy": strategy,
            "seed": seed,
            "speed_sec": speed_sec,
            "auto_scroll": auto_scroll,
            "rebate_pct": rebate_pct,
            "loss_progression_pct": loss_prog_pct,
            "loss_progression_dec_pct": loss_prog_dec_pct,
            "loss_progression_start": loss_prog_start,
            "loss_progression_win_mode": loss_win_mode,
                "win_progression_inc_pct": win_inc_pct,
                "win_progression_dec_pct": win_dec_pct,
                "win_progression_start": win_prog_start,
                "win_progression_loss_mode": win_loss_mode,
        },
    )

    if "params" not in st.session_state:
        st.session_state.params = None
    if "events" not in st.session_state:
        st.session_state.events = []
    if "gen" not in st.session_state:
        st.session_state.gen = None
    if "playing" not in st.session_state:
        st.session_state.playing = False

    def reset_state():
        st.session_state.events = []
        st.session_state.gen = None
        st.session_state.playing = False
        st.session_state.params = RunParams(
            bankroll=bankroll,
            bet=bet,
            hands=hands,
            decks=decks,
            penetration=penetration,
            strategy=strategy,
            seed=seed,
            csv_path=None,
            json_path=None,
        )

    if st.sidebar.button("Reset"):
        reset_state()

    if st.session_state.params is None:
        reset_state()

    def _build_params_from_widgets() -> RunParams:
        return RunParams(
            bankroll=st.session_state.get("play_bankroll", bankroll),
            bet=st.session_state.get("play_bet", bet),
            hands=st.session_state.get("play_hands", hands),
            decks=st.session_state.get("play_decks", decks),
            penetration=st.session_state.get("play_penetration", penetration),
            strategy=st.session_state.get("play_strategy", strategy),
            seed=(int(st.session_state.get("play_seed_str")) if str(st.session_state.get("play_seed_str", "")).strip().isdigit() else None),
            csv_path=None,
            json_path=None,
            loss_progression_pct=st.session_state.get("play_loss_prog", loss_prog_pct),
            loss_progression_dec_pct=st.session_state.get("play_loss_prog_dec", loss_prog_dec_pct),
            loss_progression_start=st.session_state.get("play_loss_prog_start", loss_prog_start),
            loss_progression_win_mode=st.session_state.get("play_loss_win_mode", loss_win_mode),
            win_progression_inc_pct=st.session_state.get("play_win_inc_pct", win_inc_pct),
            win_progression_dec_pct=st.session_state.get("play_win_dec_pct", win_dec_pct),
            win_progression_start=st.session_state.get("play_win_prog_start", win_prog_start),
            win_progression_loss_mode=st.session_state.get("play_win_loss_mode", win_loss_mode),
        )

    # If user loaded settings with autorun, start automatically once
    loaded = st.session_state.get("play_loaded_payload")
    if loaded and loaded.get("autorun") and not st.session_state.playing and st.session_state.gen is None:
        st.session_state.params = _build_params_from_widgets()
        st.session_state.gen = simulate_hands(st.session_state.params, yield_per_hand=True)
        st.session_state.playing = True

    st.title("Baccarat Simulator - Playback")

    # Controls
    c_ctrl1, c_ctrl2, c_ctrl3, c_ctrl4, c_ctrl5, c_ctrl6 = st.columns(6)
    if c_ctrl1.button("Start"):
        st.session_state.params = _build_params_from_widgets()
        st.session_state.gen = simulate_hands(st.session_state.params, yield_per_hand=True)
        st.session_state.playing = True
    if c_ctrl2.button("Pause"):
        st.session_state.playing = False
    if c_ctrl3.button("Resume"):
        if st.session_state.gen is None:
            st.session_state.params = _build_params_from_widgets()
            st.session_state.gen = simulate_hands(st.session_state.params, yield_per_hand=True)
        st.session_state.playing = True
    if c_ctrl4.button("Next"):
        if st.session_state.gen is None:
            st.session_state.params = _build_params_from_widgets()
            st.session_state.gen = simulate_hands(st.session_state.params, yield_per_hand=True)
        try:
            ev = next(st.session_state.gen)
            st.session_state.events.append(ev)
        except StopIteration:
            st.session_state.playing = False
    if c_ctrl5.button("Skip 5"):
        if st.session_state.gen is None:
            st.session_state.params = _build_params_from_widgets()
            st.session_state.gen = simulate_hands(st.session_state.params, yield_per_hand=True)
        for _ in range(5):
            try:
                ev = next(st.session_state.gen)
                st.session_state.events.append(ev)
            except StopIteration:
                st.session_state.playing = False
                break
    if c_ctrl6.button("Skip to Report"):
        if st.session_state.gen is None:
            st.session_state.params = _build_params_from_widgets()
            st.session_state.gen = simulate_hands(st.session_state.params, yield_per_hand=True)
        for ev in st.session_state.gen:
            st.session_state.events.append(ev)
        st.session_state.playing = False

    # Live playback
    placeholder_metrics = st.empty()
    placeholder_detail = st.empty()
    # charts are drawn fresh each rerun to avoid add_rows target errors
    placeholder_table = st.empty()

    if st.session_state.playing:
        # iterate one step
        try:
            ev = next(st.session_state.gen)
            st.session_state.events.append(ev)
        except StopIteration:
            st.session_state.playing = False

        # pacing
        if speed_sec > 0:
            time.sleep(speed_sec)

    events = st.session_state.events

    # Summary-like derived values during playback
    if events:
        last = events[-1]
        player_count = sum(1 for e in events if e.outcome == "player")
        banker_count = sum(1 for e in events if e.outcome == "banker")
        tie_count = sum(1 for e in events if e.outcome == "tie")
        bet_count = sum(1 for e in events if e.bet_side)
        push_count = sum(1 for e in events if e.bet_side and e.outcome == "tie")
        wins = sum(1 for e in events if e.bet_side and e.bet_side == e.outcome)
        attempts = bet_count - push_count
        hit_rate = (wins / attempts) if attempts > 0 else None

        with placeholder_metrics.container():
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Progress", f"{last.hand_no}/{st.session_state.params.hands}")
            c2.metric("Bankroll", f"{last.bankroll_after:,.2f}", f"{last.cumulative_win:+,.2f}")
            c3.metric("Player", f"{player_count} ({(player_count/len(events))*100:.2f}%)")
            c4.metric("Banker", f"{banker_count} ({(banker_count/len(events))*100:.2f}%)")
            c5.metric("Tie", f"{tie_count} ({(tie_count/len(events))*100:.2f}%)")
            st.caption(f"Hit rate 胜率: {hit_rate*100:.2f}%" if hit_rate is not None else "Hit rate 胜率: N/A")

        # extra KPI row: turnover/rebate/profit(+rebate)
        total_wagered = sum(e.bet_amount for e in events if e.bet_side)
        rebate_amt = round(total_wagered * (rebate_pct/100.0), 2)
        profit = round(last.bankroll_after - float(st.session_state.params.bankroll), 2)
        profit_with_rebate = round(profit + rebate_amt, 2)
        roi = (profit / total_wagered) if total_wagered > 0 else 0.0
        roi_with_rebate = (profit_with_rebate / total_wagered) if total_wagered > 0 else 0.0

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Turnover 流水", f"{total_wagered:,.2f}")
        k2.metric("Rebate 返水", f"{rebate_amt:,.2f}")
        k3.metric("Profit 收益", f"{profit:+,.2f}")
        k4.metric("ROI/含返", f"{roi*100:.2f}% / {roi_with_rebate*100:.2f}%")

        with placeholder_detail.container():
            st.subheader("当前局详情")
            st.write(
                f"Hand #{last.hand_no}: Bet={last.bet_side or '-'} Amt={last.bet_amount:.2f} | "
                f"P={last.player_cards} ({last.player_total}) vs B={last.banker_cards} ({last.banker_total}) -> {last.outcome} | "
                f"Win={last.win_amount:+.2f} | Comm={last.commission_paid:.2f}"
            )

        # Charts row: bankroll curve (last 2000) and P&L histogram (all so far)
        colA, colB = st.columns(2)
        recent = events[-2000:]
        if len(recent) >= 2:
            chart_df = pd.DataFrame({
                "hand_no": [e.hand_no for e in recent],
                "bankroll_after": [e.bankroll_after for e in recent],
            })
            line = (
                alt.Chart(chart_df)
                .mark_line(point=False)
                .encode(
                    x=alt.X("hand_no:Q", title="Hand #"),
                    y=alt.Y("bankroll_after:Q", title="Bankroll"),
                    tooltip=["hand_no", "bankroll_after"],
                )
                .properties(height=280)
            )
            colA.subheader("资金曲线（最近2000局）")
            colA.altair_chart(line, use_container_width=True)

        pnl_df = pd.DataFrame({"win_amount": [e.win_amount for e in events]})
        if len(pnl_df) >= 1:
            hist = (
                alt.Chart(pnl_df)
                .transform_bin("win_amount_binned", field="win_amount", bin={"maxbins": 60})
                .mark_bar()
                .encode(
                    x=alt.X("win_amount_binned:Q", title="每局盈亏", bin="binned"),
                    x2="win_amount_binned_end:Q",
                    y=alt.Y("count():Q", title="次数"),
                )
                .properties(height=280)
            )
            colB.subheader("盈亏分布")
            colB.altair_chart(hist, use_container_width=True)

        # Recent table N=30
        table_df = to_df(events[-30:])
        placeholder_table.dataframe(table_df, use_container_width=True)

        # Downloads section - show when there are events
        if len(events) > 0:
            st.subheader("📥 数据下载")
            col_down1, col_down2 = st.columns(2)
            
            # Generate full CSV and summary for download
            full_df = to_df(events)
            csv_bytes = full_df.to_csv(index=False).encode("utf-8")
            
            # Create summary-like data for JSON download
            summary_data = {
                "total_hands": len(events),
                "bet_hands": sum(1 for e in events if e.bet_side),
                "observe_hands": sum(1 for e in events if not e.bet_side),
                "player_wins": sum(1 for e in events if e.outcome == "player"),
                "banker_wins": sum(1 for e in events if e.outcome == "banker"),
                "ties": sum(1 for e in events if e.outcome == "tie"),
                "total_wagered": sum(e.bet_amount for e in events if e.bet_side),
                "current_bankroll": last.bankroll_after,
                "total_profit": last.cumulative_win,
                "commission_paid": sum(e.commission_paid for e in events),
                "hit_rate": hit_rate,
                "settings": {
                    "initial_bankroll": float(st.session_state.params.bankroll),
                    "bet_amount": float(st.session_state.params.bet),
                    "strategy": st.session_state.params.strategy,
                    "decks": st.session_state.params.decks,
                    "penetration": st.session_state.params.penetration
                }
            }
            json_bytes = json.dumps(summary_data, ensure_ascii=False, indent=2).encode("utf-8")
            
            with col_down1:
                st.download_button(
                    "📊 下载完整CSV数据", 
                    data=csv_bytes, 
                    file_name=f"baccarat_playback_{len(events)}hands.csv", 
                    mime="text/csv"
                )
            
            with col_down2:
                st.download_button(
                    "📋 下载统计JSON", 
                    data=json_bytes, 
                    file_name=f"baccarat_playback_summary_{len(events)}hands.json", 
                    mime="application/json"
                )

    # trigger next tick only while playing (prevents infinite rerun when paused)
        if auto_scroll and st.session_state.playing:
            _safe_rerun()


def page_fast_mode():
    st.sidebar.header("Fast Mode Settings")
    bankroll = st.sidebar.number_input("bankroll 初始本金", min_value=1.0, value=10000.0, step=100.0, key="fast_bankroll")
    bet = st.sidebar.number_input("bet", min_value=0.01, value=200.0, step=10.0, key="fast_bet")
    hands = st.sidebar.number_input("hands 局数", min_value=1, value=10000, step=1000, key="fast_hands")
    decks = st.sidebar.selectbox("decks 副牌数", options=[6, 8], index=1, key="fast_decks")
    penetration = st.sidebar.number_input("penetration 渗透阈值", min_value=1, value=52, step=1, key="fast_penetration")
    strategy = st.sidebar.selectbox(
        "strategy 策略",
        options=["flip-opposite-wait", "always-banker", "always-player", "alternate", "random"],
        index=0,
        key="fast_strategy",
    )
    seed_str = st.sidebar.text_input("seed 随机种子 (可选)", key="fast_seed_str")
    seed = int(seed_str) if seed_str.strip().isdigit() else None
    rebate_pct_fast = st.sidebar.number_input("rebate 返水比例(%)", min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="fast_rebate_pct")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🎯 连输/连赢注码设置**")
    loss_prog_pct_fast = st.sidebar.number_input("loss progression 连输加注(%)", min_value=0.0, max_value=200.0, value=0.0, step=1.0, key="fast_loss_prog")
    loss_prog_dec_pct_fast = st.sidebar.number_input("loss progression 连输减注(%)", min_value=0.0, max_value=99.0, value=0.0, step=1.0, key="fast_loss_prog_dec")
    loss_prog_start_fast = st.sidebar.number_input("从第几连输开始加注", min_value=1, max_value=20, value=1, step=1, key="fast_loss_prog_start")
    loss_win_mode_fast = st.sidebar.selectbox("赢后注码调整", options=["reset", "persist", "ignore"], index=0, key="fast_loss_win_mode")
    st.sidebar.markdown("---")
    win_inc_pct_fast = st.sidebar.number_input("win progression 连赢加注(%)", min_value=0.0, max_value=200.0, value=0.0, step=1.0, key="fast_win_inc_pct")
    win_dec_pct_fast = st.sidebar.number_input("win progression 连赢减注(%)", min_value=0.0, max_value=99.0, value=0.0, step=1.0, key="fast_win_dec_pct")
    win_prog_start_fast = st.sidebar.number_input("从第几连赢开始生效", min_value=1, max_value=20, value=1, step=1, key="fast_win_prog_start")
    win_loss_mode_fast = st.sidebar.selectbox("输后注码调整(针对连赢设置)", options=["reset", "persist", "ignore"], index=0, key="fast_win_loss_mode")
    
    # 加注计算说明
    if loss_prog_pct_fast > 0:
        increased_bet = bet * (1 + loss_prog_pct_fast/100)
        st.sidebar.markdown(f"""
        <div style='background: rgba(255,165,0,0.1); padding: 10px; border-radius: 5px; font-size: 12px;'>
        <b>📊 连输加注示例 (基础: {bet:.0f})</b><br>
        • 正常下注: {bet:.0f}<br>
        • 连输时下注: {increased_bet:.0f} (固定增加{loss_prog_pct_fast:.0f}%)<br>
        • 无论连输几次，都是: {increased_bet:.0f}<br>
        <small>📝 计算公式: 基础下注 × (1 + {loss_prog_pct_fast:.0f}%) = {bet:.0f} × {1 + loss_prog_pct_fast/100:.2f} = {increased_bet:.0f}</small>
        </div>
        """, unsafe_allow_html=True)

    if win_inc_pct_fast > 0 or win_dec_pct_fast > 0:
        if win_inc_pct_fast > 0:
            win_bet = bet * (1 + win_inc_pct_fast/100)
            extra = f"连赢加注: {win_bet:.0f} (+{win_inc_pct_fast:.0f}%)"
        else:
            win_bet = bet * (1 - win_dec_pct_fast/100)
            extra = f"连赢减注: {win_bet:.0f} (-{win_dec_pct_fast:.0f}%)"
        st.sidebar.markdown(f"""
        <div style='background: rgba(135,206,250,0.15); padding: 10px; border-radius: 5px; font-size: 12px;'>
        <b>📊 连赢调整示例 (基础: {bet:.0f})</b><br>
        • 正常下注: {bet:.0f}<br>
        • {extra}<br>
        <small>📝 从第 {win_prog_start_fast} 次连赢开始生效；当选择“persist”时会在输之前保持调整后的注码</small>
        </div>
        """, unsafe_allow_html=True)

    _settings_sidebar_io(
        "保存/载入设定",
        mode="fast",
        values={
            "bankroll": bankroll,
            "bet": bet,
            "hands": hands,
            "decks": decks,
            "penetration": penetration,
            "strategy": strategy,
            "seed": seed,
            "rebate_pct": rebate_pct_fast,
            "loss_progression_pct": loss_prog_pct_fast,
            "loss_progression_dec_pct": loss_prog_dec_pct_fast,
            "loss_progression_start": loss_prog_start_fast,
            "loss_progression_win_mode": loss_win_mode_fast,
            "win_progression_inc_pct": win_inc_pct_fast,
            "win_progression_dec_pct": win_dec_pct_fast,
            "win_progression_start": win_prog_start_fast,
            "win_progression_loss_mode": win_loss_mode_fast,
        },
    )

    st.title("Baccarat Simulator - Fast Mode")

    auto_run_loaded = st.session_state.get("fast_loaded_payload", {}).get("autorun", False)
    run_clicked = st.button("运行（只看报告）") or auto_run_loaded
    if run_clicked:
        params = RunParams(
            bankroll=bankroll,
            bet=bet,
            hands=hands,
            decks=decks,
            penetration=penetration,
            strategy=strategy,
            seed=seed,
            csv_path=None,
            json_path=None,
            loss_progression_pct=loss_prog_pct_fast,
            loss_progression_dec_pct=loss_prog_dec_pct_fast,
            loss_progression_start=loss_prog_start_fast,
            loss_progression_win_mode=loss_win_mode_fast,
            win_progression_inc_pct=win_inc_pct_fast,
            win_progression_dec_pct=win_dec_pct_fast,
            win_progression_start=win_prog_start_fast,
            win_progression_loss_mode=win_loss_mode_fast,
        )
        events, summary = _run_batch(params)

        render_summary(summary, rebate_pct=(rebate_pct_fast/100.0))
        df = to_df(events)

        # Charts row (full dataset)
        colA, colB = st.columns(2)
        if len(df) >= 2:
            line = (
                alt.Chart(df.assign(hand_no=df["hand_no"].astype(int)))
                .mark_line()
                .encode(
                    x=alt.X("hand_no:Q", title="Hand #"),
                    y=alt.Y("bankroll_after:Q", title="Bankroll"),
                )
                .properties(height=300)
            )
            colA.subheader("资金曲线（全量）")
            colA.altair_chart(line, use_container_width=True)

        if len(df) >= 1:
            pnl = (
                alt.Chart(df)
                .transform_bin("win_amount_binned", field="win_amount", bin={"maxbins": 60})
                .mark_bar()
                .encode(
                    x=alt.X("win_amount_binned:Q", title="每局盈亏", bin="binned"),
                    x2="win_amount_binned_end:Q",
                    y=alt.Y("count():Q", title="次数"),
                )
                .properties(height=300)
            )
            colB.subheader("盈亏分布（全量）")
            colB.altair_chart(pnl, use_container_width=True)

        # Show preview head/tail
        st.subheader("结果预览（前后各20行）")
        st.dataframe(pd.concat([df.head(20), df.tail(20)]), use_container_width=True)

        # Downloads
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        json_bytes = json.dumps(asdict(summary), ensure_ascii=False, indent=2).encode("utf-8")
        st.download_button("下载 CSV", data=csv_bytes, file_name="baccarat_report.csv", mime="text/csv")
        st.download_button("下载 JSON", data=json_bytes, file_name="baccarat_summary.json", mime="application/json")

        if st.button("重新开始"):
            _safe_rerun()


def main():
    # 首先进行密码验证
    ensure_authenticated()
    
    # 验证通过后设置页面配置
    st.set_page_config(page_title="Baccarat Simulator", layout="wide")
    
    # 添加登出功能到侧边栏
    with st.sidebar:
        # 顶部品牌区：Logo + 版权
        render_sidebar_branding()
        st.markdown("---")
        if st.button("🚪 登出系统"):
            st.session_state.authenticated = False
            st.rerun()
    
    mode = st.sidebar.radio("模式", options=["播放模式", "极速模式"], index=0, key="mode_radio")
    if mode == "播放模式":
        page_play_mode()
    else:
        page_fast_mode()


if __name__ == "__main__":
    main()
