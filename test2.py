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

/* ---------- GLOBAL TEXT ---------- */
html, body, .stApp {
    background-color: #ffffff !important;
    color: #1a1a1a !important;   /* Dark readable text */
}

/* ---------- HEADINGS ---------- */
h1, h2, h3, h4, h5, h6 {
    color: #0a3d62 !important;
    font-weight: 700;
}

/* ---------- LABELS ---------- */
label {
    font-weight: 600 !important;
    color: #0b3c49 !important;
}

/* ---------- INPUTS ---------- */
input[type=text],
textarea,
select,
.stTextInput>div>div>input {
    background-color: #f4fbfb !important;
    border: 2px solid #00796B !important;
    color: #102a43 !important;   /* Strong contrast */
    border-radius: 6px !important;
}

/* ---------- SELECT BOX TEXT ---------- */
div[data-baseweb="select"] span {
    color: #102a43 !important;
}

/* ---------- BUTTONS ---------- */
div.stButton > button {
    background-color: #00796B !important;
    color: #ffffff !important;
    border-radius: 8px;
    padding: 8px 18px;
    font-weight: 600;
}

/* ---------- DATAFRAME TEXT ---------- */
.stDataFrame, 
.stDataFrame td, 
.stDataFrame th {
    color: #1a1a1a !important;
    background-color: #ffffff !important;
}

/* ---------- SUCCESS / WARNING / ERROR ---------- */
div[data-testid="stSuccess"] {
    background-color: #E8F5E9 !important;
    color: #1B5E20 !important;
}

div[data-testid="stWarning"] {
    background-color: #FFF8E1 !important;
    color: #5D4037 !important;
}

div[data-testid="stError"] {
    background-color: #FDECEA !important;
    color: #B71C1C !important;
}

/* ---------- HR ---------- */
hr {
    border: 1px solid #80CBC4;
}

</style>
""", unsafe_allow_html=True)


# st.markdown("""
# <style>
# body, .stApp { background-color: #ffffff; }
# hr { border: 1px solid #B2EBF2; }
# label { font-weight: 600 !important; color: #004D40 !important; }

# input[type=text], select, textarea, .stTextInput>div>div>input {
#     background-color: #E0F2F1 !important;
#     border: 2px solid #009688 !important;
#     color: #004D40 !important;
#     border-radius: 6px !important;
# }

# div.stButton > button {
#     background-color: #009688 !important;
#     color: white !important;
#     border-radius: 8px;
#     padding: 8px 18px;
# }
# </style>
# """, unsafe_allow_html=True)

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
FILE_PATH = "1021- India - Cyclon Montha - HH Survey Details - 30.12.25.xlsx"

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
    m_name = colC.text_input("Ward Number").strip()
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
        "Panchayat/ Area",
        "Ward Number",
        "District",
        "Family Head Name",
        "Category",
        "Caste",
        "Age"
    ]

    if st.button("▶ RUN SEARCH", type="primary"):
        result = dataset.copy()

        for i in range(len(filter_list)):
            if filter_list[i] in ["", "select"]:
                continue

            if doc_list[i] != "Age":
                result = result[result[doc_list[i]] == filter_list[i]]
            else:
                if age == "below 18":
                    result = result[result["Age"] < 18]
                elif age == "18 to 50":
                    result = result[(result["Age"] >= 18) & (result["Age"] < 50)]
                elif age == "50 to 60":
                    result = result[(result["Age"] >= 50) & (result["Age"] < 60)]
                else:
                    result = result[result["Age"] >= 60]

        st.success(f"✔ {len(result)} Records Found")
        st.dataframe(result.iloc[:, 1:-1], use_container_width=True, height=350)

# ---------------- COUNT SECTION -----------------
if st.session_state.show_count:
    st.markdown("## 📊 Count Summary")

    c_village = st.text_input("🏘 Mandal Name").strip()
    gender_category = st.selectbox("👥 Group", ["select", "Children", "Handicapped"])
    gender = st.selectbox("⚧ Gender", ["select", "Male", "Female"])

    if st.button("▶ RUN COUNT"):
        result = dataset.copy()
        count = 0

        if c_village:
            result = result[result["Name of the Mandal"] == c_village]

        if gender_category != "select" and gender != "select":
            if gender_category == "Children":
                col = "Numer of Children_Male" if gender == "Male" else "Numer of Children_Female"
            else:
                col = "Disability_Male" if gender == "Male" else "Disability_Female"

            if col in result.columns:
                result[col] = result[col].fillna(0).astype(int)
                count = result[col].sum()

        st.success(f"### ✔ Total Persons Count: **{count}**")




