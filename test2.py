import pandas as pd
import streamlit as st
from PIL import Image
import base64

# --------- PAGE CONFIG ---------
st.set_page_config(
    page_title="S N I R D – Data Explorer",
    layout="wide",
    page_icon="🌾"
)

# --------- CUSTOM TEAL THEME (INPUTS + BUTTONS + SUCCESS BOX UPDATED) ---------
st.markdown("""
<style>

/* Main background */
body, .stApp {
    background-color: #ffffff;
}

/* Header divider */
hr {
    border: 1px solid #B2EBF2;
}

/* Labels */
label {
    font-weight: 600 !important;
    color: #004D40 !important;
}

/* -------- INPUT FIELDS -------- */
input[type=text], select, textarea, .stTextInput>div>div>input {
    background-color: #E0F2F1 !important;
    border: 2px solid #009688 !important;
    color: #004D40 !important;
    border-radius: 6px !important;
    padding: 4px 10px !important;
    font-size: 15px !important;
}

input:hover, .stTextInput:hover input {
    border-color: #00796B !important;
}

input:focus, .stTextInput:focus-within input {
    border-color: #004D40 !important;
    box-shadow: 0 0 6px #80CBC4 !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background-color: #E0F2F1 !important;
    border: 2px solid #009688 !important;
    color: #004D40 !important;
    border-radius: 6px !important;
}

/* -------- BUTTONS -------- */
div.stButton > button {
    background-color: #009688 !important;
    color: white !important;
    border-radius: 8px;
    padding: 8px 18px;
    font-size: 16px;
    border: 1px solid #00796B;
}

div.stButton > button:hover {
    background-color: #00796B !important;
    border-color: #00695C !important;
}

/* -------- HEADERS -------- */
h2, h3, h4 {
    color: #004D40 !important;
    font-weight: 700 !important;
}

/* DataFrame header */
.dataframe thead th {
    background-color: #B2DFDB !important;
    color: #004D40 !important;
    font-weight: 700 !important;
}

/* -------- SUCCESS BOX -------- */
.stAlert {
    background-color: #00796B !important;
    border: 2px solid #009688 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

/* ----------- MODERN CENTERED HEADER IMAGE ----------- */
.header-box {
    width: 100%;
    display: flex;
    justify-content: center;
    margin-top: -10px;
    margin-bottom: 5px;
}

.header-img {
    width: 62%;
    max-width: 700px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0, 77, 64, 0.30);
}

</style>
""", unsafe_allow_html=True)

# --------- HEADER IMAGE (MODERN CENTERED) ---------
try:
    img_data = base64.b64encode(open("testing.png", "rb").read()).decode()
    st.markdown(
        f"""
        <div class="header-box">
            <img src="data:image/png;base64,{img_data}" class="header-img">
        </div>
        """,
        unsafe_allow_html=True
    )
except:
    st.warning("Header image not found. Please place testing.png in the same folder.")

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

# ---------------- FILE UPLOAD ------------------
st.markdown("### 📤 Upload Excel File")
file = st.file_uploader("Choose .xlsx file", type=["xlsx"])

