import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import socket
# 🔵 import区增加 openai (如果暂时没有，可以先注释)
import openai
from openai import OpenAI
import io
from io import BytesIO
import uuid  # 在文件开头统一import
import base64
# ✅ 引入静态建议模块（顶部已导入）
from static_summaries import STATIC_RECOMMENDATIONS_ZH, STATIC_RECOMMENDATIONS_EN


# ✅ 手动设定默认语言
DEFAULT_LANGUAGE = "English"  # 或改为 "中文"

# ✅ 语言对应标题
page_title = (
    "住房过滤动态仿真（ABM）"
    if DEFAULT_LANGUAGE == "中文"
    else "Dynamic Housing Filtering Simulation (ABM)"
)

# ✅ 设置 favicon 和标题
st.set_page_config(
    page_title=page_title,
    page_icon="assets/home_icon.png",
    layout="wide"
)

if "language" not in st.session_state:
    st.session_state.language = DEFAULT_LANGUAGE

def setup_language():
    if "language" not in st.session_state:
        st.session_state.language = "English"  # 默认语言

    current_language = st.session_state.language

    # 👇 对应语言标签和选项显示
    if current_language == "中文":
        label = "选择语言"
        display_names = ["中文", "英文"]
    else:
        label = "Select Language"
        display_names = ["Chinese", "English"]

    # ✅ 映射 display ➜ value
    internal_values = ["中文", "English"]
    value_to_display = dict(zip(internal_values, display_names))
    display_to_value = dict(zip(display_names, internal_values))

    default_index = internal_values.index(current_language)

    with st.sidebar:
        selected_display = st.selectbox(label, display_names, index=default_index)

    selected_value = display_to_value[selected_display]

    if selected_value != current_language:
        st.session_state.language = selected_value
        st.rerun()

    language = st.session_state.language
    lang = translations[language]
    return language, lang


def img_to_base64(path: str) -> str:
    """读取本地文件并返回符合 <img src="…"> 的 Base64 URL"""
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:image/png;base64,{b64}"



# ========== 页面配置 & 中文字体 ==========

# 先把你要用的图标读成 Base64 URL
try:
    home_b64 = img_to_base64("assets/home_icon.png")
    key_b64 = img_to_base64("assets/key_icon.png")
    visual_b64 = img_to_base64("assets/visualization_icon.png")
    llm_b64 = img_to_base64("assets/llm_icon.png")
except Exception as e:
    st.warning(f"❌ 图标加载失败：{str(e)}")

