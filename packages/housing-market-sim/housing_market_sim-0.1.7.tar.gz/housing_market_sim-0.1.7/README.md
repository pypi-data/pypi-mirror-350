# 🏠 housing_market_sim

**housing_market_sim** 是一个基于 Agent-Based Modeling（ABM） 和 Streamlit 构建的住房市场动态仿真平台。它用于模拟住房过滤行为、评估政策干预情景，并结合 LLM（大语言模型）生成多角色结构性总结，适用于政策分析、学术研究和教学演示。

---

## 🔧 核心功能 Features

- ✅ 基于 ABM 实现住房市场微观仿真
- ✅ 支持三类政策情景：
  - 基准市场（Baseline Scenario）
  - 信贷刺激（Credit Stimulus Scenario）
  - 财政补贴（Fiscal Subsidy Scenario）
- ✅ 可视化市场演化过程：
  - 新房 / 二手房 / 租赁交易趋势
  - 住房质量变化
  - 群体结构变化
- ✅ 嵌入大语言模型分析：
  - 支持 GPT 模型（需 API Key）
  - 支持本地 fallback 总结
  - 三种总结角色：政策制定者、监管者、分析师
- ✅ 中英文界面一键切换
- ✅ 支持图表导出、参数调节、随机种子控制

---

## 📦 安装 Installation

```bash
pip install housing_market_sim
```

---

## 🚀 使用方法 Usage
推荐终端直接运行

```bash
streamlit run housing_market_sim/app.py
```


运行后浏览器将自动打开 Streamlit 应用（默认：http://localhost:8501）。

---

## 📂 目录结构 Project Structure

```
housing_market_sim/
├── app.py                # 主入口（运行 Streamlit）
├── static_summaries.py   # 静态总结模块
├── assets/               # 页面图标资源
├── setup.py              # pip 安装配置
├── requirements.txt      # 依赖声明
├── MANIFEST.in           # 包含静态文件配置
└── README.md             # 当前文件
```

---

## 🧠 LLM 模型说明

- ✅ 可输入 OpenAI API Key，启用 GPT 模型（支持 GPT-4、GPT-4o）
- ✅ 若未输入 Key，自动使用本地静态总结（来自 `static_summaries.py`）
- ✅ 支持三种总结风格：
  - **政策制定者（Policymaker）**：关注供给结构、补贴投放、金融规则
  - **市场监管者（Regulator）**：关注中介、信息透明与风险控制
  - **分析师 / 研究者（Analyst）**：提供指标设计与结构评估

---

## 🧪 本地运行与调试 Local Dev

```bash
streamlit run housing_market_sim/app.py
```

```bash
pip install build
python -m build
```

```bash
pip install dist/housing_market_sim-*.whl
```

---

## 📋 项目依赖 Requirements

```text
streamlit>=1.0
mesa
openai
matplotlib
numpy
```

---

## 📄 License

本项目采用 MIT License 开源，允许自由使用、修改、发布，但请注明原始作者。

---

## 👤 作者 Author

- 开发者：Your Name  
- 邮箱：your_email@example.com  
- GitHub: https://github.com/your_account/housing-market-sim