if file:

    df = pd.read_excel(file, header=[1, 2, 3])
    columns = []

    for i in df.columns:
        if "Unnamed" in i[1]:
            col_name = i[0]
        elif "Unnamed" in i[2]:
            col_name = "_".join([i[0], i[1]])
            if "Rs." in col_name:
                col_name = columns[-1] + "_Rs."
            elif "Value" in col_name:
                col_name = columns[-1] + "_Value"
        else:
            col_name = "_".join([i[0], i[1], i[2]])
        columns.append(col_name)

    dataset = pd.read_excel(file, header=None)
    dataset.drop(index=[0, 1, 2, 3], axis=0, inplace=True)
    dataset.columns = columns
    
    '''dataset.columns = (
        dataset.columns
        .str.strip()
        .str.replace('\u00a0', ' ', regex=False)
    )'''


    # ---------------- ACTION BUTTONS ------------------
    st.markdown("### ⚙️ Choose Action")
    col1, col2 = st.columns(2)

    with col1:
        st.button("🔍 SEARCH RECORDS", on_click=show_search_ui, use_container_width=True)
    with col2:
        st.button("📊 COUNT SUMMARY", on_click=show_count_ui, use_container_width=True)

    # ---------------- SEARCH SECTION ------------------
    if st.session_state.show_search:
        st.markdown("## 🔍 Search Records")

        colA, colB, colC, colD = st.columns(4)
        with colA:
            v_name = st.text_input("🏘 Village")
        with colB:
            p_name = st.text_input("📍 Panchayat")
        with colC:
            m_name = st.text_input("🗺 Mandal")
        with colD:
            d_name = st.text_input("🌏 District")

        f_name = st.text_input("👨‍👩‍👦 Family Head")

        # col1, col2 = st.columns(2)
        # with col1:
        #     caste_options = dataset["Caste"].unique().tolist()
        #     caste_options.insert(0, "select")
        #     caste = st.selectbox("🧬 Caste", caste_options)

        # with col2:
        #     category_options = dataset["Category "].unique().tolist()
        #     category_options.insert(0, "select")
        #     category = st.selectbox("📁 Category", category_options)
            
        with col1:
            age = st.selectbox("🎂 Age Group", ["select", "Below 18", "18 to 50", "50 to 60", "Above 60"])
        with col2:
            cash_transfer = st.selectbox("Cash Transfer",["select","Completed","Pending"])

        # AFTER reading Excel
    
       filter_list = [v_name, p_name, m_name, d_name, f_name, caste, category, age, cash_transfer]
        doc_list = ["Village Name", "Panchayat/ Area", "Mandal", "District",
                    "Family Head Name" , "Caste", "Category ", "Age","CASH Transfer"]

        if st.button("▶ RUN SEARCH", type="primary"):
            result = dataset.copy()

            for i in range(len(filter_list)):
                if filter_list[i] in ['', 'select']:
                    continue
                else:
                    if doc_list[i] != "Age":
                        result = result[result[doc_list[i]] == filter_list[i]]
                    else:
                        if filter_list[i] == "Below 18":
                            result = result[result["Age"] < 18]
                        elif filter_list[i] == "18 to 50":
                            result = result[(result["Age"] >= 18) & (result["Age"] < 50)]
                        elif filter_list[i] == "50 to 60":
                            result = result[(result["Age"] >= 50) & (result["Age"] < 60)]
                        else:
                            result = result[result["Age"] >= 60]

            st.success(f"✔ {len(result)} Records Found")
            st.dataframe(result, use_container_width=True, height=350)

    # ---------------- COUNT SECTION ------------------
    if st.session_state.show_count:
        st.markdown("## 📊 Count Summary")

        c_village = st.text_input("🏘 Village Name")
        gender_categrory = st.selectbox("👥 Group", ["select", "Children", "Handicapped"])
        gender = st.selectbox("⚧ Gender", ["select", "Male", "Female"])

        if st.button("▶ RUN COUNT"):
            result = dataset.copy()

            if c_village != "":
                result = result[result["Village Name"] == c_village]

            if gender_categrory != "select":
                if gender_categrory == "Children":
                    if gender == "Male":
                        result = result[result["Numer of Child_Male"] > 0]
                        count = result["Numer of Child_Male"].sum()
                    else:
                        result = result[result["Numer of Child_Female"] > 0]
                        count = result["Numer of Child_Female"].sum()
                else:
                    if gender == "Male":
                        result = result[result["Physically Challanged Persons_Male"] > 0]
                        count = result["Physically Challanged Persons_Male"].sum()
                    else:
                        result = result[result["Physically Challanged Persons_Female"] > 0]
                        count = result["Physically Challanged Persons_Female"].sum()

            st.success(f"### ✔ Total Count: **{count}**")













