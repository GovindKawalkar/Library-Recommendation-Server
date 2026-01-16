import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import bcrypt
from datetime import date

# ---------------- OWNER CONFIG ----------------
OWNER_EMAIL = "Kawalkar123@gmail.com"
OWNER_REF_CODE = "Govi123"

OWNER_PASSWORD_HASH = bcrypt.hashpw(
    "GoviGod12".encode(), bcrypt.gensalt()
)

# ---------------- SESSION INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# ---------------- LOGIN PAGE ----------------
def login_page():
    st.title("📚 Library Recommendation Serv")
    st.subheader("🔐 Secure Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email == OWNER_EMAIL and bcrypt.checkpw(
            password.encode(), OWNER_PASSWORD_HASH
        ):
            st.session_state.logged_in = True
            st.session_state.role = "OWNER"
            st.session_state.user_name = "Govind Kawalkar"
            st.success("Owner login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ---------------- DASHBOARD ----------------
def dashboard():
    st.sidebar.title("📘 Menu")
    st.sidebar.write(f"👤 {st.session_state.user_name}")

    menu = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Book Catalog",
            "Upcoming Stock",
            "Available Stock",
            "Issue & Return Book",
            "New Stock Database",
            "Logout"
        ]
    )

    if menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()

    if menu == "Dashboard":
        show_dashboard()

    if menu == "New Stock Database":
        new_stock_database()

    else:
        st.info(f"📌 {menu} module coming soon")

# ---------------- DASHBOARD UI ----------------
def show_dashboard():
    st.title("📊 Dashboard Overview")

    col1, col2 = st.columns(2)

    # Sample chart data
    data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr"],
        "Books Issued": [120, 90, 150, 110]
    })

    with col1:
        st.subheader("📊 Monthly Analysis (Bar)")
        fig, ax = plt.subplots()
        ax.bar(data["Month"], data["Books Issued"])
        st.pyplot(fig)

    with col2:
        st.subheader("🥧 Category Usage (Pie)")
        fig2, ax2 = plt.subplots()
        ax2.pie(
            [40, 30, 20, 10],
            labels=["Science", "Arts", "Commerce", "Other"],
            autopct="%1.1f%%"
        )
        st.pyplot(fig2)

    st.subheader("📈 Progress Report")
    st.progress(70)

    st.subheader("📅 Upcoming Events & Holidays")
    st.write("📌 Book Fair – 15 Aug")
    st.write("📌 Library Holiday – 26 Jan")

# ---------------- NEW STOCK DATABASE ----------------
def new_stock_database():
    st.title("🆕 New Stock Database")

    if st.session_state.role != "OWNER":
        st.error("Only OWNER can access this feature")
        return

    st.subheader("➕ Create New Database")

    db_date = st.date_input("Select Date", date.today())
    db_name = f"Stock_{db_date.strftime('%d_%m_%Y')}"

    if st.button("Create Database"):
        if "databases" not in st.session_state:
            st.session_state.databases = []

        st.session_state.databases.append({
            "Database Name": db_name,
            "Date": db_date
        })

        st.success(f"Database {db_name} created")

    st.subheader("📂 Existing Databases")

    if "databases" in st.session_state:
        df = pd.DataFrame(st.session_state.databases)
        st.dataframe(df)
    else:
        st.info("No database created yet")

# ---------------- MAIN ----------------
if not st.session_state.logged_in:
    login_page()
else:
    dashboard()