#下拉框的字体大小和高度选择
st.markdown("""
    <style>
    div[data-baseweb="select"] > div {
        font-size: 13px;
        height: 35px;
    }
    button[kind="primary"] {
        display: none; /* 隐藏默认streamlit按钮 */
    }
    .save-icon-button {
        font-size: 16px;
        margin-left: 4px;
        margin-top: -8px;
        cursor: pointer;
        text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

plt.rcParams["axes.unicode_minus"] = False
try:
    plt.rcParams["font.sans-serif"] = ["SimHei"]
except:
    pass

# ========== 多语言支持 ==========

translations = {
    "English": {
        "title": '<img src="{home_b64}" width="56" style="vertical-align: middle; margin-right: 5px;"> ABM-Based Dynamic Housing Filtering Simulation',
        "key_variables": '<img src="{key_b64}" width="40" style="vertical-align: middle; margin-right: 5px;"> Model Parameter Tuning Panel',
        "visualization_title": '<img src="{visual_b64}" width="44" style="vertical-align: middle; margin-right: 5px;"> Visualization of Housing Filtering Behaviors',
        "llm_summary_analysis": '<img src="{llm_b64}" width="56" style="vertical-align: middle; margin-right: 5px;"> LLM-Aided Summary',
        "run": "Go",
        "price_to_income_ratio": "Price-to-Income Ratio",
        "income_growth": "Income Growth (%)",
        "loan_rate": "Loan Rate (%)",
        "down_payment_ratio": "Down Payment Ratio (%)",
        "government_subsidy": "Government Subsidy (%)",
        "secondary_tax": "Secondary Housing Transaction Tax (%)",
        "market_liquidity": "Market Liquidity (%)",
        "resale_price_ratio": "Resale Price-to-Income Ratio",
        "housing_stock_ratio": "Housing Stock-to-Family Ratio",
        "new_home_market": "New Home Activity",
        "secondary_market": "Secondary Market Activity",
        "rental_market": "Rental Market Activity",
        "high_income_swaps": "High-Income Replacement Count",
        "upgrade_swaps": "Low-/Middle-Income Replacement Count",
        "avg_quality": "Average House Quality",
        "low_quality_ratio": "Low-Quality Ratio",
        "supply": "Supply",
        "demand": "Demand",
        "pop_high": "High Income Count",
        "pop_mid": "Middle Income Count",
        "pop_low": "Low Income Count",
        "step_length": "Time Steps",
        "transactions": "Transactions",
        "population_structure": "Population Structure",
        "color_legend_label": "📌 Color Legend:",
        "color_legend": {
            "red": "Low-income homeowner",
            "Lightcoral": "Low-income renter",
            "green": "Middle-income homeowner",
            "Lightgreen": "Middle-income renter",
            "blue": "High-income homeowner",
            "black": "New houses"
        },
        "scenario_selection": "Select Scenario",
        "baseline_scenario": "Baseline Scenario",
        "credit_stimulus_scenario": "Credit Stimulus Scenario",
        "fiscal_subsidy_scenario": "Fiscal Subsidy Scenario",
        "summary_analysis": "Summary Analysis",
        "generate_summary": "Generate Simulation Summary",
        "summary_history": "Summary History",
        "clear_summary_history": "Clear Summary History",
        "local_fallback_warning": "⚠️ Unable to connect to OpenAI, using local summary.",
        "transaction_trend": "Fig.1 Trends in Housing Market Activity",
        "swap_trend": "Fig.2 Changes in Housing Transaction Behavior",
        "housing_quality_trend": "Fig.3 Trends in Housing Quality",
        "population_structure_change": "Fig.4 Changes in Population Structure of the Housing Market",
        "save_image": "Save Image",
        "pop_high_owner": "High-Income Owner",
        "pop_mid_owner": "Middle-Income Owner",
        "pop_mid_renter": "Middle-Income Renter",
        "pop_low_owner": "Low-Income Owner",
        "pop_low_renter": "Low-Income Renter",
        "pop_structure_title": "Population Structure Change",
        "pop_structure_xlabel": "Time Steps",
        "pop_structure_ylabel": "Population Structure",
        "pop_structure_legend": "Population Structure"
    },
    "中文": {
        "title": '<img src="{home_b64}" width="56" style="vertical-align: middle; margin-right: 5px;"> 基于ABM的住房过滤动态仿真',
        "key_variables": '<img src="{key_b64}" width="40" style="vertical-align: middle; margin-right: 5px;"> 模型参数调优面板',
        "visualization_title": '<img src="{visual_b64}" width="44" style="vertical-align: middle; margin-right: 5px;"> 住房过滤行为可视化',
        "llm_summary_analysis": '<img src="{llm_b64}" width="56" style="vertical-align: middle; margin-right: 5px;"> 大语言模型智能总结',
        "run": "运行",
        "price_to_income_ratio": "房价收入比",
        "income_growth": "收入增速 (%)",
        "loan_rate": "贷款利率 (%)",
        "down_payment_ratio": "首付比例 (%)",
        "government_subsidy": "购房补贴 (%)",
        "secondary_tax": "二手房交易税 (%)",
        "market_liquidity": "市场流动性 (%)",
        "resale_price_ratio": "二手房售价/收入比",
        "housing_stock_ratio": "存量住房/家庭比",
        "new_home_market": "新房交易活跃度",
        "secondary_market": "二手房交易活跃度",
        "rental_market": "租赁市场活跃度",
        "high_income_swaps": "高收入置换次数",
        "upgrade_swaps": "中低收入置换次数",
        "avg_quality": "平均住房质量",
        "low_quality_ratio": "低质量占比",
        "supply": "供给量",
        "demand": "需求量",
        "pop_high": "高收入代理数",
        "pop_mid": "中等收入代理数",
        "pop_low": "低收入代理数",
        "step_length": "时间步长",
        "transactions": "交易量",
        "population_structure": "人口结构",
        "color_legend_label": "📌 颜色图例：",
        "color_legend": {
            "red": "低收入有房",
            "Lightcoral": "低收入租房",
            "green": "中等收入有房",
            "Lightgreen": "中等收入租房",
            "blue": "高收入有房",
            "black": "新房"
        },
        "scenario_selection": "选择情景",
        "baseline_scenario": "基准情景",
        "credit_stimulus_scenario": "信贷刺激情景",
        "fiscal_subsidy_scenario": "财政补贴情景",
        "summary_analysis": "总结分析",
        "generate_summary": "生成模拟总结",
        "summary_history": "总结历史记录",
        "clear_summary_history": "清空总结历史",
        "local_fallback_warning": "⚠️ 无法连接OpenAI，使用本地总结。",
        "transaction_trend": "图1 住房市场活跃度趋势图",
        "swap_trend": "图2 住房交易行为变化图",
        "housing_quality_trend": "图3 住房质量变化趋势图",
        "population_structure_change": "图4 住房市场人口结构变化图",
        "save_image": "保存图",
        "pop_high_owner": "高收入有房",
        "pop_mid_owner": "中等收入有房",
        "pop_mid_renter": "中等收入租房",
        "pop_low_owner": "低收入有房",
        "pop_low_renter": "低收入租房",
        "pop_structure_title": "人口结构变化",
        "pop_structure_xlabel": "时间步长",
        "pop_structure_ylabel": "人口结构",
        "pop_structure_legend": "人口结构"
    }
}
tooltips = {
    "English": {
        "price_to_income_ratio": "Price-to-Income Ratio (PIR): The ratio of housing prices to household annual income. Higher values indicate greater housing unaffordability.",
        "income_growth": "Income Growth (IG): Annual growth rate of household income. Higher rates enhance purchasing power.",
        "loan_rate": "Loan Rate (LR): Mortgage interest rate. Higher rates increase financing costs and suppress home purchases.",
        "down_payment_ratio": "Down Payment Ratio (DPR): The proportion of down payment to total house price. Higher ratios increase the initial barrier to home ownership.",
        "government_subsidy": "Government Subsidy (GS): Financial assistance provided by the government to support home purchases. Higher subsidies encourage buying.",
        "secondary_tax": "Secondary Housing Transaction Tax (ST): Taxes incurred when buying or selling second-hand houses. Higher taxes reduce market liquidity.",
        "market_liquidity": "Market Liquidity (ML): The ease of buying and selling houses in the secondary market. Higher liquidity fosters more frequent transactions.",
        "resale_price_ratio": "Resale Price-to-Income Ratio (RPR): The ratio of resale house prices to household income. Higher ratios imply greater difficulty in affording second-hand homes.",
        "housing_stock_ratio": "Housing Stock-to-Family Ratio (HSR): The total housing stock divided by the number of households. Higher ratios indicate oversupply, easing purchase pressure."
    },
    "中文": {
        "price_to_income_ratio": "房价收入比（PIR）：住房价格与家庭年收入之比，越高表明购房压力越大。",
        "income_growth": "收入增速（IG）：家庭年收入的年增长率，增长越快支付能力越强。",
        "loan_rate": "贷款利率（LR）：购房贷款利率，利率越高贷款负担越重，购房意愿下降。",
        "down_payment_ratio": "首付比例（DPR）：首付款占房价的比例，比例越高购房初期门槛越高。",
        "government_subsidy": "购房补贴（GS）：政府给予购房者的资金支持，补贴越高越促进购房。",
        "secondary_tax": "二手房交易税（ST）：二手房交易时需支付的税率，税负越高交易活跃度下降。",
        "market_liquidity": "市场流动性（ML）：二手房买卖的便利程度，流动性越高交易越频繁。",
        "resale_price_ratio": "二手房售价/收入比（RPR）：二手房价格与家庭收入的比值，越高表示二手房购买难度增大。",
        "housing_stock_ratio": "存量住房/家庭比（HSR）：城市住房存量与家庭数量之比，越高说明供应充足，有助于缓解购房压力。"
    }
}


language, lang = setup_language()

# ✅ 在读取 base64 后立即替换字符串中的变量
# ✅ 替换含图标的字段，统一放大图标尺寸
for lang_key in translations:
    # 修改图标宽度为 28 像素
    translations[lang_key]["title"] = translations[lang_key]["title"].replace('width="20"', 'width="32"').format(
        home_b64=home_b64, key_b64=key_b64, visual_b64=visual_b64, llm_b64=llm_b64)
    translations[lang_key]["key_variables"] = translations[lang_key]["key_variables"].replace('width="18"', 'width="28"').format(
        home_b64=home_b64, key_b64=key_b64, visual_b64=visual_b64, llm_b64=llm_b64)
    translations[lang_key]["visualization_title"] = translations[lang_key]["visualization_title"].replace('width="18"', 'width="28"').format(
        home_b64=home_b64, key_b64=key_b64, visual_b64=visual_b64, llm_b64=llm_b64)
    translations[lang_key]["llm_summary_analysis"] = translations[lang_key]["llm_summary_analysis"].replace('width="18"', 'width="28"').format(
        home_b64=home_b64, key_b64=key_b64, visual_b64=visual_b64, llm_b64=llm_b64)


# ✅ 在这里初始化 session_state 变量
if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""

# ========== 再绘制标题 ==========
st.markdown(f"<h1>{lang['title']}</h1>", unsafe_allow_html=True)

# ========== 初始化状态 ==========
if "show_api_prompt" not in st.session_state:
    st.session_state.show_api_prompt = False
if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""

# ========== 选择情景 ==========
scenario = st.sidebar.selectbox(
    lang["scenario_selection"],
    (lang["baseline_scenario"], lang["credit_stimulus_scenario"], lang["fiscal_subsidy_scenario"])
)
# 初始化默认参数（基准情景）
pir_default = 18
ig_default = 3.0
lr_default = 5.0
dpr_default = 30
gs_default = 5
stx_default = 5
ml_default = 50
rpr_default = 3.5
hsr_default = 2.5

# 根据情景切换调整默认参数
if scenario == lang["credit_stimulus_scenario"]:
    # 信贷刺激参数设定
    pir_default = 12
    ig_default = 5.0
    lr_default = 3.0
    dpr_default = 15
    gs_default = 0
    stx_default = 3
    ml_default = 80
    rpr_default = 2.5
    hsr_default = 2.5

elif scenario == lang["fiscal_subsidy_scenario"]:
    # 政府补贴参数设定
    pir_default = 10
    ig_default = 3.0
    lr_default = 5.0
    dpr_default = 30
    gs_default = 20
    stx_default = 1
    ml_default = 80
    rpr_default = 3.2
    hsr_default = 2.5

# ========== 参数表单 ==========
with st.sidebar.form(key="params_form"):
    st.markdown(f"""
        <div style='font-size:22px; font-weight: bold; margin-bottom: 10px;'>
            {lang['key_variables']}
        </div>
    """, unsafe_allow_html=True)

    pir = st.slider(lang["price_to_income_ratio"], 5, 40, pir_default, help=tooltips[language]["price_to_income_ratio"])
    ig = st.slider(lang["income_growth"], -5.0, 10.0, ig_default, help=tooltips[language]["income_growth"])
    lr = st.slider(lang["loan_rate"], 3.0, 8.0, lr_default, help=tooltips[language]["loan_rate"])
    dpr = st.slider(lang["down_payment_ratio"], 10, 50, dpr_default, help=tooltips[language]["down_payment_ratio"])
    gs = st.slider(lang["government_subsidy"], 0, 20, gs_default, help=tooltips[language]["government_subsidy"])
    stx = st.slider(lang["secondary_tax"], 0, 10, stx_default, help=tooltips[language]["secondary_tax"])
    ml = st.slider(lang["market_liquidity"], 0, 100, ml_default, help=tooltips[language]["market_liquidity"])
    rpr = st.slider(lang["resale_price_ratio"], 1.0, 10.0, rpr_default, help=tooltips[language]["resale_price_ratio"])
    hsr = st.slider(lang["housing_stock_ratio"], 0.1, 5.0, hsr_default, help=tooltips[language]["housing_stock_ratio"])

    seed = st.number_input("Random Seed", value=42)
    run = st.form_submit_button(lang["run"])


# ========== 新增：总结历史初始化 ==========
if "summary_history" not in st.session_state:
    st.session_state.summary_history = []

# 固定随机种子
random.seed(int(seed))
np.random.seed(int(seed))

# ========== 常量与标准化 ==========
PIR0, IG0 = 40.0, 0.10
LR0, DPR0 = 0.08, 0.50
GS0, ST0 = 0.20, 0.10
ML0, RPR0 = 1.0, 10.0
HSR0 = 5.0
Q0 = 5.0
delta = 0.1
Q_pref = 1
BETA = {"high": (1.5, 1.2, 0.5, 1.0), "middle": (1.2, 1.0, 1.0, 1.0), "low": (1.0, 0.8, 1.5, 0.8)}
ALPHA = {"high": (0.5, 0.8, 0.3, 0.3, 1.0), "middle": (1.0, 1.2, 1.0, 1.0, 0.8), "low": (0.8, 1.5, 1.5, 1.5, 2.0)}

# ========== Agent ==========
class HouseholdAgent(Agent):
    def __init__(self, uid, model, group):
        super().__init__(uid, model)
        self.group = group
        # 设置是否拥有房产
        self.has_house = True if group == "high" else random.random() < (0.8 if group == "middle" else 0.6)
        # 设置 is_renter 属性        # 根据是否拥有房产设置租房代理属性
        self.is_renter = not self.has_house  # 没有房产是租户，反之是房主
        # 打印调试信息
        print(f"Agent {uid}: Group = {self.group}, Has House = {self.has_house}, Is Renter = {self.is_renter}")

        # 初始化房屋质量
        if self.has_house:
            # 如果拥有房产，根据收入组别设定房屋质量
            if self.group == "high":
                self.house_quality = round(random.uniform(4, 5), 2)
            elif self.group == "middle":
                self.house_quality = round(random.uniform(2.5, 4), 2)
            else:
                self.house_quality = round(random.uniform(0.5, 3), 2)
        else:
            # 对于没有房产的代理，房屋质量为 None（标记为租房代理）
            self.house_quality = None

            # 根据收入组别初始化租房质量
            if self.group == "low":
                self.rental_quality = round(random.uniform(0.5, 3), 2)  # 低收入群体的租房质量范围为 [1, 3]
            elif self.group == "middle":
                self.rental_quality = round(random.uniform(2.5, 5), 2)  # 中等收入群体的租房质量范围为 [2.5, 5]

        self.is_new_home = False  # 默认不是新房

    def step(self):
        # 如果是拥有房产的代理，进行房屋质量折旧
        if self.has_house:
            self.house_quality = max(1.0, self.house_quality * (1 - delta))  # 房屋质量折旧

        # 默认设置为不是新房，避免上轮状态影响本轮显示
        self.is_new_home = False

        # 高收入群体换房逻辑：当房屋质量低于 4.5 时，只有当有新房供应时才会触发换房
        if self.group == "high" and self.has_house and self.house_quality < 4:
            # 只有新房供应量大于 0，才会卖掉当前房产并尝试购买新房
            if self.model.new_supply > 0:
                self.has_house = False  # 卖掉当前房产
                self.model.released_houses.append(self.house_quality)  # 将当前房产放入二手市场
                self.model.high_income_swaps += 1  # 记录高收入群体换房次数

               # 高收入代理买新房的逻辑：只有在没有房产的情况下，且有新房供应时
            if self.group == "high" and not self.has_house and self.model.new_supply > 0:
                new_house_quality = round(random.uniform(4.5, 5), 2)  # 新房质量设定
                self.has_house = True  # 购买新房
                self.house_quality = new_house_quality  # 为购买的新房设定质量
                self.model.new_supply -= 1  # 新房供应量减少
                self.model.new_home += 1  # 记录新房交易
                self.is_new_home = True  # ✅ 关键：让可视化显示黑色圆形

        # 中低收入群体置换：即升级置换
        if self.group in ["middle", "low"] and random.random() < 0.2:  # 中低收入群体置换
            self.model.released_houses.append(self.house_quality)  # 将旧房质量加入市场
            self.model.upgrade_swaps += 1  # 记录中低收入群体置换次数
            self.has_house = False  # 中低收入群体卖房

        # 标准化参数
        til = {
            "PIR": pir / PIR0,
            "IG": (ig / 100) / IG0,
            "LR": (lr / 100) / LR0,
            "DPR": (dpr / 100) / DPR0,
            "GS": (gs / 100) / GS0,
            "ST": (stx / 100) / ST0,
            "ML": (ml / 100) / ML0,
            "RPR": rpr / RPR0,
            "HSR": hsr / HSR0
        }

        # 卖房决策
        b1, b2, b3, b4 = BETA[self.group]
        z_sell = b1 * til["ML"] + b2 * til["RPR"] - b3 * til["ST"] + b4 * til["HSR"]
        p_sell = 1 / (1 + np.exp(-z_sell))
        if self.has_house and random.random() < p_sell:
            self.has_house = False
            self.model.secondary_market += 1
            self.model.released_houses.append(self.house_quality)

        # 买房决策
        a1, a2, a3, a4, a5 = ALPHA[self.group]
        z_buy = -a1 * til["PIR"] + a2 * til["IG"] - a3 * til["LR"] - a4 * til["DPR"] + a5 * til["GS"]
        p_buy = 1 / (1 + np.exp(-z_buy))
        if not self.has_house and random.random() < p_buy:
            # 购买新房或二手房的逻辑
            if self.group == "high" and self.model.new_supply > 0:
                pool_new = [Q0] * self.model.new_supply
                better = [q for q in pool_new if q > self.house_quality]
                worse = [q for q in pool_new if q <= self.house_quality]
                if better and random.random() < 0.8:
                    chosen = random.choice(better)
                elif worse:
                    chosen = random.choice(worse)
                else:
                    chosen = random.choice(pool_new)
                self.has_house = True
                self.house_quality = chosen
                self.is_new_home = True
                self.model.new_supply -= 1
                self.model.new_home += 1
            elif self.model.released_houses:
                q = self.model.released_houses.pop(0)
                if q is not None and q > Q_pref:
                    self.has_house = True
                    self.house_quality = q
                    if self.group == "high":
                        self.model.high_income_swaps += 1
                    else:
                        self.model.upgrade_swaps += 1
                    self.model.new_home += 1

        # 代理迁移逻辑
        if random.random() < 0.2:
            new_x = (self.pos[0] + self.random.randint(-1, 1)) % 15 # 周期性边界
            new_y = (self.pos[1] + self.random.randint(-1, 1)) % 15
            self.model.grid.move_agent(self, (new_x, new_y))  # 移动代理
        # ✅ 更新租房状态（必须放在最后）
        self.is_renter = not self.has_house
        # ✅ 若新变成租户，补上租房质量
        if self.is_renter and not hasattr(self, "rental_quality"):
            if self.group == "low":
                self.rental_quality = round(random.uniform(0.5, 3), 2)
            elif self.group == "middle":
                self.rental_quality = round(random.uniform(2.5, 5), 2)

# ========== Model ==========

class HousingMarketModel(Model):
    def __init__(self, N, ml=50, ig=3.0, pir=18.0, lr=5.0):
        super().__init__()
        self.num_agents = N  # 代理数量
        self.grid = MultiGrid(15, 15, torus=True)  # 创建 10x10 的周期性网格，允许代理从边界移出后从对面进入
        self.schedule = RandomActivation(self)  # 随机激活调度器，用于控制代理的活动

        # 初始化关键参数
        self.ml = ml  # 市场流动性，默认值为 50
        self.ig = ig  # 收入增长，默认值为 3.0%
        self.pir = pir  # 房价收入比，默认值为 18.0
        self.lr = lr  # 贷款利率，默认值为 5.0%

        # 新房、二手房交易的统计变量
        # 初始化新房供应量 (假设一开始有10个新房)
        self.new_supply = 10  # ✅ 设置初始的新房供应量
        self.new_home = 0  # 新房交易量
        self.secondary_market = 0  # 二手房市场交易量
        self.rental_market_transactions = 0  # 租赁市场交易量
        self.released_houses = []  # 被卖出的二手房
        self.high_income_swaps = 0  # 高收入群体换房次数
        self.upgrade_swaps = 0  # 中低收入群体置换次数
        self.current_step = 1  # 初始化step

        # 创建代理并随机放置到网格中
        for i in range(self.num_agents):
            grp = random.choices(["high", "middle", "low"], weights=[0.2, 0.5, 0.3])[0]  # 随机分配收入组别
            agent = HouseholdAgent(i, self, grp)  # 创建代理
            self.schedule.add(agent)  # 将代理添加到调度器中
            # 不再检查空位置，允许重叠
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            # 允许代理重叠，直接放置到网格上
            self.grid.place_agent(agent, (x, y))

        # 在初始化时就执行一次step，让代理执行“买新房”逻辑
        self.step()
    def step(self):
        """ 执行每个时间步的市场更新 """
        self.schedule.step()  # 所有代理执行一次行动
        # 每一步后增加当前步数
        self.current_step += 1

        # 统计租赁市场交易：租房代理为没有房产的低收入和中等收入群体
        rental_count = sum(1 for a in self.schedule.agents if not a.has_house and a.group in ["low", "middle"])
        self.rental_market_transactions += rental_count  # 增加租房市场的交易次数

        # 统计重置
        self.new_home = 0
        self.secondary_market = 0
        self.high_income_swaps = 0  # 高收入群体的换房次数
        self.upgrade_swaps = 0  # 升级置换次数
        self.released_houses.clear()  # 清空被释放的二手房

        # **确保有初始新房供应**，即 10 个新房
        if self.new_supply == 0:
            self.new_supply = 10  # 重新设置新房供应量为 10
        # **根据市场需求调整新房供应量**（动态变化）
        self.new_supply = max(0, int((ml / 100) * 20 * (1 + (ig / 100)) * (1 - (pir / 100)) * (1 - (lr / 100))))
        print(f"New supply: {self.new_supply}")  # 打印新房供应量（调试用）

        # **高收入代理的换房与买新房**
        for agent in self.schedule.agents:
            # 高收入群体换房：当房屋质量低于 4.5 且有新房供应时，执行换房
            if agent.group == "high" and agent.has_house and agent.house_quality < 4.5:
                if self.new_supply > 0:
                    agent.has_house = False  # 卖掉当前房产
                    self.released_houses.append(agent.house_quality)  # 放入二手市场
                    self.high_income_swaps += 1  # 记录换房次数
                # 高收入代理买新房：如果没有房产且有新房供应
            if agent.group == "high" and not agent.has_house and self.new_supply > 0:
                new_house_quality = round(random.uniform(4.5, 5), 2)  # 新房质量设定
                agent.has_house = True  # 购买新房
                agent.house_quality = new_house_quality  # 新房质量
                self.new_supply -= 1  # 新房供应量减少
                self.new_home += 1  # 记录新房交易
                agent.is_new_home = True  # 设置为新房，确保可视化显示为黑色圆形
        # 处理二手房市场和置换
        for agent in self.schedule.agents:
            if agent.has_house:
                if agent.group == "high" and random.random() < 0.8:  # 高收入群体置换二手房
                    self.released_houses.append(agent.house_quality)  # 将旧房质量加入市场
                    self.high_income_swaps += 1  # 记录高收入群体换房次数
                    agent.has_house = False  # 高收入群体卖房

                if agent.group in ["middle", "low"] and random.random() < 0.3:  # 中低收入群体置换
                    self.released_houses.append(agent.house_quality)  # 将旧房质量加入市场
                    self.upgrade_swaps += 1  # 记录中低收入群体置换次数
                    agent.has_house = False  # 中低收入群体卖房

            if not agent.has_house:  # 如果代理没有房产，尝试购买
                if random.random() < 0.8:  # 假设 70% 的代理会尝试购买房产
                    if agent.group == "high" and self.new_supply > 0:
                        new_house_quality = round(random.uniform(4.5, 5), 2)  # 只有高收入群体购买新房
                        agent.has_house = True  # 高收入代理购买新房
                        agent.house_quality = new_house_quality  # 为新房设置质量
                        self.new_supply -= 1  # 新房供应量减少
                        self.new_home += 1  # 记录新房交易
                elif agent.group in ["middle", "low"] and self.released_houses:
                    # 设置最大可接受质量阈值
                    quality_ceiling = 4.5 if agent.group == "middle" else 3

                    # 在可接受范围内筛选房源
                    eligible_houses = [h for h in self.released_houses if h <= quality_ceiling]

                    if eligible_houses:
                        house_to_buy = eligible_houses[0]  # 买第一个符合条件的房源
                        self.released_houses.remove(house_to_buy)

                        agent.has_house = True
                        agent.house_quality = house_to_buy
                        self.secondary_market += 1

                        # ⚠️ 调试：验证房屋质量是否超限
                        if agent.group == "low" and agent.house_quality > 3:
                            print(f"⚠️ 异常！低收入代理 {agent.unique_id} 买到了高质量房：质量={agent.house_quality}")
                    else:
                        # 如果没有合适的房子，就不买
                        pass

        for _ in range(random.randint(5, 10)):
            idx = len(self.schedule.agents)
            grp = random.choices(["high", "middle", "low"], weights=[0.2, 0.5, 0.3])[0]
            agent = HouseholdAgent(idx, self, grp)
            self.schedule.add(agent)

            # 不再检查是否为空位置，允许重叠
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))


    def render_model(self):
        """ 用于更新可视化的模型渲染 """
        self.schedule.step()  # 让所有代理执行一次行动
        # 使用 CanvasGrid 对象进行渲染
        grid.render(self)  # 使用 CanvasGrid 对象进行渲染



# 定义一个更新统计数据的函数
def update_statistics(model):
    """更新统计数据"""
    counts = {"high": 0, "middle": 0, "low": 0}
    for agent in model.schedule.agents:
        counts[agent.group] += 1
    history["pop_high"].append(counts["high"])
    history["pop_mid"].append(counts["middle"])
    history["pop_low"].append(counts["low"])
    history["new_home_market"].append(model.new_home)
    history["secondary_market"].append(model.secondary_market)
    history["rental_market"].append(model.rental_market_transactions)
    rental_count = sum(1 for a in model.schedule.agents if not a.has_house and a.group in ["low", "middle"])
    history["rental_market"].append(int(rental_count))  # 或者不乘系数1.5，直接显示租房代理的数量
    history["high_income_swaps"].append(model.high_income_swaps)
    history["upgrade_swaps"].append(model.upgrade_swaps)
    owned_q = [a.house_quality for a in model.schedule.agents if a.has_house]
    history["avg_quality"].append(np.mean(owned_q) if owned_q else 0)
    history["low_quality_ratio"].append(sum(q < 2.5 for q in owned_q) / len(owned_q) if owned_q else 0)
    history["supply"].append(model.new_supply + model.secondary_market)
    history["demand"].append(sum(1 for a in model.schedule.agents if not a.has_house))
    low_own = sum(1 for a in model.schedule.agents if a.group == "low" and a.has_house)
    low_rent = sum(1 for a in model.schedule.agents if a.group == "low" and not a.has_house)
    mid_own = sum(1 for a in model.schedule.agents if a.group == "middle" and a.has_house)
    mid_rent = sum(1 for a in model.schedule.agents if a.group == "middle" and not a.has_house)

    history["low_own"].append(low_own)
    history["low_rent"].append(low_rent)
    history["mid_own"].append(mid_own)
    history["mid_rent"].append(mid_rent)


# 网格显示
def render_grid(model):
    grid.render(model)

# 动态添加情景说明
if scenario == lang["baseline_scenario"]:
    scenario_description = "本次模拟基于【基准市场演化情景】，市场处于自由运行状态，交易活跃度中等，住房过滤过程较为自然。"
elif scenario == lang["credit_stimulus_scenario"]:
    scenario_description = "本次模拟基于【信贷刺激与市场活跃情景】，贷款条件放宽，购房需求显著释放，市场交易活跃。"
elif scenario == lang["fiscal_subsidy_scenario"]:
    scenario_description = "本次模拟基于【政府干预与住房可负担性提升情景】，政府购房补贴增强，交易税下降，中低收入家庭购房能力提升。"

# ========== 新增：生成总结用的进阶prompt函数 ==========
# 自动推断情景中的核心政策矛盾
def infer_scenario_issue(history, pir, lr, ml, ig):
    pct_new = (history['new_home_market'][-1] - history['new_home_market'][0]) / max(history['new_home_market'][0], 1)
    delta_q = history['avg_quality'][-1] - history['avg_quality'][0]
    delta_lq = history['low_quality_ratio'][-1] - history['low_quality_ratio'][0]
    pct_rent = (history['rental_market'][-1] - history['rental_market'][0]) / max(history['rental_market'][0], 1)
    issues = []
    if pct_new > 0.2 and delta_q < -0.1:
        issues.append("市场过热且品质下滑风险")
    if pct_rent < 0.05 and delta_lq > 0.05:
        issues.append("过滤效率不足与结构性轮候阻滞")
    if ig > 0.2 and (pct_new > 0.3 or pct_rent > 0.3):
        issues.append("政府补贴下套利与虚假交易现象加剧")
    return "；".join(issues) or "市场演化中的潜在问题"

# 构建针对政策建议的 Prompt
# ------------------- 自动推断情景中的核心政策矛盾 -------------------
def infer_scenario_issue(history, pir, lr, ml, ig):
    pct_new = (history['new_home_market'][-1] - history['new_home_market'][0]) / max(history['new_home_market'][0], 1)
    delta_q = history['avg_quality'][-1] - history['avg_quality'][0]
    delta_lq = history['low_quality_ratio'][-1] - history['low_quality_ratio'][0]
    pct_rent = (history['rental_market'][-1] - history['rental_market'][0]) / max(history['rental_market'][0], 1)
    issues = []
    if pct_new > 0.2 and delta_q < -0.1:
        issues.append("市场过热且品质下滑风险")
    if pct_rent < 0.05 and delta_lq > 0.05:
        issues.append("过滤效率不足与结构性轮候阻滞")
    if ig > 0.2 and (pct_new > 0.3 or pct_rent > 0.3):
        issues.append("政府补贴下套利与虚假交易现象加剧")
    return "；".join(issues) or "市场演化中的潜在问题"

# ------------------- 构建针对政策建议的 Prompt -------------------
def generate_policy_recommendation_prompt(history, pir, lr, ml, ig,
                                          scenario_name, policy_principles,
                                          language="中文", role="policymaker",
                                          call_llm=False, model="gpt-4"):
    """
    根据真实模拟数据和国家政策理念，生成面向特定角色的可操作性政策建议。

    返回值：
      system_prompt, user_prompt （若 call_llm=True，则附加 llm_response）
    """
    # 1. 推断场景核心矛盾
    issue = infer_scenario_issue(history, pir, lr, ml, ig)

    # 2. 场景与政策背景描述
    scene_desc = (
        f"情景：{scenario_name}，核心矛盾：{issue}\n"
        f"参数：PIR={pir}, LR={lr}, ML={ml}, IG={ig}\n"
        f"政策导向：{policy_principles}\n"
    )

    # 3. 构建 system_prompt
    if language == "中文":
        if role == "policymaker":
            sys = (
                scene_desc +
                "你是住房政策制定者，请基于上述情景和数据，从以下四个维度提出具体、可操作的政策建议：\n"
                "1. 住房供给：如何精准投放与保障\n"
                "2. 住房品质：如何提升品质与存量改造\n"
                "3. 金融与税收：如何优化信贷、契税、公积金等工具\n"
                "4. 财政支持：如何设计补贴与资金配置机制\n"
                "请确保每条建议都明确回应核心矛盾，并说明政策实施路径与预期效果。"
            )
        elif role == "regulator":
            sys = (
                scene_desc +
                "你是市场监管者，请基于上述情景，针对以下领域提出监管举措：\n"
                "1. 信贷风控：如何防范和化解信贷风险\n"
                "2. 交易秩序：如何规范中介与平台行为\n"
                "3. 信息透明：如何完善数据与白名单机制\n"
                "4. 合规测试：如何在 ABM 模型中验证监管措施有效性\n"
                "请提供具体操作步骤和监管工具设计。"
            )
        else:
            sys = (
                scene_desc +
                "你是住房政策分析师，请基于上述情景，设计评估政策干预效果的可量化指标：\n"
                "- 过滤效率指数、住房支付能力指数、轮候响应指数等\n"
                "并提出模拟方案，以量化不同政策组合的效果和反馈机制。"
            )
    else:
        if role == "policymaker":
            sys = (
                scene_desc +
                "You are a policymaker. Based on the above, propose actionable policies in four dimensions: supply, quality, finance, and fiscal support. "
                "Ensure each recommendation addresses the core issue and outlines implementation and expected outcomes."
            )
        elif role == "regulator":
            sys = (
                scene_desc +
                "You are a regulator. Propose regulatory measures in: credit risk control, transaction oversight, data transparency, and compliance testing within the ABM model. "
                "Detail tools, processes, and validation steps."
            )
        else:
            sys = (
                scene_desc +
                "You are an analyst. Design quantitative metrics such as filter efficiency, affordability index, waiting response index. "
                "Outline simulation schemes to evaluate policy combinations."
            )

    # 4. 用户 Prompt
    user = "请根据以上系统提示和提供的模拟数据，输出结构化政策建议列表。"

    # 5. 可选 调用 LLM
    if call_llm:
        messages = [
            {"role": "system", "content": sys},
            {"role": "user", "content": user}
        ]
        resp = openai.ChatCompletion.create(model=model, messages=messages, temperature=0.7)
        return sys, user, resp['choices'][0]['message']['content']

    return sys, user
# 示例调用方法
def example_usage():
    # 准备示例数据
    history = {
        'new_home_market': [100, 140],
        'secondary_market': [80, 85],
        'rental_market': [50, 52],
        'avg_quality': [0.8, 0.75],
        'low_quality_ratio': [0.1, 0.15]
    }
    pir, lr, ml, ig = 6.0, 0.045, 0.5, 0.15
    scenario_name = 'baseline_scenario'
    policy_principles = '租购并举；因城施策；多主体供给'
    # 不调用 LLM，仅返回 prompts
    system_prompt, user_prompt = generate_policy_recommendation_prompt(
        history, pir, lr, ml, ig,
        scenario_name, policy_principles,
        language='中文', role='policymaker', call_llm=False
    )
    print('=== SYSTEM PROMPT ===')
    print(system_prompt)
    print('\n=== USER PROMPT ===')
    print(user_prompt)

if __name__ == '__main__':
    example_usage()



# ========== 可视化网格 ==========

def agent_portrayal(agent):
    """ 定义 ABM 代理的可视化 """
    # 打印代理的 `group`、`has_house` 和 `is_renter` 属性
    print(
        f"Agent {agent.unique_id}: Group = {agent.group}, Has House = {agent.has_house}, Is Renter = {agent.is_renter}")
    # 只渲染没有房产且不是租房代理的代理
    if agent.has_house is False and agent.is_renter is False:
        return {}  # 跳过该代理，不渲染
    if agent.is_renter:
        # 如果是租房代理但未初始化 rental_quality，则根据收入组别补充
        if not hasattr(agent, "rental_quality"):
            if agent.group == "low":
                agent.rental_quality = round(random.uniform(0.5, 3), 2)
            elif agent.group == "middle":
                agent.rental_quality = round(random.uniform(2.5, 5), 2)
            else:
                # 高收入群体不应是租户，这里加默认值防止报错（或直接 return {} 跳过）
                return {}
        radius = agent.rental_quality / 8
    else:
        # 否则，使用房屋质量计算半径
        if agent.house_quality is None:
            radius = 0  # 如果房屋质量是 None，设置为 0 或者其他合理值
        else:
            radius = agent.house_quality / 8  # 房屋质量影响半径

    # 确保每个代理都属于一个明确的状态，并具有明确的颜色和形状
    symbol_map = {
        ("low", False): {"color": "lightcoral", "symbol": "🟥", "shape": "rect"},  # 低收入且没有房子显浅红色正方形
        ("low", True): {"color": "red", "symbol": "🔴", "shape": "circle"},    # 低收入且有房子显示红色圆形
        ("middle", False): {"color": "lightgreen", "symbol": "🟩", "shape": "rect"},  # 中等收入且没有房子显示浅绿色正方形
        ("middle", True): {"color": "green", "symbol": "🟢", "shape": "circle"},  # 中等收入且有房子显示绿色圆形
        ("high", True): {"color": "blue", "symbol": "🔵", "shape": "circle"},   # 高收入且有房子显示蓝色圆形
    }

    # 常规情况处理
    key = (agent.group, agent.has_house)
    style = symbol_map.get(key, None)  # 从字典中获取样式，不使用默认值
    # 如果没有匹配到，直接返回，避免灰色
    # 新房特殊处理
    if agent.is_new_home:
        return {
            "Shape": "circle",  # 新房用圆形
            "Color": "black",
            "r": radius,
            "Layer": 0,
            "Text": "⚫",
            "Filled": "true"  # 新房是实心圆形
        }

    # 正方形的边长设置为 2 * radius，确保与圆形的直径相匹配
    if style["shape"] == "rect":
        return {
            "Shape": "rect",  # 设置为矩形（即正方形）
            "Color": style["color"],
            "w":  radius,  # 正方形的边长为半径的2倍
            "h":  radius,  # 正方形的高度与宽度相同，确保为正方形
            "Layer": 0,
            "Text": style["symbol"],  # 显示符号
            "Filled": "true"  # 确保为实心矩形
        }
    else:
        return {
            "Shape": "circle",  # 设置为圆形
            "Color": style["color"],
            "r": radius,  # 半径
            "Layer": 0,
            "Text": style["symbol"],  # 显示符号
            "Filled": "true"  # 确保为实心圆形
        }

# 在 Streamlit 中使用可视化
grid = CanvasGrid(agent_portrayal, 15, 15, 500, 500)  # 创建网格

# ========== 统计与图表 ==========
history = {"new_home_market": [], "secondary_market": [], "rental_market": [], "high_income_swaps": [],
           "upgrade_swaps": [], "avg_quality": [], "low_quality_ratio": [], "supply": [], "demand": [], "pop_high": [],
           "pop_mid": [], "pop_low": [], "secondary_supply": [], "low_own": [], "low_rent": [], "mid_own": [], "mid_rent": []}

model = HousingMarketModel(50) #设置代理最初数量

for t in range(100):
    model.step()
    model.render_model() # 渲染网格

    # ✅ 每步模拟后新增细分人口结构记录
    low_own = sum(1 for a in model.schedule.agents if a.group == "low" and a.has_house)
    low_rent = sum(1 for a in model.schedule.agents if a.group == "low" and not a.has_house)
    mid_own = sum(1 for a in model.schedule.agents if a.group == "middle" and a.has_house)
    mid_rent = sum(1 for a in model.schedule.agents if a.group == "middle" and not a.has_house)

    history["low_own"].append(low_own)
    history["low_rent"].append(low_rent)
    history["mid_own"].append(mid_own)
    history["mid_rent"].append(mid_rent)

    history["new_home_market"].append(model.new_home)
    history["secondary_market"].append(model.secondary_market)

    rental_count = sum(1 for a in model.schedule.agents if not a.has_house and a.group in ["low", "middle"])
    history["rental_market"].append(int(rental_count))  # 或者不乘系数1.5，直接显示租房代理的数量

    history["high_income_swaps"].append(model.high_income_swaps)
    history["upgrade_swaps"].append(model.upgrade_swaps)
    # 记录拥有房产代理的房屋质量统计
    owned_q = [a.house_quality for a in model.schedule.agents if a.has_house]
    history["avg_quality"].append(np.mean(owned_q) if owned_q else 0)
    history["low_quality_ratio"].append(sum(q < 2.5 for q in owned_q) / len(owned_q) if owned_q else 0)
    # 记录新房供应量和二手房交易量
    history["supply"].append(model.new_supply + model.secondary_market)
    history["demand"].append(sum(1 for a in model.schedule.agents if not a.has_house))
    # 统计各群体的人口数量
    counts = {"high": 0, "middle": 0, "low": 0}
    for a in model.schedule.agents:
        counts[a.group] += 1
    history["pop_high"].append(counts["high"])
    history["pop_mid"].append(counts["middle"])
    history["pop_low"].append(counts["low"])
 # 记录二手房供应量
    history["secondary_supply"].append(model.secondary_market)  # 记录二手房供应量

# ✅ 生成图表
x = np.arange(1, 101)
# ✅ 在这里加上导出格式选择
# ✅ 不再需要 export_format 选择器
# 直接统一导出格式为 'png'
export_format = "png"


# ① 新房/二手/租赁交易量趋势
fig1, ax1 = plt.subplots(figsize=(6, 4))
ax1.plot(x, history["new_home_market"], label=lang["new_home_market"], color="black", linewidth=2)
ax1.plot(x, history["secondary_market"], label=lang["secondary_market"], color="red", linewidth=2)
ax1.plot(x, history["rental_market"], label=lang["rental_market"], color="gold", linewidth=2)
ax1.set_xlabel(lang["step_length"])
ax1.set_ylabel(lang["transactions"])
ax1.grid(True)
ax1.legend(loc="upper right")
# 导出按钮
buffer1 = io.BytesIO()
fig1.savefig(buffer1, format=export_format, bbox_inches='tight')
buffer1.seek(0)

# ② 换房行为趋势
fig2, ax2 = plt.subplots(figsize=(6, 4))
ax2.plot(x, history["high_income_swaps"], label=lang["high_income_swaps"], color="blue", linewidth=2)
ax2.plot(x, history["upgrade_swaps"], label=lang["upgrade_swaps"], color="green", linewidth=2)
ax2.set_xlabel(lang["step_length"])
ax2.set_ylabel(lang["transactions"])
ax2.grid(True)
ax2.legend(loc="upper right")
# 导出按钮
buffer2 = io.BytesIO()
fig2.savefig(buffer2, format=export_format, bbox_inches='tight')
buffer2.seek(0)

# ③ 平均住房质量 vs 低质住房占比
fig3, ax3 = plt.subplots(figsize=(7.8, 5.2))  # 原来是(6, 4)，现在稍微加宽
ax3.plot(x, history["avg_quality"], label=lang["avg_quality"], color="purple", linewidth=2)
ax3.set_xlabel(lang["step_length"])
ax3.set_ylabel(lang["avg_quality"], color="purple", fontsize=15)
ax3.grid(True)
ax3.set_ylim(0, 5)
ax3.tick_params(axis='x', labelsize=15)
ax3.tick_params(axis='y', labelsize=15)
ax3.set_xlabel(lang["step_length"], fontsize=15)


ax4 = ax3.twinx()
ax4.plot(x, history["low_quality_ratio"], label=lang["low_quality_ratio"], color="red", linewidth=2)
ax4.set_ylabel(lang["low_quality_ratio"], color="red", fontsize=15)
# ✅ 强制设置Y轴范围一致感
ax4.set_ylim(0, 1)
ax4.tick_params(axis='y', labelsize=15)
# 图例合并
h1, l1 = ax3.get_legend_handles_labels()
h2, l2 = ax4.get_legend_handles_labels()
ax3.legend(h1 + h2, l1 + l2, loc="upper right", fontsize=15)

# 自动紧凑布局
fig3.tight_layout()
# 导出按钮
buffer3 = io.BytesIO()
fig3.savefig(buffer3, format=export_format, bbox_inches='tight')
buffer3.seek(0)


# ④ 人口结构堆叠柱状图（函数式绘图）
# ④ 人口结构堆叠柱状图（语言联动 + 导出图像）
fig4, ax4 = plt.subplots(figsize=(6, 4))
x = list(range(len(history["low_own"])))

ax4.bar(x, history["pop_high"], label=lang["pop_high_owner"], color="blue")
ax4.bar(x, history["mid_own"], label=lang["pop_mid_owner"], color="green", bottom=np.array(history["pop_high"]))
ax4.bar(x, history["mid_rent"], label=lang["pop_mid_renter"], color="lightgreen", bottom=np.array(history["pop_high"]) + np.array(history["mid_own"]))
bottom_low_own = np.array(history["pop_high"]) + np.array(history["mid_own"]) + np.array(history["mid_rent"])
ax4.bar(x, history["low_own"], label=lang["pop_low_owner"], color="red", bottom=bottom_low_own)
bottom_low_rent = bottom_low_own + np.array(history["low_own"])
ax4.bar(x, history["low_rent"], label=lang["pop_low_renter"], color="lightcoral", bottom=bottom_low_rent)

ax4.set_xlabel(lang["pop_structure_xlabel"])
ax4.set_ylabel(lang["pop_structure_ylabel"])
ax4.grid(True)
ax4.legend(loc="upper left")

# 导出图像
buffer4 = io.BytesIO()
fig4.savefig(buffer4, format=export_format, bbox_inches='tight')
buffer4.seek(0)

# 📌 2. 两两排版，并且每张图下面都加一个小下载按钮

# --- 第一行（图1 左，图2 右） ---
row1_col1, row1_col2 = st.columns(2)

# --- 图1左 ---
with row1_col1:
    title_col1, title_col2, title_col3 = st.columns([12, 3.4, 1])
    with title_col1:
        st.markdown(f"<h5 style='text-align: center; font-weight: normal;'>{lang['transaction_trend']}</h5>",
                    unsafe_allow_html=True)

    with title_col2:
        selected_format1 = st.selectbox(
            label="格式",
            options=("eps", "jpeg", "png"),
            label_visibility="collapsed",
            key="format_selector_fig1"
        )
    with title_col3:
        buffer1 = io.BytesIO()
        fig1.savefig(buffer1, format=selected_format1, bbox_inches='tight')
        buffer1.seek(0)
        href1 = f"data:image/{'jpeg' if selected_format1 == 'jpeg' else selected_format1};base64,{base64.b64encode(buffer1.getvalue()).decode()}"
        st.markdown(f'<a href="{href1}" download="transaction_volume_change.{selected_format1}" class="save-icon-button">💾</a>', unsafe_allow_html=True)

    st.pyplot(fig1, use_container_width=True)
    if language == "中文":
        st.markdown(
            "<p style='text-align: left; font-size: 14px; color: gray;'>注：该图展示了模拟期内三类住房市场（新房、二手房、租赁）的交易活跃度变化趋势。</p>",
            unsafe_allow_html=True)
    else:
        st.markdown(
            "<p style='text-align: left; font-size: 14px; color: gray;'>Note: This chart shows the transaction dynamics of new housing, resale, and rental markets during the simulation.</p>",
            unsafe_allow_html=True)

# --- 图2右 ---
with row1_col2:
    title_col4, title_col5, title_col6 = st.columns([12, 3.4, 1])
    with title_col4:
        st.markdown(f"<h5 style='text-align: center; font-weight: normal;'>{lang['swap_trend']}</h5>",
                    unsafe_allow_html=True)

    with title_col5:
        selected_format2 = st.selectbox(
            label="格式",
            options=("eps", "jpeg", "png"),
            label_visibility="collapsed",
            key="format_selector_fig2"
        )
    with title_col6:
        buffer2 = io.BytesIO()
        fig2.savefig(buffer2, format=selected_format2, bbox_inches='tight')
        buffer2.seek(0)
        href2 = f"data:image/{'jpeg' if selected_format2 == 'jpeg' else selected_format2};base64,{base64.b64encode(buffer2.getvalue()).decode()}"
        st.markdown(f'<a href="{href2}" download="housing_swap_behavior_change.{selected_format2}" class="save-icon-button">💾</a>', unsafe_allow_html=True)

    st.pyplot(fig2, use_container_width=True)
    if language == "中文":
        st.markdown(
            "<p style='text-align: left; font-size: 14px; color: gray;'>注：该图展示了模拟期内高收入群体换新房以及中低收入群体升级置换的住房行为演变过程。</p>",
            unsafe_allow_html=True)
    else:
        st.markdown(
            "<p style='text-align: left; font-size: 14px; color: gray;'>Note: This chart illustrates housing replacement behaviors of high-income and upgrading low/middle-income groups during the simulation.</p>",
            unsafe_allow_html=True)

# --- 第二行（图3 左，图4 右） ---
row2_col1, row2_col2 = st.columns(2)

# --- 图3左 ---
with row2_col1:
    title_col7, title_col8, title_col9 = st.columns([12, 3.4, 1])
    with title_col7:
        st.markdown(f"<h5 style='text-align: center; font-weight: normal;'>{lang['housing_quality_trend']}</h5>",
                    unsafe_allow_html=True)

    with title_col8:
        selected_format3 = st.selectbox(
            label="格式",
            options=("eps", "jpeg", "png"),
            label_visibility="collapsed",
            key="format_selector_fig3"
        )
    with title_col9:
        buffer3 = io.BytesIO()
        fig3.savefig(buffer3, format=selected_format3, bbox_inches='tight')
        buffer3.seek(0)
        href3 = f"data:image/{'jpeg' if selected_format3 == 'jpeg' else selected_format3};base64,{base64.b64encode(buffer3.getvalue()).decode()}"
        st.markdown(f'<a href="{href3}" download="housing_quality_change.{selected_format3}" class="save-icon-button">💾</a>', unsafe_allow_html=True)

    st.pyplot(fig3, use_container_width=True)
    if language == "中文":
        st.markdown(
            "<p style='text-align: left; font-size: 14px; color: gray;'>注：该图展示了模拟期内所有房主的平均住房质量以及低质量住房（房屋质量低于 2.5）占比的演变过程。</p>",
            unsafe_allow_html=True)
    else:
        st.markdown(
            "<p style='text-align: left; font-size: 14px; color: gray;'>Note: This chart shows the evolution of average housing quality among all homeowners and the proportion of low-quality housing (defined as quality below 2.5) during the simulation period.</p>",
            unsafe_allow_html=True)

# --- 图4右 ---
with row2_col2:
    title_col10, title_col11, title_col12 = st.columns([11, 3.4, 1])
    with title_col10:
        st.markdown(f"<h5 style='text-align: center; font-weight: normal;'>{lang['population_structure_change']}</h5>",
                    unsafe_allow_html=True)#图名格式
    with title_col11:
        selected_format4 = st.selectbox(
            label="格式",
            options=("eps", "jpeg", "png"),
            label_visibility="collapsed",
            key="format_selector_fig4"
        )
    with title_col12:
        buffer4 = io.BytesIO()
        fig4.savefig(buffer4, format=selected_format4, bbox_inches='tight')
        buffer4.seek(0)
        href4 = f"data:image/{'jpeg' if selected_format4 == 'jpeg' else selected_format4};base64,{base64.b64encode(buffer4.getvalue()).decode()}"
        st.markdown(f'<a href="{href4}" download="population_structure_change.{selected_format4}" class="save-icon-button">💾</a>', unsafe_allow_html=True)

    st.pyplot(fig4, use_container_width=True)
    if language == "中文":
        st.markdown(
            "<p style='text-align: left; font-size: 14px; color: gray;'>注：该图展示了不同收入群体中有房与租房人口的变化趋势。图中颜色区分不同收入层次与住房状态，柱状高度代表对应人口数量。</p>",
            unsafe_allow_html=True)
    else:
        st.markdown(
            "<p style='text-align: left; font-size: 14px; color: gray;'>Note: This chart shows changes in population structure by income and housing status. Colored bars represent income and tenure groups, and bar height indicates population size.</p>",
            unsafe_allow_html=True)

# ========== 📝 模拟总结模块开始 ==========
st.markdown(f"""
    <div style='font-size: 22px; font-weight: bold; margin-top: 25px; margin-bottom: 10px;'>
        {lang["llm_summary_analysis"]}
    </div>
""", unsafe_allow_html=True)


# 选择总结风格
# 🔄 根据语言显示不同角色标签和选项
if language == "中文":
    role_options = {
        "政策制定者": "policymaker",
        "监督者": "regulator",
        "分析师/研究者": "analyst"
    }
    role_label = "选择总结角色"
else:
    role_options = {
        "Policymaker": "policymaker",
        "Regulator": "regulator",
        "Analyst / Researcher": "analyst"
    }
    role_label = "Select Summary Role"

summary_role_display = st.selectbox(
    role_label,
    list(role_options.keys())
)
summary_role = role_options[summary_role_display]



# 语言联动输入框 label
label_key = "🔑 输入 OpenAI API Key（可选）" if language == "中文" else "🔑 Enter OpenAI API Key (optional)"
st.session_state.user_api_key = st.text_input(label_key, type="password")

# 输入框下方说明提示（联动语言）
if language == "中文":
    st.markdown("""
    <div style='background-color:#eaf4fb; padding:10px; border-left: 6px solid #2c91d3; font-size:13px;'>
    🔎 为确保模型可用性，在未输入 OpenAI API Key 的情况下，系统将自动启用作者预设的总结规则生成结果。该结果为基于模拟过程的静态分析，仅供参考。
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='background-color:#eaf4fb; padding:10px; border-left: 6px solid #2c91d3; font-size:13px;'>
    🔎 If you do not provide an OpenAI API Key, the system will automatically generate a fallback summary based on rule-based analysis of the simulation process. This result is for reference only.
    </div>
    """, unsafe_allow_html=True)
# 👉 添加空白行，拉开距离
st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
# ========== 模拟总结生成 ==========
if st.button(lang["generate_summary"]):
    use_llm = bool(st.session_state.user_api_key)
    if scenario == lang["baseline_scenario"]:
        scenario_name = "baseline_scenario"
    elif scenario == lang["credit_stimulus_scenario"]:
        scenario_name = "credit_stimulus_scenario"
    elif scenario == lang["fiscal_subsidy_scenario"]:
        scenario_name = "fiscal_subsidy_scenario"

    policy_principle_map = {
        'baseline_scenario': '租购并举；因城施策；多主体供给',
        'credit_stimulus_scenario': '支持合理信贷；防范泡沫；优化置换链条',
        'fiscal_subsidy_scenario': '财政兜底保障；精准发力低收入群体；稳定住房消费'
    }
    policy_principles = policy_principle_map.get(scenario_name, '租购并举；因城施策；多主体供给')
    if use_llm:
        try:
            client = OpenAI(api_key=st.session_state.user_api_key)
            system_prompt, user_prompt = generate_policy_recommendation_prompt(
                history, pir, lr, ml, ig,
                scenario_name, policy_principles,
                language='中文', role='policymaker', call_llm=False
            )
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            summary_text = response.choices[0].message.content
        except Exception as e:
            st.warning(f"⚠️ 无法连接OpenAI，使用本地细化总结。错误：{str(e)}")
            use_llm = False

    if not use_llm:
        # ✅ 根据语言选择推荐集
        static_recommendations = STATIC_RECOMMENDATIONS_ZH if language == "中文" else STATIC_RECOMMENDATIONS_EN

        # ✅ 调用推荐内容：按情景 + 角色获取
        summary_text = static_recommendations.get(scenario_name, {}).get(summary_role)

        # ✅ 若无匹配内容则提醒
        if not summary_text:
            summary_text = "⚠️ 当前角色与情景组合暂无静态分析文本，请完善 static_summaries.py。"

    # ✅ 保存历史并提示
    st.session_state.summary_history.append(summary_text.strip())
    st.session_state[f"summary_style_{len(st.session_state.summary_history)}"] = summary_role_display
    st.success("✅ 总结生成成功！")


# ========== 展示总结历史 ==========
if st.session_state.summary_history:
    for i, summary in enumerate(reversed(st.session_state.summary_history)):
        expanded = (i == 0)
        style_display = st.session_state.get(f"summary_style_{len(st.session_state.summary_history) - i}", "正式")
        with st.expander(f"总结 #{len(st.session_state.summary_history) - i}（{style_display}风格）", expanded=expanded):
            st.markdown(summary)


# ========== 清空总结历史 ==========
if st.button(lang["clear_summary_history"]):
    # 清空历史逻辑...
    st.session_state.summary_history = []
    st.rerun()  # ✅ 立刻局部刷新页面


# ========== 颜色图例 & 网格 ==========
st.markdown(f"""
    <div style='font-size: 22px; font-weight: bold; margin-top: 25px; margin-bottom: 10px;'>
        {lang["visualization_title"]}
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3) #三列排版
with col1:
    st.markdown(f"🔴 {lang['color_legend']['red']}")
    st.markdown(f"🟥 {lang['color_legend']['Lightcoral']}")
with col2:
    st.markdown(f"🟢 {lang['color_legend']['green']}")
    st.markdown(f"🟩 {lang['color_legend']['Lightgreen']}")
with col3:
    st.markdown(f"🔵 {lang['color_legend']['blue']}")
    st.markdown(f"⚫ {lang['color_legend']['black']}")


# 启动 Mesa 服务器
def find_free_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

if run:
    # 用一个纯文本标题（不带图标）传给 ModularServer，防止乱码
    clean_title = (
        "🔄 基于ABM的住房过滤动态仿真"
        if language == "中文"
        else "🔄 ABM-Based Dynamic Housing Filtering Simulation"
    )
    server = ModularServer(
        HousingMarketModel,
        [grid],
        clean_title,
        {"N": 100}
    )
    server.port = find_free_port()
    server.launch()

def main():
    import streamlit.web.cli as stcli
    import sys
    sys.argv = ["streamlit", "run", __file__]
    sys.exit(stcli.main())
