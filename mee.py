import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import json
import os
import time
import calendar
from datetime import datetime, timedelta
import datetime as dt

# 🔹 Add here — before any UI layout code
st.markdown("""
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<style>
/* Hide any element that literally contains 'keyboard_arrow_right' */
:contains("keyboard_arrow_right") {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ---- Your app code starts here ----


if st.session_state.get("logged_in"):  # Only run after login
    st.markdown("""
        <style>
            /* Fix top white space */
            .main .block-container {
                padding-top: 0rem !important;
                margin-top: -2rem !important;
            }

            /* Hide top white header if Streamlit adds it */
            header, .st-emotion-cache-18ni7ap {
                display: none !important;
            }

            /* Body & app styling */
            html, body, .stApp {
                background: linear-gradient(to bottom right, #f5f5f5, #e1e4ec, #d3d7e6) !important;
                font-family: 'Footlight MT Light', serif !important;
                margin: 0 !important;
                padding: 0 !important;
            }

            h1, h2, h3, h4, h5, h6, label, p, span, div, li {
                font-family: 'Footlight MT Light', serif !important;
                font-weight: normal !important;
                text-shadow: none !important;
                background: none !important;
                box-shadow: none !important;
            }

            /* Input box visibility */
            input[type="text"], input[type="number"], textarea,
            .stTextInput > div > input, .stDateInput input,
            .stSelectbox > div > div {
                background-color: #ffffff !important;
                color: #000000 !important;
                border: 1px solid #ccc !important;
                border-radius: 6px !important;
                padding: 6px !important;
            }

            /* Remove the annoying » double arrow */
            .css-1aumxhk.e1fqkh3o2::before {
                content: none !important;
            }
        </style>
    """, unsafe_allow_html=True)



# --- Notes load/save functions ---
def load_notes():
    if os.path.exists("notes_data.json"):
        with open("notes_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_notes(notes_data):
    with open("notes_data.json", "w", encoding="utf-8") as f:
        json.dump(notes_data, f, indent=4)


# ---------------- CONFIG ----------------
st.set_page_config(page_title="Spendtel Tracker", layout="wide")

# ---------- FILE PATHS ----------
data_file = "finance_data.json"
user_file = "user_credentials.json"
session_file = "session.json"

import streamlit as st
import time

# --- Session State Init --- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_time" not in st.session_state:
    st.session_state.login_time = None

# --- Auto-Logout After 30 Min --- #
import time
import streamlit as st

# --- Session Timeout Handling --- #
if st.session_state.get("logged_in") and st.session_state.get("login_time"):
    session_duration = time.time() - st.session_state["login_time"]
    if session_duration > 1800:
        st.session_state.logged_in = False
        st.session_state.login_time = None  # Clear the login_time
        st.warning("Session expired. Please log in again.")
        st.stop()

# --- Login Function --- #
import streamlit as st
import time

import streamlit as st
import time


def login():
    st.markdown("""
        <style>
            /* Whole app background: Aqua to Dark Navy gradient */
            .stApp {
                background: linear-gradient(135deg, #00c9a7, #1a1a2e); /* Aqua to dark navy */
                background-attachment: fixed;
                background-repeat: no-repeat;
                background-size: cover;
                color: white;
                font-family: "Segoe UI", sans-serif;
                min-height: 100vh;
            }

            .main > div {
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }

            /* Login form container (glass effect) */
            .block-container {
                background-color: rgba(0, 0, 0, 0.4);  /* semi-transparent dark overlay */
                padding: 2rem;
                border-radius: 16px;
                box-shadow: 0 0 25px rgba(0,0,0,0.6);
                backdrop-filter: blur(10px);
            }

            h5 {
                text-align: center;
                color: white;
                font-weight: bold;
                margin-bottom: 20px;
            }

            .stTextInput>div>div>input {
                background-color: rgba(255, 255, 255, 0.15);
                color: Black;
                border: 1px solid #cccccc40;
                border-radius: 8px;
                padding: 10px;
            }

            .stTextInput>div>label {
                color: #eeeeee;
                font-size: 14px;
                margin-bottom: 5px;
            }

            .stButton>button {
                background-color: #007c70;  /* dark aqua */
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                width: 100%;
                font-weight: bold;
            }

            .footer {
                text-align: center;
                margin-top: 10px;
                font-size: 12px;
                color: #dddddd;
            }
        </style>
    """, unsafe_allow_html=True)


    # Create two columns (left for logo, right for login)
    left, right = st.columns([6, 4])

    with left:
        st.markdown(
            """
            <div style="height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center;
                        background: linear-gradient(to bottom right, #0f2027, #203a43, #2c5364); color:white;">
                <div style="font-size:60px; font-weight:bold;">Spendtel</div>
                <div style="font-size:18px; font-weight:normal; margin-top:10px;">Track Your Spending</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:
        # Add vertical space at the top (adjust 150px as needed)
        st.markdown("<div style='margin-top: 150px;'></div>", unsafe_allow_html=True)

        # Centered heading
        st.markdown("<h3 style='text-align:center;'>Login to Continue</h3>", unsafe_allow_html=True)

        # Username input
        username = st.text_input("", value="", key="user_input", label_visibility="collapsed",
                                 placeholder="Enter username")

        # Password input
        password = st.text_input("", value="", key="pass_input", label_visibility="collapsed",
                                 placeholder="Enter password", type="password")

        # Login button
        if st.button("Login"):
            users = {"IamThel": "methel", "admin": "admin123"}
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.login_time = time.time()
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")

        # Footer note
        st.markdown('<div class="footer" style="margin-top: 20px;">Forgot password? Not yet implemented.</div>',
                    unsafe_allow_html=True)
        st.markdown('<div class="footer">Spendtel • Designed by Methel</div>', unsafe_allow_html=True)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()


# ---------- LOAD & SAVE DATA ----------
def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            return json.load(f)
    return {"transactions": [], "piggy_bank": 0, "savings_goal": 0, "notes": ""}

def save_data(data):
    with open(data_file, "w") as f:
        json.dump(data, f, indent=4, default=str)

data = load_data()

# ---------- CORE FUNCTIONS ----------
def add_transaction(date, category, amount, note, type_):
    today = datetime.date.today()
    last = st.session_state.last_log_date
    if last != today:
        if last == today - datetime.timedelta(days=1):
            st.session_state.streak += 1
        else:
            st.session_state.streak = 1
        st.session_state.last_log_date = today

    data["transactions"].append({
        "date": str(date),
        "category": category,
        "amount": float(amount),
        "note": note,
        "type": type_
    })
    save_data(data)

def get_balance():
    income = sum(txn["amount"] for txn in data["transactions"] if txn["type"] == "Income")
    expenses = sum(txn["amount"] for txn in data["transactions"] if txn["type"] == "Expense")
    piggy = data.get("piggy_bank", 0)
    return income - expenses - piggy


# ---------- BOTTOM MENU NAVIGATION ----------
menu = st.sidebar.radio("Menu", [
    "🏠 Dashboard", "📑 Financial Statement", "➕ Add Entry", "🐷 Savings", "📅 History", "📝 Notes",
    "📊 Statistics", "🧮 Calculator", "💰 Budget", "⚙️ Settings", "🔓 Logout"
])



if menu == "🏠 Dashboard":
    import os
    import json
    import datetime
    import pandas as pd
    import plotly.express as px

if menu == "🏠 Dashboard":
    st.title("📊 Dashboard Overview")

    df = pd.DataFrame(data["transactions"])

    # ---------- Load Functions ----------
    def load_income():
        if os.path.exists("income.json"):
            with open("income.json", "r") as f:
                return float(json.load(f).get("income", 0))
        return 0.0

    def save_income(income_amount):
        with open("income.json", "w") as f:
            json.dump({"income": income_amount}, f)

    # ---------- Session Initialization ----------
    if "user_income" not in st.session_state:
        st.session_state.user_income = load_income()

    if "max_expenses" not in st.session_state:
        st.session_state.max_expenses = {
            "Rent": 6500,
            "Electricity": 9000,
            "Water": 400,
            "Laundry": 1260,
            "Drinking Water": 120,
            "Transportation": 1365,
            "Food - Methel": 1050,
            "Food - Jeffrey": 1050,
            "Evening Meals": 3720,
            "Pamasahe - Jeff": 500,
            "Groceries": 4000,
            "Budget for Mom": 1000,
            "Sat/Sun": 2400,
            "Skin Care": 1000,
            "Other expenses": 5000,
        }

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date", ascending=False)
        total_expense = df[df["type"] == "Expense"]["amount"].sum()
    else:
        total_expense = 0.0

    # ---------- Edit Monthly Income ----------
    with st.expander(" "):
        new_income = st.number_input(
            "Enter your monthly income",
            min_value=0.0,
            value=st.session_state.user_income,
            step=500.0,
            format="%.2f"
        )
        if st.button("Update Income"):
            st.session_state.user_income = new_income
            save_income(new_income)
            st.success("Income updated!")

    # ---------- Auto Calculation of Current Balance ----------
    current_balance = st.session_state.user_income - total_expense

    # ---------- Metric Cards ----------
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₱{st.session_state.user_income:,.2f}")
    col2.metric("Total Expense", f"₱{total_expense:,.2f}")
    col3.metric("Current Balance", f"₱{current_balance:,.2f}", delta_color="inverse")

    # ---------- Pie Chart of Top Expense Categories ----------
    if not df.empty:
        category_sum = df[df["type"] == "Expense"].groupby("category")["amount"].sum().sort_values(ascending=False)
        if not category_sum.empty:
            fig = px.pie(names=category_sum.index, values=category_sum.values, title="Top Expense Categories")
            st.plotly_chart(fig, use_container_width=True)

    # ---------- Budget Summary with Limit Checks ----------
    if not df.empty:
        st.subheader("📌 Category Budget Summary")

        for category, limit in st.session_state.max_expenses.items():
            spent = df[(df["type"] == "Expense") & (df["category"] == category)]["amount"].sum()

            col1, col2 = st.columns([3, 7])
            with col1:
                st.markdown(f"**{category}**")
            with col2:
                if spent > limit:
                    st.error(f"Spent ₱{spent:,.2f} / ₱{limit:,.2f} ⚠️ Over budget!")
                else:
                    st.success(f"Spent ₱{spent:,.2f} / ₱{limit:,.2f}")
    else:
        st.info("No transactions yet.")



import streamlit as st
import datetime

# Session state initializations
if "max_expenses" not in st.session_state:
    st.session_state.max_expenses = {
        "Rent": 6500,
        "Electricity": 9000,
        "Water": 400,
        "Laundry": 1260,
        "Drinking Water": 120,
        "Transportation": 1365,
        "Food - Methel": 1050,
        "Food - Jeffrey": 1050,
        "Evening Meals": 3720,
        "Pamasahe - Jeff": 500,
        "Groceries": 4000,
        "Budget for Mom": 1000,
        "Sat/Sun": 2400,
        "Skin Care": 1000,
        "Other expenses": 5000,
    }

if "last_log_date" not in st.session_state:
    st.session_state.last_log_date = None


elif menu == "➕ Add Entry":
    st.title("➕ Add New Entry")

    date = st.date_input("Date", value=datetime.date.today())
    category = st.selectbox("Category", list(st.session_state.max_expenses.keys()))
    amount = st.number_input("Amount", min_value=0.0)
    note = st.text_input("Note")
    type_ = st.selectbox("Type", ["Expense", "Income"])

    if st.button("Add Transaction"):
        # 🔁 Replace this with your actual function to store the entry
        add_transaction(date, category, amount, note, type_)
        st.success("Transaction added successfully!")

        # 🚨 Overspending check
        if type_ == "Expense" and amount > st.session_state.max_expenses.get(category, float('inf')):
            st.error(f"⚠️ Overspending Alert: You went over the ₱{st.session_state.max_expenses[category]:,.2f} limit for {category}!")


elif menu == "🐷 Savings":
    st.subheader("🐷 Savings Goal")

    import os
    import json

    # File where savings data is stored
    SAVINGS_FILE = "savings.json"

    # Load savings from file
    def load_savings():
        if os.path.exists(SAVINGS_FILE):
            with open(SAVINGS_FILE, "r") as f:
                data = json.load(f)
                return data.get("current_savings", 0.0), data.get("target_savings", 0.0)
        return 0.0, 0.0

    # Save savings to file
    def save_savings(current, target):
        with open(SAVINGS_FILE, "w") as f:
            json.dump({"current_savings": current, "target_savings": target}, f)

    # Load saved values
    current_savings, target_savings = load_savings()

    # Inputs for user
    col1, col2 = st.columns(2)
    with col1:
        current_input = st.number_input("💰 Current Savings", min_value=0.0, value=current_savings, step=100.0)
    with col2:
        target_input = st.number_input("🎯 Target Savings", min_value=0.0, value=target_savings, step=100.0)

    # Buttons
    col3, col4 = st.columns(2)
    with col3:
        if st.button("✅ Update Savings"):
            save_savings(current_input, target_input)
            st.success("Savings updated!")

    with col4:
        if st.button("🔄 Reset Savings"):
            save_savings(0.0, 0.0)
            st.success("Savings reset to zero!")

    # Reload after any save/reset
    current_savings, target_savings = load_savings()

    # Show progress if target is set
    if target_savings > 0:
        percent = (current_savings / target_savings) * 100
        st.markdown(f"**📊 Progress: {percent:.2f}%**")
        st.progress(min(1.0, percent / 100))
    else:
        st.info("Set a target savings amount to see progress.")


elif menu == "📅 History":
    st.title("📅 Transaction History")
    df = pd.DataFrame(data["transactions"])

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date", ascending=False)

        # ---------- Filters ----------
        with st.expander("🔍 Filter Options"):
            category_filter = st.multiselect("Filter by Category", options=df["category"].unique())
            date_range = st.date_input("Filter by Date Range", [])

            filtered_df = df.copy()

            if category_filter:
                filtered_df = filtered_df[filtered_df["category"].isin(category_filter)]
            if len(date_range) == 2:
                start_date, end_date = date_range
                filtered_df = filtered_df[
                    (filtered_df["date"].dt.date >= start_date) & (filtered_df["date"].dt.date <= end_date)
                ]

        # ---------- Assign unique ID for each row ----------
        def generate_id(row):
            return f"{pd.to_datetime(row['date']).strftime('%Y-%m-%d')}_{row['category']}_{float(row['amount']):.2f}_{row.get('note', '').strip()}"

        df["id"] = df.apply(generate_id, axis=1)
        filtered_df["id"] = filtered_df.apply(generate_id, axis=1)

        if not filtered_df.empty:
            st.subheader("🗂️ Filtered Transactions")

            for i, row in filtered_df.iterrows():
                with st.container():
                    cols = st.columns([4, 3, 2, 2, 1])
                    cols[0].markdown(f"**📅 {row['date'].strftime('%Y-%m-%d')}**")
                    cols[1].markdown(f"**🏷️ {row['category']}**")
                    cols[2].markdown(f"**₱{row['amount']:,.2f}**")
                    cols[3].markdown(f"📝 {row.get('note', '')}")

                    # Confirm delete flag
                    confirm_key = f"confirm_delete_{row['id']}"
                    if confirm_key not in st.session_state:
                        st.session_state[confirm_key] = False

                    if not st.session_state[confirm_key]:
                        if cols[4].button("Del.", key=f"delete_{row['id']}"):
                            st.session_state[confirm_key] = True
                    else:
                        cols[4].warning("Confirm delete?")
                        if cols[4].button("✅ Yes, Delete", key=f"confirm_btn_{row['id']}"):
                            # Load original data and assign IDs
                            original_df = pd.DataFrame(data["transactions"])
                            original_df["id"] = original_df.apply(generate_id, axis=1)

                            # Delete matching row
                            updated_df = original_df[original_df["id"] != row["id"]]

                            # Save
                            data["transactions"] = updated_df.drop(columns="id").to_dict(orient="records")
                            save_data(data)

                            st.success("✅ Deleted successfully.")
                            st.experimental_rerun()

        else:
            st.info("No transactions match your filter.")
    else:
        st.info("No history to show.")

elif menu == "📝 Notes":
    import json
    import os
    import datetime

    NOTES_FILE = "notes.json"

    def load_notes():
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_notes(notes):
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            json.dump(notes, f, indent=4)

    notes = load_notes()

    st.title("📝 My Simple Notes")

    new_note = st.text_area("Write your note here")

    if st.button("➕ Save Note"):
        if new_note.strip():
            note_data = {
                "text": new_note.strip(),
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            notes.insert(0, note_data)
            save_notes(notes)
            st.success("Note saved!")
        else:
            st.warning("Note is empty.")

    st.subheader("📚 Saved Notes")
    if notes:
        for i, note in enumerate(notes):
            with st.expander(f"{note['timestamp']}"):
                st.write(note["text"])
                if st.button(f"🗑 Delete", key=f"delete_{i}"):
                    notes.pop(i)
                    save_notes(notes)
                    st.rerun()
    else:
        st.info("No notes yet.")

elif menu == "📊 Statistics":
        st.title("📊 Monthly Summary")

        import pandas as pd
        import datetime
        import plotly.express as px

        data = load_data()
        transactions = data.get("transactions", [])
        monthly_income = st.session_state.get("user_income", 0.0)

        # Convert transactions to DataFrame
        df = pd.DataFrame(transactions)
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            current_month = datetime.datetime.now().month
            current_year = datetime.datetime.now().year
            df_month = df[(df["date"].dt.month == current_month) & (df["date"].dt.year == current_year)]
        else:
            df = pd.DataFrame(columns=["date", "type", "amount", "category"])
            df_month = df.copy()

        total_income = monthly_income  # This comes from user input
        total_expense = df[df["type"] == "Expense"]["amount"].sum()

        # ---------- Edit Monthly Income ----------
        with st.expander("💰 Edit Total Monthly Income"):
            new_income = st.number_input(
                "Enter your monthly income",
                min_value=0.0,
                value=monthly_income,
                step=500.0,
                format="%.2f"
            )


            def save_income(income):
                data = load_data()
                data["monthly_income"] = income
                save_data(data)


            if st.button("Update Income"):
                st.session_state.user_income = new_income
                save_income(new_income)
                st.success("Income updated!")

        # ---------- Auto Calculation of Current Balance ----------
        current_balance = st.session_state.user_income - total_expense

        # Summary Display
        st.markdown("### 💰 Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Income", f"₱{total_income:,.2f}")
        col2.metric("Total Expenses", f"₱{total_expense:,.2f}")
        col3.metric("Balance", f"₱{current_balance:,.2f}")

        # Daily Averages
        days_active = df_month["date"].nunique()
        if days_active > 0:
            st.subheader("📅 Daily Averages")
            st.write(f"Total Income: ₱{monthly_income / days_active:,.2f}")
            st.write(f"Estimated Expense: ₱{total_expense / days_active:,.2f}")

        # Top Categories (Bar Chart)
        st.subheader("📌 Top Expense Categories")
        top_cat = df_month[df_month["type"] == "Expense"].groupby("category")["amount"].sum()
        if not top_cat.empty:
            st.bar_chart(top_cat.sort_values(ascending=False))

        import pandas as pd
        import streamlit as st

        import pandas as pd
        import streamlit as st

        st.subheader("📈 Spending Trend")

        # Dropdown to select frequency
        time_freq = st.selectbox(
            "Select time range:",
            ["Daily", "Weekly (Mon–Sun)", "Weekly (4 Weeks)", "Monthly", "Yearly"]
        )

        # Filter for only Expense type and ensure date format
        df_expense = df[df["type"] == "Expense"].copy()
        df_expense["date"] = pd.to_datetime(df_expense["date"])

        # Daily view
        if time_freq == "Daily":
            trend = df_expense.groupby(df_expense["date"].dt.date)["amount"].sum()

        # Weekly (Mon–Sun calendar week)
        elif time_freq == "Weekly (Mon–Sun)":
            df_expense["week_start"] = df_expense["date"].dt.to_period("W").apply(lambda r: r.start_time)
            df_expense["week_end"] = df_expense["week_start"] + pd.Timedelta(days=6)

            df_expense["week_range"] = df_expense.apply(
                lambda row: f"{row['week_start'].strftime('%b %d')} – {row['week_end'].strftime('%b %d')}",
                axis=1
            )
            trend = df_expense.groupby("week_range")["amount"].sum()

        # Weekly (4 fixed weeks per month)
        elif time_freq == "Weekly (4 Weeks)":
            df_expense["day"] = df_expense["date"].dt.day
            df_expense["month"] = df_expense["date"].dt.strftime("%B %Y")


            def assign_week(day):
                if day <= 7:
                    return "Week 1"
                elif day <= 14:
                    return "Week 2"
                elif day <= 21:
                    return "Week 3"
                elif day <= 28:
                    return "Week 4"
                else:
                    return "Week 5"


            df_expense["week_of_month"] = df_expense["day"].apply(assign_week)
            df_expense["month_week"] = df_expense["month"] + " - " + df_expense["week_of_month"]

            trend = df_expense.groupby("month_week")["amount"].sum()

        # Monthly
        elif time_freq == "Monthly":
            df_expense["month_year"] = df_expense["date"].dt.strftime("%B %Y")
            trend = df_expense.groupby("month_year")["amount"].sum()

        # Yearly
        elif time_freq == "Yearly":
            df_expense["year"] = df_expense["date"].dt.year
            trend = df_expense.groupby("year")["amount"].sum()

        # Display the chart
        st.line_chart(trend)

        # --- Filtered Section ---
        st.subheader("🔍 Filtered View")
        categories = df["category"].unique().tolist()
        selected_categories = st.multiselect("Select Categories", options=categories, default=categories)

        if not df.empty:
            start_date = st.date_input("Start Date", value=df["date"].min().date())
            end_date = st.date_input("End Date", value=df["date"].max().date())
        else:
            start_date = datetime.date.today()
            end_date = datetime.date.today()

        filtered_df = df[
            (df["category"].isin(selected_categories)) &
            (df["date"].dt.date >= start_date) &
            (df["date"].dt.date <= end_date)
            ]

        if filtered_df.empty:
            st.warning("No transactions match the selected filters.")
        else:
            total_expense_filtered = filtered_df[filtered_df["type"] == "Expense"]["amount"].sum()
            total_income_filtered = filtered_df[filtered_df["type"] == "Income"]["amount"].sum()

            st.metric("Filtered Expense", f"₱{total_expense_filtered:,.2f}")
            st.metric("Filtered Income", f"₱{total_income_filtered:,.2f}")

            # Pie Chart
            expense_by_category = filtered_df[filtered_df["type"] == "Expense"].groupby("category")["amount"].sum()
            if not expense_by_category.empty:
                fig = px.pie(
                    names=expense_by_category.index,
                    values=expense_by_category.values,
                    title="Filtered: Expenses by Category"
                )
                st.plotly_chart(fig, use_container_width=True)

            # Export to CSV
            csv = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Export Filtered Data", data=csv, file_name="filtered_transactions.csv", mime="text/csv")

elif menu == "📑 Financial Statement":
    st.title("📑 Weekly Financial Statement")

    import pandas as pd
    import datetime

    data = load_data()
    transactions = data.get("transactions", [])
    monthly_income = st.session_state.get("user_income", 0.0)

    # Ensure income_history exists
    income_history = data.get("income_history", [])

    # Add or update this week's income from Dashboard/Statistics
    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=today.weekday())
    week_end = week_start + datetime.timedelta(days=6)

    # Check if this week exists in income_history
    existing_week = next((e for e in income_history if e["week_start"] == str(week_start)), None)
    if existing_week:
        # Update income if changed
        if existing_week["Income"] != monthly_income:
            existing_week["Income"] = monthly_income
            data["income_history"] = income_history
            save_data(data)
    else:
        # Append new week income
        income_history.append({
            "week_start": str(week_start),
            "week_end": str(week_end),
            "Income": monthly_income
        })
        data["income_history"] = income_history
        save_data(data)

    # ---- Add Manual Past Income (before automatic tracking) ----
    manual_income_data = [
        {"week_start": "2025-07-21", "week_end": "2025-07-27", "Income": 9650},
        {"week_start": "2025-07-28", "week_end": "2025-08-03", "Income": 11650},
        {"week_start": "2025-08-04", "week_end": "2025-08-10", "Income": 13431},
    ]
    # Add manual incomes if missing
    for m in manual_income_data:
        if not any(e["week_start"] == m["week_start"] and e["week_end"] == m["week_end"] for e in income_history):
            income_history.append(m)
    # Save after adding manual entries
    data["income_history"] = income_history
    save_data(data)

    # Process transactions dataframe
    df = pd.DataFrame(transactions)
    if df.empty:
        st.info("No transactions found.")

    else:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        # Create week ranges for grouping
        df["week_start"] = df["date"] - pd.to_timedelta(df["date"].dt.weekday, unit="D")
        df["week_end"] = df["week_start"] + pd.Timedelta(days=6)

        # Group weekly expenses
        weekly_expenses = (
            df[df["type"] == "Expense"]
            .groupby(["week_start", "week_end"])["amount"]
            .sum()
            .reset_index(name="Expense")
        )

    # Income DataFrame
    income_df = pd.DataFrame(income_history)
    income_df["week_start"] = pd.to_datetime(income_df["week_start"])
    income_df["week_end"] = pd.to_datetime(income_df["week_end"])

    # Merge income and expenses on week_start & week_end
    merged = pd.merge(
        weekly_expenses,
        income_df,
        on=["week_start", "week_end"],
        how="outer"
    ).fillna(0)

    merged["Expense %"] = merged.apply(
        lambda row: f"{(row['Expense'] / row['Income'] * 100):.1f}%" if row["Income"] > 0 else "0.0%",
        axis=1
    )

    # Format Week column without time
    merged["Week"] = merged.apply(
        lambda row: f"{row['week_start'].strftime('%Y-%m-%d')} → {row['week_end'].strftime('%Y-%m-%d')}",
        axis=1
    )

    # Format Income and Expense with commas and peso sign
    merged["Income"] = merged["Income"].apply(lambda x: f"₱{x:,.2f}")
    merged["Expense"] = merged["Expense"].apply(lambda x: f"₱{x:,.2f}")

    # Sort latest week first
    merged = merged.sort_values("week_start", ascending=False)

    # Display table with Week, Income, Expense, Expense %
    st.dataframe(merged[["Week", "Income", "Expense", "Expense %"]], use_container_width=True)

    # Convert formatted Income and Expense back to numeric for plotting
    merged["Income_num"] = merged["Income"].str.replace('[₱,]', '', regex=True).astype(float)
    merged["Expense_num"] = merged["Expense"].str.replace('[₱,]', '', regex=True).astype(float)

    # Plot trend chart for Income vs Expense using numeric columns
    import plotly.express as px

    fig = px.line(
        merged,
        x="week_start",
        y=["Income", "Expense"],
        markers=True,
        title="Weekly Income vs Expense Trend"
    )
    st.plotly_chart(fig, use_container_width=True)



elif menu == "🧮 Calculator":
    st.title("🧮 Basic Calculator")
    num1 = st.number_input("Enter first number")
    num2 = st.number_input("Enter second number")
    operation = st.selectbox("Select Operation", ["Add", "Subtract", "Multiply", "Divide"])
    if st.button("Calculate"):
        result = None
        if operation == "Add":
            result = num1 + num2
        elif operation == "Subtract":
            result = num1 - num2
        elif operation == "Multiply":
            result = num1 * num2
        elif operation == "Divide":
            if num2 != 0:
                result = num1 / num2
            else:
                st.error("Cannot divide by zero")
        if result is not None:
            st.success(f"Result: {result}")

elif menu == "💰 Budget":
    st.title("💰 Allocated Budget")
    st.write("Below are the Spending Cap per category. These values cannot be changed.")

    CATEGORY_BUDGETS = {
        "Rent": 6500,
        "Electricity": 900,
        "Water": 400,
        "Laundry": 1260,
        "Drinking Water": 120,
        "Transportation": 1365,
        "Food - Methel": 1050,
        "Food - Jeffrey": 1050,
        "Evening Meals": 3720,
        "Pamasahe - Jeff": 500,
        "Groceries": 4000,
        "Budget for Mom": 1000,
        "Sat/Sun": 2400,
        "Skin Care": 1000,
        "Other expenses": 5000,
    }

    for cat, amount in CATEGORY_BUDGETS.items():
        st.markdown(f"**{cat}**: ₱{amount:,.2f}")


elif menu == "⚙️ Settings":
    st.title("⚙️ Category Settings")
    new_cat = st.text_input("Add New Category")
    if st.button("Add Category") and new_cat:
        if new_cat not in st.session_state.max_expenses:
            st.session_state.max_expenses[new_cat] = 0
            st.success("Category added!")
    if st.checkbox("Show All Categories"):
        st.json(st.session_state.max_expenses)


elif menu == "🔓 Logout":
    st.session_state.logged_in = False
    st.rerun()










