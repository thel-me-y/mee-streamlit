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




