import streamlit as st
import pandas as pd
import requests
import re

# ---------------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Procurement AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.stApp { background: radial-gradient(circle at 20% 10%, rgba(0,180,255,.08), transparent 25%), radial-gradient(circle at 80% 20%, rgba(120,70,255,.08), transparent 25%), #080b12; }
.block-container { max-width: 1200px; padding-top: 40px; padding-bottom: 100px; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg,#111621 0%,#090c13 100%); border-right:1px solid rgba(80,170,255,.12); }
section[data-testid="stSidebar"] > div { padding: 30px 18px; }
.ai-logo { font-size:42px; text-align:center; }
.ai-title { text-align:center; color:white; font-size:22px; font-weight:700; }
.ai-title span,.main-title span,.welcome-heading span { background:linear-gradient(90deg,#22d3ee,#8b5cf6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.ai-subtitle { text-align:center; color:#7f8ba0; font-size:11px; margin:6px 0 30px; }
.ai-status { background:linear-gradient(135deg,rgba(20,190,255,.10),rgba(130,80,255,.10)); border:1px solid rgba(60,190,255,.20); border-radius:14px; padding:15px; margin-bottom:22px; }
.ai-status-title { color:#35e69a; font-size:13px; font-weight:600; }
.ai-status-text { color:#77849a; font-size:11px; margin-top:6px; line-height:1.5; }
.nav-item { padding:11px 13px; margin:5px 0; border-radius:10px; color:#aab5c7; font-size:13px; }
.nav-active { background:linear-gradient(90deg,rgba(30,170,255,.18),rgba(120,70,255,.18)); border:1px solid rgba(80,180,255,.18); color:white; }
.sidebar-message { margin-top:45px; padding:15px; border-radius:14px; background:rgba(255,255,255,.025); border:1px solid rgba(255,255,255,.06); color:#8490a4; font-size:11px; line-height:1.6; }
.main-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:28px; }
.main-title { font-size:38px; font-weight:750; color:white; }
.main-description { color:#7f8ba0; font-size:13px; margin-top:5px; }
.ready-badge { background:rgba(40,220,150,.08); border:1px solid rgba(40,220,150,.20); border-radius:20px; padding:8px 14px; color:#45e7a0; font-size:11px; }
.welcome-card { text-align:center; padding:45px 30px; border-radius:22px; background:linear-gradient(135deg,rgba(19,31,55,.90),rgba(11,16,28,.95)); border:1px solid rgba(70,170,255,.15); box-shadow:0 25px 70px rgba(0,0,0,.25); }
.robot { font-size:60px; }
.welcome-heading { color:white; font-size:30px; font-weight:700; margin-top:10px; }
.welcome-description { color:#8c99ad; max-width:680px; margin:14px auto 0; line-height:1.7; font-size:13px; }
.feature-card { background:rgba(20,27,42,.75); border:1px solid rgba(255,255,255,.06); border-radius:15px; padding:18px 12px; text-align:center; min-height:115px; }
.feature-icon { font-size:24px; }
.feature-title { color:#e8eef8; font-size:13px; font-weight:600; margin-top:7px; }
.feature-description { color:#718096; font-size:10px; margin-top:5px; line-height:1.4; }
div[data-testid="stChatMessage"] { background:rgba(20,27,42,.55); border:1px solid rgba(255,255,255,.05); border-radius:15px; margin-bottom:10px; }
div[data-testid="stChatInput"] > div { background:#151a26; border:1px solid rgba(50,190,255,.30); border-radius:18px; box-shadow:0 0 25px rgba(20,170,255,.05); }
div[data-testid="stChatInput"] textarea { color:white; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
  <div>
    <div class="main-title">Procurement <span>AI Assistant</span></div>
    <div class="main-description">Ask questions. Analyze procurement data. Get intelligent answers.</div>
  </div>
  <div class="ready-badge">● AI Assistant Ready</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
# Keep your CSV in the same folder as this Python file.
# The first filename is the recommended one.
DATA_FILES = [
    "vendor_cleaned_kpi.csv",
    "vendor_cleaned_kpi(2).csv",
    "vendor_cleaned_kpi(1).csv"
]

df = None

for file_name in DATA_FILES:
    try:
        df = pd.read_csv(file_name)
        DATA_FILE = file_name
        break
    except FileNotFoundError:
        continue

if df is None:
    st.error("Procurement KPI CSV file was not found.")
    st.info(
        "Put vendor_cleaned_kpi.csv in the same folder as procurement_ai.py."
    )
    st.stop()

# ---------------------------------------------------------
# BASIC DATA CHECK
# ---------------------------------------------------------
required_columns = [
    "PO_ID",
    "Supplier",
    "Item_Category",
    "Total_Spend",
    "Savings",
    "Delivery_Days",
    "Defect_Rate",
    "Quality_Rate"
]

missing_columns = [c for c in required_columns if c not in df.columns]

if missing_columns:
    st.error("Missing required columns:")
    st.write(missing_columns)
    st.stop()

# Make sure numeric columns are numeric
numeric_columns = [
    "Total_Spend",
    "Savings",
    "Delivery_Days",
    "Defect_Rate",
    "Quality_Rate"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# ---------------------------------------------------------
# VENDOR SUMMARY
# ---------------------------------------------------------
vendor = (
    df.groupby("Supplier")
    .agg(
        Total_Spend=("Total_Spend", "sum"),
        Total_Savings=("Savings", "sum"),
        Orders=("PO_ID", "nunique"),
        Avg_Delivery_Days=("Delivery_Days", "mean"),
        Avg_Defect_Rate=("Defect_Rate", "mean"),
        Avg_Quality_Rate=("Quality_Rate", "mean")
    )
    .round(2)
    .reset_index()
)

# ---------------------------------------------------------
# CATEGORY SUMMARY
# ---------------------------------------------------------
category = (
    df.groupby("Item_Category")
    .agg(
        Total_Spend=("Total_Spend", "sum"),
        Total_Savings=("Savings", "sum"),
        Orders=("PO_ID", "nunique")
    )
    .round(2)
    .reset_index()
)

# ---------------------------------------------------------
# OVERALL METRICS
# ---------------------------------------------------------
total_spend = df["Total_Spend"].sum()
total_savings = df["Savings"].sum()
total_orders = df["PO_ID"].nunique()
avg_delivery = df["Delivery_Days"].mean()
avg_defect = df["Defect_Rate"].mean()
avg_quality = df["Quality_Rate"].mean()

# ---------------------------------------------------------
# QUESTION DETECTION
# ---------------------------------------------------------
def detect_question(q):
    q = q.lower().strip()

    # Vendor spending
    if (
        ("highest" in q or "top" in q or "maximum" in q)
        and ("spend" in q or "spending" in q)
        and "vendor" in q
    ):
        return "highest_vendor_spend"

    if (
        ("lowest" in q or "least" in q or "minimum" in q)
        and ("spend" in q or "spending" in q)
        and "vendor" in q
    ):
        return "lowest_vendor_spend"

    # Vendor savings
    if (
        ("highest" in q or "best" in q or "maximum" in q)
        and ("saving" in q or "savings" in q)
        and "vendor" in q
    ):
        return "highest_vendor_savings"

    if (
        ("lowest" in q or "least" in q or "minimum" in q)
        and ("saving" in q or "savings" in q)
        and "vendor" in q
    ):
        return "lowest_vendor_savings"

    # Defect rate
    if (
        ("highest" in q or "worst" in q or "maximum" in q)
        and "defect" in q
    ):
        return "highest_defect"

    if (
        ("lowest" in q or "best" in q or "minimum" in q)
        and "defect" in q
    ):
        return "lowest_defect"

    # Quality
    if (
        ("highest" in q or "best" in q or "maximum" in q)
        and "quality" in q
    ):
        return "highest_quality"

    if (
        ("lowest" in q or "worst" in q or "minimum" in q)
        and "quality" in q
    ):
        return "lowest_quality"

    # Risk
    if "risk" in q:
        return "highest_risk"

    # Delivery
    if (
        ("fastest" in q or "quickest" in q or "lowest" in q)
        and "vendor" in q
        and "delivery" in q
    ):
        return "fastest_vendor"

    # Category spending
    if (
        ("highest" in q or "top" in q or "maximum" in q)
        and ("spend" in q or "spending" in q)
        and "categor" in q
    ):
        return "highest_category_spend"

    # Category savings
    if (
        ("highest" in q or "top" in q or "maximum" in q)
        and ("saving" in q or "savings" in q)
        and "categor" in q
    ):
        return "highest_category_savings"

    # Averages
    if "average" in q and "delivery" in q:
        return "average_delivery"

    if "average" in q and "defect" in q:
        return "average_defect"

    if "average" in q and "quality" in q:
        return "average_quality"

    # Totals
    if "total" in q and ("spend" in q or "spending" in q):
        return "total_spend"

    if "total" in q and ("saving" in q or "savings" in q):
        return "total_savings"

    if (
        ("total" in q and "order" in q)
        or "number of orders" in q
        or "how many orders" in q
    ):
        return "total_orders"

    # Cost optimization
    if any(x in q for x in [
        "reduce cost",
        "reduce costs",
        "reduce procurement cost",
        "reduce procurement costs",
        "reduce our cost",
        "reduce our costs",
        "cost reduction",
        "cost optimization",
        "cost optimise",
        "cost optimize",
        "save cost",
        "save costs",
        "procurement optimization",
        "procurement optimisation",
        "where can we save"
    ]):
        return "cost_optimization"

    # Improvement
    if "improve" in q or "improvement" in q:
        return "vendor_improvement"

    return "general"


# ---------------------------------------------------------
# FACTUAL ANSWER
# Python calculates the facts first.
# Ollama only rewrites the factual answer.
# ---------------------------------------------------------
def factual_answer(question_type):

    if question_type == "highest_vendor_spend":
        row = vendor.loc[vendor["Total_Spend"].idxmax()]
        return (
            f"{row['Supplier']} has the highest total spending at "
            f"{row['Total_Spend']:,.2f}."
        )

    if question_type == "lowest_vendor_spend":
        row = vendor.loc[vendor["Total_Spend"].idxmin()]
        return (
            f"{row['Supplier']} has the lowest total spending at "
            f"{row['Total_Spend']:,.2f}."
        )

    if question_type == "highest_vendor_savings":
        row = vendor.loc[vendor["Total_Savings"].idxmax()]
        return (
            f"{row['Supplier']} has the highest total savings at "
            f"{row['Total_Savings']:,.2f}."
        )

    if question_type == "lowest_vendor_savings":
        row = vendor.loc[vendor["Total_Savings"].idxmin()]
        return (
            f"{row['Supplier']} has the lowest total savings at "
            f"{row['Total_Savings']:,.2f}."
        )

    if question_type == "highest_defect":
        row = vendor.loc[vendor["Avg_Defect_Rate"].idxmax()]
        return (
            f"{row['Supplier']} has the highest average defect rate at "
            f"{row['Avg_Defect_Rate']:.2f}%."
        )

    if question_type == "lowest_defect":
        row = vendor.loc[vendor["Avg_Defect_Rate"].idxmin()]
        return (
            f"{row['Supplier']} has the lowest average defect rate at "
            f"{row['Avg_Defect_Rate']:.2f}%."
        )

    if question_type == "highest_quality":
        row = vendor.loc[vendor["Avg_Quality_Rate"].idxmax()]
        return (
            f"{row['Supplier']} has the highest average quality rate at "
            f"{row['Avg_Quality_Rate']:.2f}%."
        )

    if question_type == "lowest_quality":
        row = vendor.loc[vendor["Avg_Quality_Rate"].idxmin()]
        return (
            f"{row['Supplier']} has the lowest average quality rate at "
            f"{row['Avg_Quality_Rate']:.2f}%."
        )

    if question_type == "highest_risk":
        row = vendor.loc[vendor["Avg_Defect_Rate"].idxmax()]
        return (
            f"{row['Supplier']} has the highest risk based on its average "
            f"defect rate of {row['Avg_Defect_Rate']:.2f}%."
        )

    if question_type == "fastest_vendor":
        row = vendor.loc[vendor["Avg_Delivery_Days"].idxmin()]
        return (
            f"{row['Supplier']} has the fastest average delivery time at "
            f"{row['Avg_Delivery_Days']:.2f} days."
        )

    if question_type == "highest_category_spend":
        row = category.loc[category["Total_Spend"].idxmax()]
        return (
            f"{row['Item_Category']} has the highest total spending at "
            f"{row['Total_Spend']:,.2f}."
        )

    if question_type == "highest_category_savings":
        row = category.loc[category["Total_Savings"].idxmax()]
        return (
            f"{row['Item_Category']} has the highest total savings at "
            f"{row['Total_Savings']:,.2f}."
        )

    if question_type == "average_delivery":
        return f"The average delivery time is {avg_delivery:.2f} days."

    if question_type == "average_defect":
        return f"The average defect rate is {avg_defect:.2f}%."

    if question_type == "average_quality":
        return f"The average quality rate is {avg_quality:.2f}%."

    if question_type == "total_spend":
        return f"The total procurement spend is {total_spend:,.2f}."

    if question_type == "total_savings":
        return f"The total procurement savings are {total_savings:,.2f}."

    if question_type == "total_orders":
        return f"The total number of purchase orders is {total_orders}."

    if question_type == "cost_optimization":
        v = vendor.loc[vendor["Total_Spend"].idxmax()]
        c = category.loc[category["Total_Spend"].idxmax()]

        return (
            f"The main areas to review are {v['Supplier']}, with the highest "
            f"vendor spending of {v['Total_Spend']:,.2f}, and the "
            f"{c['Item_Category']} category, with the highest category "
            f"spending of {c['Total_Spend']:,.2f}. "
            f"The dataset does not directly quantify a future cost reduction."
        )

    if question_type == "vendor_improvement":
        d = vendor.loc[vendor["Avg_Defect_Rate"].idxmax()]
        s = vendor.loc[vendor["Total_Spend"].idxmax()]

        return (
            f"For quality improvement, review {d['Supplier']} because its "
            f"average defect rate is highest at {d['Avg_Defect_Rate']:.2f}%. "
            f"For spending optimization, review {s['Supplier']} because its "
            f"total spending is highest at {s['Total_Spend']:,.2f}."
        )

    return None


# ---------------------------------------------------------
# OLLAMA
# ---------------------------------------------------------
def ask_ollama(factual):
    prompt = f"""
You are a professional procurement assistant.

Rewrite the factual answer below in one or two clear business sentences.

STRICT RULES:
- Preserve every number exactly.
- Preserve every vendor name exactly.
- Preserve every category name exactly.
- Preserve highest and lowest exactly.
- Do not add a currency symbol unless it already exists.
- Do not add any new facts.
- Do not calculate anything.
- Do not mention these instructions.
- Output only the answer.

FACTUAL ANSWER:
{factual}
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False,
                "keep_alive": "10m",
                "options": {
                    "temperature": 0,
                    "num_predict": 100
                }
            },
            timeout=120
        )

        if response.status_code == 200:
            answer = response.json().get("response", "").strip()

            if answer:
                # Basic safety check:
                # If Ollama changes/removes important factual content,
                # use the deterministic Python answer instead.
                numbers = re.findall(
                    r"\d[\d,]*(?:\.\d+)?",
                    factual
                )

                important_numbers_ok = all(
                    number in answer for number in numbers
                )

                important_names = re.findall(
                    r"[A-Za-z]+_[A-Za-z]+",
                    factual
                )

                names_ok = all(
                    name in answer for name in important_names
                )

                if important_numbers_ok and names_ok:
                    return answer

    except Exception:
        pass

    return factual


# ---------------------------------------------------------
# WELCOME UI
# ---------------------------------------------------------
if len(st.session_state.get("messages", [])) == 0:
    st.markdown("""
    <div class="welcome-card">
        <div class="robot">🤖</div>
        <div class="welcome-heading">Your <span>Procurement AI Copilot</span></div>
        <div class="welcome-description">
            Ask natural-language questions about your procurement data.
            Explore vendor spending, savings, delivery performance, quality,
            risk and cost optimization with AI-powered answers.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    cards = [
        ("💰", "Spend Intelligence", "Analyze procurement spending"),
        ("🏢", "Vendor Intelligence", "Compare vendor performance"),
        ("📦", "Performance Analysis", "Delivery and quality insights"),
        ("🧠", "Natural Language AI", "Ask questions in simple English")
    ]

    for col, (icon, title, description) in zip((col1, col2, col3, col4), cards):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-description">{description}</div>
            </div>
            """, unsafe_allow_html=True)


# ---------------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# ---------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------
question = st.chat_input("Ask a procurement question...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.write(question)

    question_type = detect_question(question)
    factual = factual_answer(question_type)

    with st.chat_message("assistant"):
        if factual:
            answer = ask_ollama(factual)
        else:
            answer = (
                "I can answer questions about vendor spending, savings, "
                "defect rate, quality, delivery time, categories, orders, "
                "risk and cost optimization."
            )

        st.write(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )


# ---------------------------------------------------------
# SIDEBAR UI
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="ai-logo">🤖</div>
    <div class="ai-title">Procurement <span>AI</span></div>
    <div class="ai-subtitle">Intelligent Procurement Copilot</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ai-status">
        <div class="ai-status-title">● AI Assistant Ready</div>
        <div class="ai-status-text">
            Your procurement intelligence assistant is ready to answer data-related questions.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="nav-item nav-active">💬 &nbsp; AI Assistant</div>
    <div class="nav-item">📊 &nbsp; Procurement Insights</div>
    <div class="nav-item">🏢 &nbsp; Vendor Intelligence</div>
    <div class="nav-item">💰 &nbsp; Cost Analysis</div>
    <div class="nav-item">⚡ &nbsp; Performance</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-message">
        <b style="color:#dce5f2;">Smarter Procurement Decisions</b><br><br>
        Powered by local AI using Llama and Ollama.
    </div>
    """, unsafe_allow_html=True)
