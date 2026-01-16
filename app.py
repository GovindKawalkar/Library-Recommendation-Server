import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import bcrypt
from datetime import date

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="Library Recommendation Server",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================== CUSTOM CSS ==================
def load_css(dark=False):
    if dark:
        st.markdown("""
        <style>
        body { background-color: #0e1117; color: white; }
        .card {
            background: #1e222d;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 0 15px rgba(0,0,0,0.4);
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .card {
            background: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)

# ================== OWNER CONFIG ==================
OWNER_EMAIL = "Kawalkar123@gmail.com"
OWNER_REF_CODE = "Govi123"
OWNER_PASSWORD_HASH = bcrypt.hashpw("GoviGod12".encode(), bcrypt.gensalt())

# ================== SESSION ==================
for key, val in {
    "logged_in": False,
    "role": None,
    "user_name": "",
    "dark_mode": False,
    "databases": []
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

load_css(st.session_state.dark_mode)

# ================== HEADER ==================
col1, col2 = st.columns([10, 1])
with col2:
    if st.button("🌗"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ================== LOGIN PAGE ==================
def login_page():
    st.markdown("<h2 style='text-align:center;'>📚 Library Recommendation Server</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3,4,3])
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🔐 Secure Login")

        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")

        if st.button("Login", use_container_width=True):
            if email == OWNER_EMAIL and bcrypt.checkpw(password.encode(), OWNER_PASSWORD_HASH):
                st.session_state.logged_in = True
                st.session_state.role = "OWNER"
                st.session_state.user_name = "Govind Kawalkar"
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.markdown("</div>", unsafe_allow_html=True)

# ================== SIDEBAR ==================
def sidebar_menu():
    st.sidebar.markdown("## 📘 Library Panel")
    st.sidebar.write(f"👤 **{st.session_state.user_name}**")

    return st.sidebar.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "📚 Book Catalog",
            "📦 Upcoming Stock",
            "✅ Available Stock",
            "🔄 Issue & Return",
            "🆕 New Stock Database",
            "🚪 Logout"
        ]
    )

# ================== DASHBOARD ==================
def dashboard():
    st.title("📊 Dashboard Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("📚 Total Books", "12,450")
    c2.metric("📖 Issued Today", "124")
    c3.metric("👥 Active Users", "842")

    st.markdown("---")

    col1, col2 = st.columns(2)

    data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr"],
        "Books Issued": [120, 90, 150, 110]
    })

    with col1:
        st.subheader("📊 Monthly Issue Analysis")
        fig, ax = plt.subplots()
        ax.bar(data["Month"], data["Books Issued"])
        st.pyplot(fig)

    with col2:
        st.subheader("🥧 Category Distribution")
        fig2, ax2 = plt.subplots()
        ax2.pie([40, 30, 20, 10],
                labels=["Science", "Arts", "Commerce", "Other"],
                autopct="%1.1f%%")
        st.pyplot(fig2)

    st.subheader("📈 Progress Report")
    st.progress(0.7)

    st.subheader("📅 Events & Holidays (Date-wise)")
    events = pd.DataFrame({
        "Date": [date(2026,1,26), date(2026,8,15)],
        "Event": ["Republic Day Holiday", "Independence Day – Book Fair"]
    })
    st.dataframe(events, use_container_width=True)

# ================== NEW STOCK DATABASE ==================
def new_stock_database():
    st.title("🆕 New Stock Database")

    if st.session_state.role != "OWNER":
        st.error("Only OWNER can access this module")
        return

    st.subheader("📂 Upload Stock File")
    file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

    if file:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.success("File uploaded successfully")
        st.dataframe(df, use_container_width=True)

        if st.button("Save to Database"):
            st.session_state.databases.append({
                "Name": file.name,
                "Rows": df.shape[0],
                "Date": date.today()
            })
            st.success("Database saved")

    st.subheader("📁 Existing Databases")
    if st.session_state.databases:
        st.dataframe(pd.DataFrame(st.session_state.databases), use_container_width=True)
    else:
        st.info("No database available")

# ================== MAIN ==================
if not st.session_state.logged_in:
    login_page()
else:
    menu = sidebar_menu()

    if menu == "📊 Dashboard":
        dashboard()
    elif menu == "🆕 New Stock Database":
        new_stock_database()
    elif menu == "🚪 Logout":
        st.session_state.logged_in = False
        st.rerun()
    else:
        st.info("🚧 Module under development")
