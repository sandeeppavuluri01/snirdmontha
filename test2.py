import pandas as pd
import streamlit as st
import base64
import os

# --------- PAGE CONFIG ---------
st.set_page_config(
    page_title="S N I R D – Data Explorer",
    layout="wide",
    page_icon="🌾"
)

# --------- STYLE ---------
st.markdown("""
<style>
body, .stApp { background-color: #ffffff; }
hr { border: 1px solid #B2EBF2; }
label { font-weight: 600 !important; color: #004D40 !important; }

input[type=text], select, textarea, .stTextInput>div>div>input {
    background-color: #E0F2F1 !important;
    border: 2px solid #009688 !important;
    color: #004D40 !important;
    border-radius: 6px !important;
}

div.stButton > button {
    background-color: #009688 !important;
    color: white !important;
    border-radius: 8px;
    padding: 8px 18px;
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

# ---------------- HELPER: UNIQUE COLUMNS -----------------
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

# ---------------- LOAD EXCEL (NO UPLOAD) -----------------
FILE_PATH = "data/snir_data.xlsx"

if not os.path.exists(FILE_PATH):
    st.error("❌ Excel file not found at data/snir_data.xlsx")
    st.stop()

st.success("📁 Data loaded from local Excel file")

# ----- READ MULTI HEADER -----
df = pd.read_excel(FILE_PATH, header=[1, 2, 3])
columns = []

for i in df.columns:
    if "Unnamed" in str(i[1]):
        col_name = i[0]
    elif "Unnamed" in str(i[2]):
        col_name = f"{i[0]}_{i[1]}"
        if "Rs." in col_name:
            col_name = columns[-1] + "_Rs."
        elif "Value" in col_name:
            col_name = columns[-1] + "_Value"
    else:
        col_name = f"{i[0]}_{i[1]}_{i[2]}"
    columns.append(col_name)

# ----- READ DATA -----
dataset = pd.read_excel(FILE_PATH, header=None, skiprows=4)
dataset.columns = make_unique(columns)

# Convert Age safely
if "Age" in dataset.columns:
    dataset["Age"] = pd.to_numeric(dataset["Age"], errors="coerce")

# ---------------- ACTION BUTTONS -----------------
st.markdown("### ⚙️ Choose Action")
col1, col2 = st.columns(2)

with col1:
    st.button("🔍 SEARCH RECORDS", on_click=show_search_ui, use_container_width=True)
with col2:
    st.button("📊 COUNT SUMMARY", on_click=show_count_ui, use_container_width=True)

# ---------------- SEARCH SECTION -----------------
if st.session_state.show_search:
    st.markdown("## 🔍 Search Records")

    colA, colB, colC, colD = st.columns(4)
    v_name = colA.text_input("🏘 Mandal Name").strip()
    p_name = colB.text_input("📍 Panchayat").strip()
    m_name = colC.text_input("Ward No").strip()
    d_name = colD.text_input("🌏 District").strip()

    f_name = st.text_input("👨‍👩‍👦 Family Head").strip()

    col1, col2 = st.columns(2)
    category_options = ["select"] + sorted(dataset["Category"].dropna().unique().tolist())
    caste_options = ["select"] + sorted(dataset["Caste"].dropna().unique().tolist())

    category = col1.selectbox("📁 Category", category_options)
    caste = col2.selectbox("🧬 Caste", caste_options)

    col1, col2 = st.columns(2)
    age = col1.selectbox("🎂 Age Group", ["select", "below 18", "18 to 50", "50 to 60", "above 60"])

    filter_list = [v_name, p_name, m_name, d_name, f_name, category, caste, age]
    doc_list = [
        "Name of the Mandal",
