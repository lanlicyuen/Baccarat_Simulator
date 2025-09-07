# 百家乐模拟器 / Baccarat Simulator

一个功能完整的百家乐模拟器，支持策略回测、注码管理和数据分析。  
A comprehensive Baccarat simulator with strategy backtesting, bet management, and data analysis.

![Baccarat Simulator](https://img.shields.io/badge/License-MIT-blue.svg) ![Python](https://img.shields.io/badge/Python-3.10+-green.svg) ![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red.svg)

## ✨ 主要功能 / Key Features

### 🎯 核心功能 / Core Features
- **完整规则实现** / Complete baccarat rules implementation
- **多种下注策略** / Multiple betting strategies (flip-opposite-wait, always-banker, always-player, etc.)
- **连输进阶管理** / Loss progression management with percentage-based increases
- **资金曲线分析** / Bankroll curve analysis and visualization
- **实时数据导出** / Real-time data export (CSV/JSON)

### 🖥️ 用户界面 / User Interface
- **播放模式** / Playback mode: Hand-by-hand visualization with controls
- **极速模式** / Fast mode: Batch simulation with comprehensive reports
- **参数配置** / Parameter configuration with save/load functionality
- **图表分析** / Chart analysis using Altair for smooth visualization

### 📊 数据分析 / Data Analysis
- **胜率统计** / Win rate statistics
- **ROI计算** / ROI calculation with commission
- **流水分析** / Turnover analysis
- **盈亏分布** / Profit/loss distribution charts

## 🚀 快速开始 / Quick Start

### 环境要求 / Requirements
```bash
Python 3.10+
```

### 安装步骤 / Installation

1. **克隆仓库** / Clone repository
```bash
git clone https://github.com/lanlicyuen/Baccarat_Simulator.git
cd Baccarat_Simulator
```

2. **创建虚拟环境** / Create virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

3. **安装依赖** / Install dependencies
```bash
pip install -r requirements.txt
```

4. **配置环境变量** / Configure environment variables
```bash
# 复制环境变量模板 / Copy environment template
cp .env.example .env

# 编辑 .env 文件，设置你的密码 / Edit .env file to set your password
# ACCESS_PASSWORD=your_secure_password_here
```

5. **启动应用** / Run application
```bash
streamlit run app.py
```

6. **访问界面** / Access interface
```bash
浏览器打开: http://localhost:8501
Browser: http://localhost:8501
```

## � 安全配置 / Security Configuration

### 密码设置 / Password Setup
出于安全考虑，需要设置访问密码：  
For security reasons, you need to set an access password:

```bash
# 方法1：使用 .env 文件 / Method 1: Using .env file
cp .env.example .env
# 编辑 .env 文件设置 ACCESS_PASSWORD / Edit .env file to set ACCESS_PASSWORD

# 方法2：环境变量 / Method 2: Environment variable
export ACCESS_PASSWORD=your_secure_password_here

# 方法3：Docker Compose / Method 3: Docker Compose
# 编辑 docker-compose.yml 中的 ACCESS_PASSWORD / Edit ACCESS_PASSWORD in docker-compose.yml
```

## �🐳 Docker 部署 / Docker Deployment

### 使用 Docker Compose / Using Docker Compose
```bash
# 设置密码环境变量 / Set password environment variable
export ACCESS_PASSWORD=your_secure_password_here

# 构建并启动 / Build and start
docker-compose up -d

# 访问应用 / Access application
http://localhost:9006
```

### 管理脚本 / Management Script
```bash
# 构建镜像 / Build image
./manage.sh build

# 启动服务 / Start service
./manage.sh start

# 重启服务 / Restart service
./manage.sh restart

# 查看日志 / View logs
./manage.sh logs

# 停止服务 / Stop service
./manage.sh stop
```

## 📖 使用指南 / Usage Guide

### 命令行模式 / CLI Mode
```bash
# 基础模拟 / Basic simulation
python baccarat_sim.py --bankroll 100000 --bet 100 --hands 10000

# 导出数据 / Export data
python baccarat_sim.py --bankroll 100000 --bet 100 --hands 10000 --csv output.csv --json summary.json

# 指定策略 / Specify strategy
python baccarat_sim.py --bankroll 100000 --bet 100 --hands 10000 --strategy always-banker
```

### 网页界面 / Web Interface

#### 播放模式 / Playback Mode
- **逐局观看** / Watch hand by hand
- **暂停/继续** / Pause/Resume controls
- **跳过功能** / Skip options (5 hands, to report)
- **实时图表** / Real-time charts

#### 极速模式 / Fast Mode
- **批量模拟** / Batch simulation
- **完整报告** / Comprehensive reports
- **数据下载** / Data download (CSV/JSON)
- **参数保存** / Parameter save/load

### 策略配置 / Strategy Configuration

#### 下注策略 / Betting Strategies
- `flip-opposite-wait`: 连庄连闲后等待一手再反向下注 / Wait one hand after streaks then bet opposite
- `always-banker`: 永远下注庄家 / Always bet banker
- `always-player`: 永远下注闲家 / Always bet player
- `alternate`: 交替下注 / Alternate betting
- `random`: 随机下注 / Random betting

#### 连输进阶 / Loss Progression
- **百分比增长** / Percentage increase: Each loss increases bet by (1+%)^n
- **起始阈值** / Start threshold: Begin progression after N consecutive losses
- **获胜后模式** / After win mode: Reset to base bet or persist current amount

## 📁 项目结构 / Project Structure

```
Baccarat_Simulator/
├── app.py                    # Streamlit网页界面 / Web interface
├── baccarat_core.py          # 核心引擎 / Core engine
├── baccarat_sim.py           # 命令行工具 / CLI tool
├── requirements.txt          # Python依赖 / Dependencies
├── Dockerfile               # Docker镜像配置 / Docker config
├── docker-compose.yml       # Docker编排 / Docker compose
├── manage.sh               # 管理脚本 / Management script
└── README.md               # 项目说明 / Documentation
```

## 📊 数据输出 / Data Output

### CSV 格式 / CSV Format
逐局详细数据包含以下字段：  
Detailed hand-by-hand data includes:

```
timestamp, hand_no, bet_side, bet_amount, player_cards, banker_cards,
player_total, banker_total, outcome, win_amount, bankroll_after,
shoe_cards_left, commission_paid, cumulative_win
```

### JSON 格式 / JSON Format
汇总统计数据包含：  
Summary statistics include:

- 初始/最终资金 / Initial/Final bankroll
- 总收益/ROI / Total profit/ROI  
- 胜率统计 / Win rate statistics
- 流水分析 / Turnover analysis
- 策略表现 / Strategy performance

## 🔧 配置选项 / Configuration Options

### 游戏设置 / Game Settings
- **副牌数量** / Number of decks: 6 or 8
- **渗透阈值** / Penetration threshold: Cards remaining before shuffle
- **佣金率** / Commission rate: 5% on banker wins

### 模拟参数 / Simulation Parameters
- **初始资金** / Initial bankroll: Starting amount
- **基础注码** / Base bet: Basic bet amount
- **总局数** / Total hands: Number of hands to simulate
- **随机种子** / Random seed: For reproducible results

## 🛠️ 开发 / Development

### 本地开发 / Local Development
```bash
# 克隆项目 / Clone project
git clone https://github.com/lanlicyuen/Baccarat_Simulator.git
cd Baccarat_Simulator

# 安装开发依赖 / Install dev dependencies
pip install -r requirements.txt

# 运行测试 / Run tests
python baccarat_sim.py --test

# 启动开发服务器 / Start dev server
streamlit run app.py --server.runOnSave true
```

### 贡献指南 / Contributing
1. Fork 项目 / Fork the project
2. 创建功能分支 / Create feature branch (`git checkout -b feature/AmazingFeature`)
3. 提交更改 / Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 / Push to branch (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request / Open a Pull Request

## 📄 许可证 / License

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。  
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 支持 / Support

如果这个项目对你有帮助，请给它一个 ⭐️！  
If this project helps you, please give it a ⭐️!

### 问题反馈 / Issue Reporting
- 发现 Bug？请提交 [Issue](https://github.com/lanlicyuen/Baccarat_Simulator/issues)
- Found a bug? Please submit an [Issue](https://github.com/lanlicyuen/Baccarat_Simulator/issues)

### 联系方式 / Contact
- 项目维护者 / Project Maintainer: [lanlicyuen](https://github.com/lanlicyuen)

## ⚠️ 免责声明 / Disclaimer

本项目仅用于教育和研究目的。请遵守当地法律法规，理性对待博彩活动。  
This project is for educational and research purposes only. Please comply with local laws and regulations, and approach gambling responsibly.

---

**开始你的百家乐策略研究之旅！**  
**Start your Baccarat strategy research journey!**
