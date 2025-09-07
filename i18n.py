# 多语言配置 / Multi-language Configuration
# 支持的语言 / Supported Languages

LANGUAGES = {
    "en": {
        "name": "🇺🇸 English",
        "code": "en",
        "translations": {
            # 通用 / Common
            "baccarat_simulator": "Baccarat Simulator",
            "login_system": "🚪 Logout",
            "mode": "Mode",
            "playback_mode": "Playback Mode",
            "fast_mode": "Fast Mode",
            "language": "🌐 Language",
            
            # 登录页面 / Login Page
            "login_title": "Welcome to Baccarat Simulator",
            "login_subtitle": "✨ Please enter access password to continue ✨",
            "password_placeholder": "Enter password...",
            "login_button": "🚀 Enter System",
            "password_error": "❌ Incorrect password, please try again",
            "password_warning": "⚠️ Multiple failed attempts, please check your password",
            
            # 播放模式 / Playback Mode
            "game_settings": "🎮 Game Settings",
            "initial_bankroll": "Initial Bankroll",
            "bet_amount": "Bet Amount", 
            "total_hands": "Total Hands",
            "number_of_decks": "Number of Decks",
            "penetration_threshold": "Penetration Threshold",
            "betting_strategy": "Betting Strategy",
            "random_seed": "Random Seed (Optional)",
            
            # 连输设置 / Loss Progression
            "loss_progression": "🔄 Loss Progression Settings",
            "loss_increase_pct": "Loss Increase (%)",
            "loss_start_threshold": "Start After N Losses",
            "loss_win_mode": "After Win Mode",
            "reset": "Reset",
            "persist": "Persist",
            "ignore": "Ignore",
            
            # 连赢设置 / Win Progression  
            "win_progression": "🎯 Win Progression Settings",
            "win_increase_pct": "Win Increase (%)",
            "win_decrease_pct": "Win Decrease (%)", 
            "win_start_threshold": "Start After N Wins",
            "win_loss_mode": "After Loss Mode",
            
            # 控制按钮 / Control Buttons
            "start": "▶️ Start",
            "pause": "⏸️ Pause", 
            "resume": "▶️ Resume",
            "next": "⏭️ Next",
            "skip_5": "⏩ Skip 5",
            "skip_to_report": "📊 Skip to Report",
            "reset_game": "🔄 Reset",
            
            # 统计信息 / Statistics
            "current_stats": "📊 Current Statistics",
            "hand_number": "Hand",
            "current_bankroll": "Current Bankroll",
            "total_profit": "Total Profit",
            "win_rate": "Win Rate",
            "roi": "ROI",
            "commission": "Commission",
            "turnover": "Turnover",
            "rebate": "Rebate",
            "net_roi": "Net ROI",
            
            # 图表 / Charts
            "bankroll_chart": "💰 Bankroll Curve",
            "profit_distribution": "📈 Profit Distribution",
            
            # 极速模式 / Fast Mode
            "batch_simulation": "⚡ Batch Simulation",
            "run_simulation": "🚀 Run Simulation",
            "download_csv": "📥 Download CSV",
            "download_json": "📥 Download JSON",
            "save_settings": "💾 Save Settings",
            "load_settings": "📂 Load Settings",
            "auto_run_after_load": "🔄 Auto-run after load",
            
            # 设置保存/加载 / Settings Save/Load
            "settings_management": "⚙️ Settings Management",
            "settings_saved": "✅ Settings saved successfully!",
            "settings_loaded": "✅ Settings loaded successfully!",
            "settings_load_error": "❌ Error loading settings",
            
            # 策略选项 / Strategy Options
            "flip_opposite_wait": "Flip Opposite Wait",
            "always_banker": "Always Banker",
            "always_player": "Always Player", 
            "alternate": "Alternate",
            "random": "Random",
            
            # 结果报告 / Results Report
            "simulation_results": "🎯 Simulation Results",
            "final_bankroll": "Final Bankroll",
            "total_hands_played": "Total Hands Played",
            "hands_bet": "Hands Bet",
            "hands_observed": "Hands Observed",
            "ties": "Ties",
            "wins": "Wins",
            "losses": "Losses",
            "banker_wins": "Banker Wins",
            "player_wins": "Player Wins",
            "total_commission": "Total Commission",
            "strategy_hit_rate": "Strategy Hit Rate",
        }
    },
    
    "zh-CN": {
        "name": "🇨🇳 简体中文",
        "code": "zh-CN", 
        "translations": {
            # 通用 / Common
            "baccarat_simulator": "百家乐模拟器",
            "login_system": "🚪 登出系统",
            "mode": "模式",
            "playback_mode": "播放模式",
            "fast_mode": "极速模式", 
            "language": "🌐 语言",
            
            # 登录页面
            "login_title": "欢迎使用百家乐模拟器",
            "login_subtitle": "✨ 请输入访问密码以继续 ✨",
            "password_placeholder": "请输入密码...",
            "login_button": "🚀 进入系统",
            "password_error": "❌ 密码错误，请重新输入",
            "password_warning": "⚠️ 多次输入错误，请检查密码",
            
            # 播放模式
            "game_settings": "🎮 游戏设置",
            "initial_bankroll": "初始资金",
            "bet_amount": "下注金额",
            "total_hands": "总局数", 
            "number_of_decks": "副牌数",
            "penetration_threshold": "渗透阈值",
            "betting_strategy": "下注策略",
            "random_seed": "随机种子(可选)",
            
            # 连输设置
            "loss_progression": "🔄 连输进阶设置",
            "loss_increase_pct": "连输加注(%)",
            "loss_start_threshold": "从第几次连输开始",
            "loss_win_mode": "赢后注码模式",
            "reset": "重置",
            "persist": "保持",
            "ignore": "忽略",
            
            # 连赢设置
            "win_progression": "🎯 连赢进阶设置", 
            "win_increase_pct": "连赢加注(%)",
            "win_decrease_pct": "连赢减注(%)",
            "win_start_threshold": "从第几次连赢开始",
            "win_loss_mode": "输后注码模式",
            
            # 控制按钮
            "start": "▶️ 开始",
            "pause": "⏸️ 暂停",
            "resume": "▶️ 继续", 
            "next": "⏭️ 下一局",
            "skip_5": "⏩ 跳过5局",
            "skip_to_report": "📊 跳到报告",
            "reset_game": "🔄 重置",
            
            # 统计信息
            "current_stats": "📊 当前统计",
            "hand_number": "第",
            "current_bankroll": "当前资金",
            "total_profit": "总盈亏",
            "win_rate": "胜率",
            "roi": "投资回报率", 
            "commission": "佣金",
            "turnover": "流水",
            "rebate": "返水",
            "net_roi": "含返收益率",
            
            # 图表
            "bankroll_chart": "💰 资金曲线",
            "profit_distribution": "📈 盈亏分布",
            
            # 极速模式
            "batch_simulation": "⚡ 批量模拟",
            "run_simulation": "🚀 运行模拟",
            "download_csv": "📥 下载CSV",
            "download_json": "📥 下载JSON",
            "save_settings": "💾 保存设置",
            "load_settings": "📂 加载设置", 
            "auto_run_after_load": "🔄 加载后自动运行",
            
            # 设置保存/加载
            "settings_management": "⚙️ 设置管理",
            "settings_saved": "✅ 设置保存成功！",
            "settings_loaded": "✅ 设置加载成功！",
            "settings_load_error": "❌ 设置加载出错",
            
            # 策略选项
            "flip_opposite_wait": "反向等待策略",
            "always_banker": "永远押庄",
            "always_player": "永远押闲",
            "alternate": "交替下注",
            "random": "随机下注",
            
            # 结果报告
            "simulation_results": "🎯 模拟结果",
            "final_bankroll": "最终资金",
            "total_hands_played": "总局数",
            "hands_bet": "下注局数",
            "hands_observed": "观望局数", 
            "ties": "和局",
            "wins": "胜局",
            "losses": "败局", 
            "banker_wins": "庄胜",
            "player_wins": "闲胜",
            "total_commission": "总佣金",
            "strategy_hit_rate": "策略命中率",
        }
    },
    
    "zh-TW": {
        "name": "🇹🇼 繁體中文",
        "code": "zh-TW",
        "translations": {
            # 通用
            "baccarat_simulator": "百家樂模擬器",
            "login_system": "🚪 登出系統",
            "mode": "模式",
            "playback_mode": "播放模式", 
            "fast_mode": "極速模式",
            "language": "🌐 語言",
            
            # 登錄頁面
            "login_title": "歡迎使用百家樂模擬器",
            "login_subtitle": "✨ 請輸入訪問密碼以繼續 ✨",
            "password_placeholder": "請輸入密碼...",
            "login_button": "🚀 進入系統",
            "password_error": "❌ 密碼錯誤，請重新輸入",
            "password_warning": "⚠️ 多次輸入錯誤，請檢查密碼",
            
            # 播放模式
            "game_settings": "🎮 遊戲設置",
            "initial_bankroll": "初始資金",
            "bet_amount": "下注金額",
            "total_hands": "總局數",
            "number_of_decks": "副牌數",
            "penetration_threshold": "滲透閾值", 
            "betting_strategy": "下注策略",
            "random_seed": "隨機種子(可選)",
            
            # 連輸設置
            "loss_progression": "🔄 連輸進階設置",
            "loss_increase_pct": "連輸加注(%)",
            "loss_start_threshold": "從第幾次連輸開始",
            "loss_win_mode": "贏後注碼模式",
            "reset": "重置",
            "persist": "保持",
            "ignore": "忽略",
            
            # 連贏設置
            "win_progression": "🎯 連贏進階設置",
            "win_increase_pct": "連贏加注(%)",
            "win_decrease_pct": "連贏減注(%)",
            "win_start_threshold": "從第幾次連贏開始", 
            "win_loss_mode": "輸後注碼模式",
            
            # 控制按鈕
            "start": "▶️ 開始",
            "pause": "⏸️ 暫停",
            "resume": "▶️ 繼續",
            "next": "⏭️ 下一局",
            "skip_5": "⏩ 跳過5局",
            "skip_to_report": "📊 跳到報告",
            "reset_game": "🔄 重置",
            
            # 統計信息
            "current_stats": "📊 當前統計",
            "hand_number": "第",
            "current_bankroll": "當前資金",
            "total_profit": "總盈虧",
            "win_rate": "勝率",
            "roi": "投資回報率",
            "commission": "佣金", 
            "turnover": "流水",
            "rebate": "返水",
            "net_roi": "含返收益率",
            
            # 圖表
            "bankroll_chart": "💰 資金曲線",
            "profit_distribution": "📈 盈虧分佈",
            
            # 極速模式
            "batch_simulation": "⚡ 批量模擬",
            "run_simulation": "🚀 運行模擬",
            "download_csv": "📥 下載CSV",
            "download_json": "📥 下載JSON",
            "save_settings": "💾 保存設置",
            "load_settings": "📂 加載設置",
            "auto_run_after_load": "🔄 加載後自動運行",
            
            # 設置保存/加載
            "settings_management": "⚙️ 設置管理",
            "settings_saved": "✅ 設置保存成功！",
            "settings_loaded": "✅ 設置加載成功！", 
            "settings_load_error": "❌ 設置加載出錯",
            
            # 策略選項
            "flip_opposite_wait": "反向等待策略",
            "always_banker": "永遠押莊",
            "always_player": "永遠押閒",
            "alternate": "交替下注",
            "random": "隨機下注",
            
            # 結果報告
            "simulation_results": "🎯 模擬結果",
            "final_bankroll": "最終資金",
            "total_hands_played": "總局數",
            "hands_bet": "下注局數",
            "hands_observed": "觀望局數",
            "ties": "和局",
            "wins": "勝局",
            "losses": "敗局",
            "banker_wins": "莊勝",
            "player_wins": "閒勝",
            "total_commission": "總佣金",
            "strategy_hit_rate": "策略命中率",
        }
    },
    
    "ja": {
        "name": "🇯🇵 日本語",
        "code": "ja",
        "translations": {
            # 通用
            "baccarat_simulator": "バカラシミュレーター",
            "login_system": "🚪 ログアウト",
            "mode": "モード",
            "playback_mode": "再生モード",
            "fast_mode": "高速モード",
            "language": "🌐 言語",
            
            # ログインページ
            "login_title": "バカラシミュレーターへようこそ",
            "login_subtitle": "✨ 続行するにはアクセスパスワードを入力してください ✨",
            "password_placeholder": "パスワードを入力...",
            "login_button": "🚀 システムに入る",
            "password_error": "❌ パスワードが間違っています。もう一度入力してください",
            "password_warning": "⚠️ 複数回の失敗、パスワードを確認してください",
            
            # 再生モード
            "game_settings": "🎮 ゲーム設定",
            "initial_bankroll": "初期資金",
            "bet_amount": "ベット額",
            "total_hands": "総ゲーム数",
            "number_of_decks": "デッキ数",
            "penetration_threshold": "ペネトレーション閾値",
            "betting_strategy": "ベット戦略",
            "random_seed": "ランダムシード（オプション）",
            
            # 連敗設定
            "loss_progression": "🔄 連敗プログレッション設定",
            "loss_increase_pct": "連敗時増加（%）",
            "loss_start_threshold": "何回目の連敗から開始",
            "loss_win_mode": "勝利後のベットモード",
            "reset": "リセット",
            "persist": "維持",
            "ignore": "無視",
            
            # 連勝設定
            "win_progression": "🎯 連勝プログレッション設定",
            "win_increase_pct": "連勝時増加（%）",
            "win_decrease_pct": "連勝時減少（%）",
            "win_start_threshold": "何回目の連勝から開始",
            "win_loss_mode": "敗北後のベットモード",
            
            # 制御ボタン
            "start": "▶️ スタート",
            "pause": "⏸️ 一時停止",
            "resume": "▶️ 再開",
            "next": "⏭️ 次へ",
            "skip_5": "⏩ 5回スキップ",
            "skip_to_report": "📊 レポートへスキップ",
            "reset_game": "🔄 リセット",
            
            # 統計情報
            "current_stats": "📊 現在の統計",
            "hand_number": "第",
            "current_bankroll": "現在の資金",
            "total_profit": "総損益",
            "win_rate": "勝率",
            "roi": "投資収益率",
            "commission": "手数料",
            "turnover": "取引高",
            "rebate": "リベート",
            "net_roi": "実質収益率",
            
            # チャート
            "bankroll_chart": "💰 資金カーブ",
            "profit_distribution": "📈 損益分布",
            
            # 高速モード
            "batch_simulation": "⚡ バッチシミュレーション",
            "run_simulation": "🚀 シミュレーション実行",
            "download_csv": "📥 CSV ダウンロード",
            "download_json": "📥 JSON ダウンロード",
            "save_settings": "💾 設定保存",
            "load_settings": "📂 設定読込",
            "auto_run_after_load": "🔄 読込後自動実行",
            
            # 設定保存/読込
            "settings_management": "⚙️ 設定管理",
            "settings_saved": "✅ 設定が正常に保存されました！",
            "settings_loaded": "✅ 設定が正常に読み込まれました！",
            "settings_load_error": "❌ 設定の読み込みエラー",
            
            # 戦略オプション
            "flip_opposite_wait": "フリップ反対待機",
            "always_banker": "常にバンカー",
            "always_player": "常にプレイヤー",
            "alternate": "交互",
            "random": "ランダム",
            
            # 結果レポート
            "simulation_results": "🎯 シミュレーション結果",
            "final_bankroll": "最終資金",
            "total_hands_played": "総プレイ数",
            "hands_bet": "ベット数",
            "hands_observed": "観察数",
            "ties": "引き分け",
            "wins": "勝利",
            "losses": "敗北",
            "banker_wins": "バンカー勝利",
            "player_wins": "プレイヤー勝利",
            "total_commission": "総手数料",
            "strategy_hit_rate": "戦略的中率",
        }
    },
    
    "ko": {
        "name": "🇰🇷 한국어",
        "code": "ko",
        "translations": {
            # 공통
            "baccarat_simulator": "바카라 시뮬레이터",
            "login_system": "🚪 로그아웃",
            "mode": "모드",
            "playback_mode": "재생 모드",
            "fast_mode": "고속 모드",
            "language": "🌐 언어",
            
            # 로그인 페이지
            "login_title": "바카라 시뮬레이터에 오신 것을 환영합니다",
            "login_subtitle": "✨ 계속하려면 액세스 비밀번호를 입력하세요 ✨",
            "password_placeholder": "비밀번호 입력...",
            "login_button": "🚀 시스템 진입",
            "password_error": "❌ 비밀번호가 틀렸습니다. 다시 입력해주세요",
            "password_warning": "⚠️ 여러 번 실패했습니다. 비밀번호를 확인해주세요",
            
            # 재생 모드
            "game_settings": "🎮 게임 설정",
            "initial_bankroll": "초기 자금",
            "bet_amount": "베팅 금액",
            "total_hands": "총 게임 수",
            "number_of_decks": "덱 수",
            "penetration_threshold": "침투 임계값",
            "betting_strategy": "베팅 전략",
            "random_seed": "랜덤 시드 (선택사항)",
            
            # 연패 설정
            "loss_progression": "🔄 연패 프로그레션 설정",
            "loss_increase_pct": "연패시 증가(%)",
            "loss_start_threshold": "몇 번째 연패부터 시작",
            "loss_win_mode": "승리 후 베팅 모드",
            "reset": "리셋",
            "persist": "유지",
            "ignore": "무시",
            
            # 연승 설정
            "win_progression": "🎯 연승 프로그레션 설정",
            "win_increase_pct": "연승시 증가(%)",
            "win_decrease_pct": "연승시 감소(%)",
            "win_start_threshold": "몇 번째 연승부터 시작",
            "win_loss_mode": "패배 후 베팅 모드",
            
            # 제어 버튼
            "start": "▶️ 시작",
            "pause": "⏸️ 일시정지",
            "resume": "▶️ 재개",
            "next": "⏭️ 다음",
            "skip_5": "⏩ 5개 건너뛰기",
            "skip_to_report": "📊 보고서로 건너뛰기",
            "reset_game": "🔄 리셋",
            
            # 통계 정보
            "current_stats": "📊 현재 통계",
            "hand_number": "제",
            "current_bankroll": "현재 자금",
            "total_profit": "총 손익",
            "win_rate": "승률",
            "roi": "투자수익률",
            "commission": "수수료",
            "turnover": "거래량",
            "rebate": "리베이트",
            "net_roi": "실질 수익률",
            
            # 차트
            "bankroll_chart": "💰 자금 곡선",
            "profit_distribution": "📈 손익 분포",
            
            # 고속 모드
            "batch_simulation": "⚡ 일괄 시뮬레이션",
            "run_simulation": "🚀 시뮬레이션 실행",
            "download_csv": "📥 CSV 다운로드",
            "download_json": "📥 JSON 다운로드",
            "save_settings": "💾 설정 저장",
            "load_settings": "📂 설정 로드",
            "auto_run_after_load": "🔄 로드 후 자동 실행",
            
            # 설정 저장/로드
            "settings_management": "⚙️ 설정 관리",
            "settings_saved": "✅ 설정이 성공적으로 저장되었습니다!",
            "settings_loaded": "✅ 설정이 성공적으로 로드되었습니다!",
            "settings_load_error": "❌ 설정 로드 오류",
            
            # 전략 옵션
            "flip_opposite_wait": "플립 반대 대기",
            "always_banker": "항상 뱅커",
            "always_player": "항상 플레이어",
            "alternate": "교대",
            "random": "랜덤",
            
            # 결과 보고서
            "simulation_results": "🎯 시뮬레이션 결과",
            "final_bankroll": "최종 자금",
            "total_hands_played": "총 플레이 수",
            "hands_bet": "베팅 수",
            "hands_observed": "관찰 수",
            "ties": "무승부",
            "wins": "승리",
            "losses": "패배",
            "banker_wins": "뱅커 승리",
            "player_wins": "플레이어 승리",
            "total_commission": "총 수수료",
            "strategy_hit_rate": "전략 적중률",
        }
    }
}

def get_language():
    """获取当前选择的语言"""
    return st.session_state.get("selected_language", "en")

def set_language(lang_code):
    """设置语言"""
    st.session_state.selected_language = lang_code

def t(key, default=None):
    """翻译函数 - 获取当前语言的翻译文本"""
    lang = get_language()
    try:
        return LANGUAGES[lang]["translations"].get(key, default or key)
    except KeyError:
        return default or key

def render_language_selector():
    """渲染语言选择器"""
    current_lang = get_language()
    
    # 创建语言选项
    language_options = []
    language_mapping = {}
    
    for lang_code, lang_info in LANGUAGES.items():
        display_name = lang_info["name"]
        language_options.append(display_name)
        language_mapping[display_name] = lang_code
    
    # 找到当前语言的显示名称
    current_display = None
    for display_name, code in language_mapping.items():
        if code == current_lang:
            current_display = display_name
            break
    
    # 语言选择框
    selected_display = st.selectbox(
        t("language"),
        options=language_options,
        index=language_options.index(current_display) if current_display else 0,
        key="language_selector"
    )
    
    # 如果语言改变，更新并重新运行
    selected_code = language_mapping[selected_display]
    if selected_code != current_lang:
        set_language(selected_code)
        st.rerun()
