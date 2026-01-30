import pandas as pd
import streamlit as st
import base64
import os

# --------- GOOGLE SHEET LINKS ---------
NFI_KIT_URL = "https://docs.google.com/spreadsheets/d/1QvzLka1SiYIeO2Q-MvdD8x3FG6Lvi_Kg/edit?usp=sharing"
WASH_KIT_URL = "https://docs.google.com/spreadsheets/d/10vFO5iylxERCNeBOM9a1s7j0s5bvAHhf/edit?usp=sharing&ouid=104741373340307322695&rtpof=true&sd=true"

# --------- PAGE CONFIG ---------
st.set_page_config(
    page_title="S N I R D – Data Explorer",
    layout="wide",
    page_icon="🌾"
)

'''st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True'''

st.markdown(
    """
    <style>
    /* Hide top menu */
    #MainMenu {display: none;}

    /* Hide header & footer */
    header {display: none;}
    footer {display: none;}

    /* Hide Streamlit Cloud controls */
    .stDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}

    /* Hide mobile bottom-right "Manage app" */
    div[role="button"][aria-label*="Manage"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True
)
# --------- STYLE ---------
st.markdown("""
<style>
html, body, .stApp {
    background-color: #ffffff !important;
    color: #1a1a1a !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #0a3d62 !important;
    font-weight: 700;
}

label {
    font-weight: 600 !important;
    color: #0b3c49 !important;
}

input[type=text],
textarea,
select,
.stTextInput>div>div>input {
    background-color: #f4fbfb !important;
    border: 2px solid #00796B !important;
    color: #102a43 !important;
    border-radius: 6px !important;
}

div[data-baseweb="select"] span {
    color: #102a43 !important;
}

div.stButton > button {
    background-color: #00796B !important;
    color: #ffffff !important;
    border-radius: 8px;
    padding: 8px 18px;
    font-weight: 600;
}

.stDataFrame, 
.stDataFrame td, 
.stDataFrame th {
    color: #1a1a1a !important;
    background-color: #ffffff !important;
}

div[data-testid="stSuccess"] {
    background-color: #E6FFFA !important;
    color: #064E3B !important;
    font-weight: 700 !important;
    font-size: 16px !important;
}

div[data-testid="stSuccess"] p,
div[data-testid="stSuccess"] span {
    color: #064E3B !important;
}

div[data-testid="stWarning"] {
    background-color: #FFF8E1 !important;
    color: #5D4037 !important;
}

div[data-testid="stError"] {
    background-color: #FDECEA !important;
    color: #B71C1C !important;
}

hr {
    border: 1px solid #80CBC4;
}
</style>
""", unsafe_allow_html=True)

# --------- HEADER IMAGE ---------
try:
    img_data = base64.b64encode(open("testing.png", "rb").read()).decode()
    st.markdown(
        f"<div style='text-align:center'><img src='data:image/png;base64,{img_data}' width='65%'></div>",
        unsafe_allow_html=True
    )
except:
    st.warning("Header image not found (testing.png)")

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- SESSION STATE -----------------
if "show_search" not in st.session_state:
    st.session_state.show_search = False
if "show_count" not in st.session_state:
    st.session_state.show_count = False

def show_search_ui():
    st.session_state.show_search = True
    st.session_state.show_count = False

def show_count_ui():
    st.session_state.show_count = True
    st.session_state.show_search = False

# ---------------- HELPER -----------------
def make_unique(cols):
    seen = {}
    new_cols = []
    for col in cols:
        col = str(col).strip()
        if col not in seen:
            seen[col] = 0
            new_cols.append(col)
        else:
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")
    return new_cols

# ---------------- LOAD EXCEL -----------------
FILE_PATH = "1021- India - Cyclon Montha - HH Survey Details - 30.12.25.xlsx"

if not os.path.exists(FILE_PATH):
    st.error("❌ Excel file not found")
    st.stop()

st.success("📁 Data loaded from local Excel file")

df = pd.read_excel(FILE_PATH, header=[1, 2, 3])
columns = [] 

for i in df.columns:
    if "Unnamed" in str(i[1]):
        col_name = i[0]
    elif "Unnamed" in str(i[2]):
        col_name = f"{i[0]}_{i[1]}"
    else:
        col_name = f"{i[0]}_{i[1]}_{i[2]}"
    columns.append(col_name)

dataset = pd.read_excel(FILE_PATH, header=None, skiprows=4)
dataset.columns = make_unique(columns)

if "Age" in dataset.columns:
    dataset["Age"] = pd.to_numeric(dataset["Age"], errors="coerce")

# ---------------- ACTION BUTTONS -----------------
st.markdown("### ⚙️ Choose Action")
c1, c2 = st.columns(2)

with c1:
    st.button("🔍 SEARCH RECORDS", on_click=show_search_ui, use_container_width=True)
with c2:
    st.button("📊 COUNT SUMMARY", on_click=show_count_ui, use_container_width=True)

# ---------------- SEARCH SECTION -----------------
if st.session_state.show_search:
    st.markdown("## 🔍 Search Records")

    # ---- KIT BUTTONS UNDER SEARCH ----
    st.markdown("### 🎒 Relief Kit Sheets")
    k1, k2 = st.columns(2)

    with k1:
        st.markdown(f"""
            <a href="{NFI_KIT_URL}" target="_blank">
                <button style="background:#00796B;color:white;padding:10px 22px;
                border:none;border-radius:8px;font-weight:600;width:100%;">
                🧺 NFI Kit Sheet
                </button>
            </a>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
            <a href="{WASH_KIT_URL}" target="_blank">
                <button style="background:#00796B;color:white;padding:10px 22px;
                border:none;border-radius:8px;font-weight:600;width:100%;">
                🚿 Wash Kit Sheet
                </button>
            </a>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ---- SEARCH FILTERS ----
    colA, colB, colC, colD = st.columns(4)
    m_name = colC.text_input("🛖 Ward Number").strip()
    p_name = colB.text_input("📍 Panchayat").strip()
    v_name = colA.text_input("🏘 Mandal Name").strip()
    # p_name = colB.text_input("📍 Panchayat").strip()
    # m_name = colC.text_input("🛖 Ward Number").strip()
    d_name = colD.text_input("🌏 District").strip()
    f_name = st.text_input("👨‍👩‍👦 Family Head").strip()

    col1, col2 = st.columns(2)
    category = col1.selectbox("📁 Category", ["select"] + sorted(dataset["Category"].dropna().unique()))
    caste = col2.selectbox("🧬 Caste", ["select"] + sorted(dataset["Caste"].dropna().unique()))

    cola, colb = st.columns(2)
    age = cola.selectbox("🎂 Age Group", ["select", "below 18", "18 to 50", "50 to 60", "above 60"])
    gender = colb.selectbox("⚥ Gender", ["select"] + sorted(dataset["Gender"].dropna().unique()))

    if st.button("▶ RUN SEARCH", type="primary"):
        result = dataset.copy()

        if v_name: result = result[result["Name of the Mandal"] == v_name]
        if p_name: result = result[result["Panchayat/ Area"] == p_name]
        if m_name: result = result[result["Ward Number"] == m_name]
        if d_name: result = result[result["District"] == d_name]
        if f_name: result = result[result["Family Head Name"] == f_name]
        if category != "select": result = result[result["Category"] == category]
        if caste != "select": result = result[result["Caste"] == caste]
        
        if age != "select":
            if age == "below 18":
                result = result[result["Age"] < 18]
            elif age == "18 to 50":
                result = result[(result["Age"] >= 18) & (result["Age"] < 50)]
            elif age == "50 to 60":
                result = result[(result["Age"] >= 50) & (result["Age"] < 60)]
            else:
                result = result[result["Age"] >= 60]

        if gender != "select": result = result[result["Gender"] == gender]


        st.success(f"✔ {len(result)} Records Found")
        st.dataframe(result.iloc[:, 1:-1], use_container_width=True, height=350)

# ---------------- COUNT SECTION -----------------
if st.session_state.show_count:
    st.markdown("## 📊 Count Summary")

    mandal = st.selectbox("🏘 Mandal Name", ["select"] + sorted(dataset["Name of the Mandal"].dropna().unique()))
    group = st.selectbox("👥 Group", ["select", "Children", "Handicapped"])
    gender = st.selectbox("⚧ Gender", ["select", "Male", "Female"])

    if st.button("▶ RUN COUNT"):
        result = dataset.copy()
        count = 0

        if mandal:
            result = result[result["Name of the Mandal"] == mandal]

        if group != "select" and gender != "select":
            col = (
                "Numer of Children_Male" if group == "Children" and gender == "Male"
                else "Numer of Children_Female" if group == "Children"
                else "Disability_Male" if gender == "Male"
                else "Disability_Female"
            )

            if col in result.columns:
                count = result[col].fillna(0).astype(int).sum()

        st.success(f"### ✔ Total Persons Count: **{count}**")













