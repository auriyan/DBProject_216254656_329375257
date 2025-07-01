# app.py
import streamlit as st
import psycopg2
import pandas as pd
from datetime import datetime
import time

# Configuration
st.set_page_config(
    page_title="Ski Rental System",
    page_icon="🎿",
    layout="wide"
)


# Database connection
@st.cache_resource
def init_connection():
    return psycopg2.connect(
        host="localhost",
        port = 5432,
        database="mydatabase",
        user="SkiMF",
        password="Aura123an"
    )


# Main navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["🏠 Home", "👥 Customers", "🎿 Equipment", "📋 Rentals",
     "🔗 Rental Equipment", "📊 Reports", "⚙ Functions",  "📝 Original Queries"]
)

if page == "🏠 Home":
    # הוסף CSS לרקע רק לדף הבית
    st.markdown("""
        <style>
        .stApp {
            background-image: url('https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        /* הוסף שכבת כיסוי כדי שהטקסט יהיה קריא */
        .stApp::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.85);
            z-index: -1;
        }

        /* עיצוב המטריקות */
        [data-testid="metric-container"] {
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🎿 Ski Rental Management System")

elif page == "👥 Customers":
    st.title("Customer Management")

    # CRUD tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 View All", "➕ Create", "✏ Update", "🗑 Delete"])

    conn = init_connection()

    with tab1:
        df = pd.read_sql("SELECT * FROM customer ORDER BY cid", conn)
        st.dataframe(df, use_container_width=True)

    with tab2:
        with st.form("create_customer"):
            cid = st.number_input("Customer ID", min_value=1)
            name = st.text_input("Full Name")
            phone = st.text_input("Phone")

            if st.form_submit_button("Create Customer"):
                cur = conn.cursor()
                try:
                    cur.execute(
                        "INSERT INTO customer (cid, full_name, phone) VALUES (%s, %s, %s)",
                        (cid, name, phone)
                    )
                    conn.commit()
                    st.success("✅ Customer created successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    conn.rollback()

elif page == "📋 Rentals":
    st.title("Rental Management")

    conn = init_connection()
    cur = conn.cursor()

    # טאבים לניהול השכרות
    tab1, tab2, tab3, tab4 = st.tabs(["📋 View Rentals", "➕ Create Rental", "🎿 Manage Equipment", "🗑 Delete Rental"])

    with tab1:
        # הצג השכרות קיימות
        query = """
            SELECT r.rid, c.full_name, e.fname || ' ' || e.lname as cashier,
                   r.start_date, r.end_date,
                   COUNT(re.eid) as equipment_count,
                   COALESCE(SUM(eq.daily_price * (r.end_date - r.start_date + 1)), 0) as total_cost
            FROM rental r
            JOIN customer c ON r.cid = c.cid
            JOIN employee e ON r.eid = e.eid
            LEFT JOIN rental_equipment re ON r.rid = re.rid
            LEFT JOIN equipment eq ON re.eid = eq.eid
            GROUP BY r.rid, c.full_name, e.fname, e.lname, r.start_date, r.end_date
            ORDER BY r.start_date DESC
        """
        df = pd.read_sql(query, conn)
        st.dataframe(df, use_container_width=True)

    with tab2:
        st.subheader("Create New Rental")

        # Step 1: בחר לקוח ופקיד
        col1, col2 = st.columns(2)

        with col1:
            customers = pd.read_sql("SELECT cid, full_name FROM customer ORDER BY full_name", conn)
            customer_id = st.selectbox(
                "Select Customer",
                customers['cid'].tolist(),
                format_func=lambda x: f"{customers[customers['cid'] == x]['full_name'].iloc[0]} (ID: {x})"
            )

        with col2:
            cashiers = pd.read_sql("""
                SELECT c.eid, e.fname || ' ' || e.lname as name 
                FROM cashier c 
                JOIN employee e ON c.eid = e.eid
                ORDER BY name
            """, conn)
            cashier_id = st.selectbox(
                "Select Cashier",
                cashiers['eid'].tolist(),
                format_func=lambda x: f"{cashiers[cashiers['eid'] == x]['name'].iloc[0]} (ID: {x})"
            )

        # Step 2: תאריכים
        col3, col4 = st.columns(2)
        with col3:
            start_date = st.date_input("Start Date", value=pd.Timestamp.now().date())
        with col4:
            end_date = st.date_input("End Date", value=pd.Timestamp.now().date() + pd.Timedelta(days=3))

        # Step 3: בחר ציוד
        st.subheader("Select Equipment")

        # הצג ציוד זמין
        available_equipment_query = """
            SELECT e.eid, e.type, e.daily_price,
                   CASE 
                       WHEN re.eid IS NULL THEN 'Available'
                       ELSE 'Rented'
                   END as status
            FROM equipment e
            LEFT JOIN (
                SELECT DISTINCT re.eid
                FROM rental_equipment re
                JOIN rental r ON re.rid = r.rid
                WHERE r.end_date >= %s AND r.start_date <= %s
            ) re ON e.eid = re.eid
            WHERE re.eid IS NULL
            ORDER BY e.type, e.eid
        """

        available_df = pd.read_sql(available_equipment_query, conn, params=[start_date, end_date])

        if not available_df.empty:
            # multiselect לבחירת ציוד
            selected_equipment = st.multiselect(
                "Choose Equipment",
                available_df['eid'].tolist(),
                format_func=lambda
                    x: f"{available_df[available_df['eid'] == x]['type'].iloc[0]} - ₪{available_df[available_df['eid'] == x]['daily_price'].iloc[0]}/day (ID: {x})"
            )

            # חשב עלות כוללת
            if selected_equipment:
                days = (end_date - start_date).days + 1
                total_cost = sum(available_df[available_df['eid'].isin(selected_equipment)]['daily_price']) * days
                st.info(f"Total Cost: ₪{total_cost:.2f} ({days} days)")

            # כפתור יצירה
            if st.button("Create Rental", type="primary"):
                if not selected_equipment:
                    st.error("Please select at least one equipment item")
                else:
                    try:
                        # התחל טרנזקציה
                        cur.execute("BEGIN")

                        # יצור השכרה
                        cur.execute("""
                            INSERT INTO rental (cid, eid, start_date, end_date)
                            VALUES (%s, %s, %s, %s)
                            RETURNING rid
                        """, (customer_id, cashier_id, start_date, end_date))

                        rental_id = cur.fetchone()[0]

                        # הוסף ציוד להשכרה
                        for equip_id in selected_equipment:
                            cur.execute("""
                                INSERT INTO rental_equipment (rid, eid)
                                VALUES (%s, %s)
                            """, (rental_id, equip_id))

                        conn.commit()
                        st.success(f"✅ Rental #{rental_id} created successfully!")
                        st.balloons()
                        st.rerun()

                    except Exception as e:
                        conn.rollback()
                        st.error(f"❌ Error: {e}")
        else:
            st.warning("No equipment available for the selected dates")

    with tab3:
        st.subheader("Manage Rental Equipment")

        # בחר השכרה לניהול
        active_rentals = pd.read_sql("""
            SELECT r.rid, c.full_name || ' - ' || r.start_date::text as display
            FROM rental r
            JOIN customer c ON r.cid = c.cid
            WHERE r.end_date >= CURRENT_DATE
            ORDER BY r.start_date DESC
        """, conn)

        if not active_rentals.empty:
            selected_rental = st.selectbox(
                "Select Rental to Manage",
                active_rentals['rid'].tolist(),
                format_func=lambda x: f"#{x} - {active_rentals[active_rentals['rid'] == x]['display'].iloc[0]}"
            )

            # הצג ציוד נוכחי בהשכרה
            current_equipment = pd.read_sql("""
                SELECT re.eid, e.type, e.daily_price
                FROM rental_equipment re
                JOIN equipment e ON re.eid = e.eid
                WHERE re.rid = %s
            """, conn, params=[selected_rental])

            st.write("Current Equipment in Rental:")
            st.dataframe(current_equipment)

            col1, col2 = st.columns(2)

            with col1:
                st.write("*Add Equipment*")

                # קבל תאריכי השכרה
                rental_dates = pd.read_sql(
                    "SELECT start_date, end_date FROM rental WHERE rid = %s",
                    conn, params=[selected_rental]
                ).iloc[0]

                # ציוד זמין שלא בהשכרה הנוכחית
                available_to_add = pd.read_sql("""
                    SELECT e.eid, e.type, e.daily_price
                    FROM equipment e
                    WHERE e.eid NOT IN (
                        SELECT eid FROM rental_equipment WHERE rid = %s
                    )
                    AND e.eid NOT IN (
                        SELECT re.eid
                        FROM rental_equipment re
                        JOIN rental r ON re.rid = r.rid
                        WHERE r.rid != %s
                        AND r.end_date >= %s 
                        AND r.start_date <= %s
                    )
                """, conn, params=[selected_rental, selected_rental,
                                   rental_dates['start_date'], rental_dates['end_date']])

                if not available_to_add.empty:
                    equipment_to_add = st.selectbox(
                        "Select Equipment to Add",
                        available_to_add['eid'].tolist(),
                        format_func=lambda
                            x: f"{available_to_add[available_to_add['eid'] == x]['type'].iloc[0]} - ₪{available_to_add[available_to_add['eid'] == x]['daily_price'].iloc[0]}/day"
                    )

                    if st.button("Add Equipment"):
                        try:
                            cur.execute("""
                                INSERT INTO rental_equipment (rid, eid)
                                VALUES (%s, %s)
                            """, (selected_rental, equipment_to_add))
                            conn.commit()
                            st.success("✅ Equipment added successfully!")
                            st.rerun()
                        except Exception as e:
                            conn.rollback()
                            st.error(f"❌ Error: {e}")
                else:
                    st.info("No available equipment to add")

            with col2:
                st.write("*Remove Equipment*")

                if not current_equipment.empty:
                    equipment_to_remove = st.selectbox(
                        "Select Equipment to Remove",
                        current_equipment['eid'].tolist(),
                        format_func=lambda
                            x: f"{current_equipment[current_equipment['eid'] == x]['type'].iloc[0]} (ID: {x})"
                    )

                    if st.button("Remove Equipment", type="secondary"):
                        if len(current_equipment) == 1:
                            st.error("Cannot remove the last equipment item. A rental must have at least one item.")
                        else:
                            try:
                                cur.execute("""
                                    DELETE FROM rental_equipment
                                    WHERE rid = %s AND eid = %s
                                """, (selected_rental, equipment_to_remove))
                                conn.commit()
                                st.success("✅ Equipment removed successfully!")
                                st.rerun()
                            except Exception as e:
                                conn.rollback()
                                st.error(f"❌ Error: {e}")
                else:
                    st.info("No equipment in this rental")
        else:
            st.info("No active rentals found")

    with tab4:
        st.subheader("Delete Rental")

        all_rentals = pd.read_sql("""
            SELECT r.rid, c.full_name || ' - ' || r.start_date::text as display
            FROM rental r
            JOIN customer c ON r.cid = c.cid
            ORDER BY r.rid DESC
        """, conn)

        if not all_rentals.empty:
            rental_to_delete = st.selectbox(
                "Select Rental to Delete",
                all_rentals['rid'].tolist(),
                format_func=lambda x: f"#{x} - {all_rentals[all_rentals['rid'] == x]['display'].iloc[0]}"
            )

            # הצג פרטי השכרה
            rental_details = pd.read_sql("""
                SELECT r.*, c.full_name, 
                       COUNT(re.eid) as equipment_count
                FROM rental r
                JOIN customer c ON r.cid = c.cid
                LEFT JOIN rental_equipment re ON r.rid = re.rid
                WHERE r.rid = %s
                GROUP BY r.rid, r.cid, r.eid, r.start_date, r.end_date, c.full_name
            """, conn, params=[rental_to_delete])

            st.write("Rental Details:")
            st.dataframe(rental_details)

            st.warning("⚠ Deleting a rental will also remove all associated equipment assignments!")

            if st.button("Delete Rental", type="secondary"):
                try:
                    # המחיקה תמחק אוטומטית גם מ-rental_equipment בגלל ON DELETE CASCADE
                    cur.execute("DELETE FROM rental WHERE rid = %s", (rental_to_delete,))
                    conn.commit()
                    st.success("✅ Rental deleted successfully!")
                    st.rerun()
                except Exception as e:
                    conn.rollback()
                    st.error(f"❌ Error: {e}")
        else:
            st.info("No rentals found")

elif page == "🔗 Rental Equipment":
    st.title("Rental Equipment Management")
    st.info("This manages the relationship between rentals and equipment")

    conn = init_connection()

    # Display current rental-equipment relationships
    query = """
        SELECT re.rid, re.eid, e.type, e.daily_price,
               r.start_date, r.end_date, c.full_name
        FROM rental_equipment re
        JOIN equipment e ON re.eid = e.eid
        JOIN rental r ON re.rid = r.rid
        JOIN customer c ON r.cid = c.cid
        ORDER BY r.start_date DESC
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df, use_container_width=True)



elif page == "📊 Reports":
    st.title("Reports & Queries")

    conn = init_connection()

    report_type = st.selectbox(
        "Select Report",
        ["Customer Spending Analysis", "Equipment Availability",
         "Top Revenue Customers", "Equipment Utilization Report",
         "Monthly Rental Statistics", "Revenue by Equipment Type"]
    )

    if report_type == "Customer Spending Analysis":
        customer_id = st.number_input("Enter Customer ID", min_value=1, value=1)

        if st.button("Run Analysis"):
            try:
                query = "SELECT * FROM calculate_customer_total_spending(%s)"
                df = pd.read_sql(query, conn, params=[customer_id])

                if not df.empty:
                    st.success("✅ Analysis Complete!")

                    # הצג את הנתונים
                    customer_data = df.iloc[0]

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Customer Name", customer_data['customer_name'])
                    with col2:
                        st.metric("Total Spent", f"₪{customer_data['total_spent']:.2f}")
                    with col3:
                        st.metric("VIP Status", "Yes" if customer_data['is_vip'] else "No")

                    # פירוט עלויות
                    st.write("Cost Breakdown:")
                    cost_data = {
                        'Category': ['Rentals', 'Lessons'],
                        'Amount': [customer_data['rental_costs'], customer_data['lesson_costs']]
                    }
                    st.bar_chart(pd.DataFrame(cost_data).set_index('Category'))

                else:
                    st.warning("No data found for this customer")

            except Exception as e:
                st.error(f"Error: {e}")

    elif report_type == "Equipment Availability":
        check_date = st.date_input("Select Date", value=pd.Timestamp.now().date())

        if st.button("Check Availability"):
            try:
                query = "SELECT * FROM find_available_equipment(%s)"
                df = pd.read_sql(query, conn, params=[check_date])

                if not df.empty:
                    st.success(f"✅ Found {len(df)} available items for {check_date}")
                    st.dataframe(df)
                else:
                    st.warning("No equipment available for this date")

            except Exception as e:
                st.error(f"Error: {e}")

    elif report_type == "Top Revenue Customers":
        if st.button("Generate Report"):
            try:
                # שאילתה לחישוב הלקוחות המובילים
                query = """
                    WITH customer_revenue AS (
                        SELECT 
                            c.cid,
                            c.full_name,
                            c.phone,
                            COALESCE(
                                (SELECT SUM(eq.daily_price * (r.end_date - r.start_date + 1))
                                 FROM rental r
                                 JOIN rental_equipment re ON r.rid = re.rid
                                 JOIN equipment eq ON re.eid = eq.eid
                                 WHERE r.cid = c.cid), 0
                            ) as rental_revenue,
                            COALESCE(
                                (SELECT SUM(p.amount)
                                 FROM payment p
                                 WHERE p.cid = c.cid), 0
                            ) as payment_revenue
                        FROM customer c
                    )
                    SELECT 
                        cid as "Customer ID",
                        full_name as "Name",
                        phone as "Phone",
                        rental_revenue as "Rental Revenue",
                        payment_revenue as "Lesson Revenue",
                        (rental_revenue + payment_revenue) as "Total Revenue"
                    FROM customer_revenue
                    WHERE (rental_revenue + payment_revenue) > 0
                    ORDER BY "Total Revenue" DESC
                    LIMIT 10
                """

                df = pd.read_sql(query, conn)

                if not df.empty:
                    st.success("✅ Top Revenue Customers Report")

                    # הצג מטריקות
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Top Customer", df.iloc[0]['Name'])
                    with col2:
                        st.metric("Highest Revenue", f"₪{df.iloc[0]['Total Revenue']:.2f}")
                    with col3:
                        st.metric("Average Revenue", f"₪{df['Total Revenue'].mean():.2f}")

                    # הצג טבלה
                    st.dataframe(df)

                    # הצג גרף
                    if len(df) > 1:
                        chart_data = df.set_index('Name')['Total Revenue'].head(5)
                        st.bar_chart(chart_data)
                else:
                    st.info("No revenue data found")

            except Exception as e:
                st.error(f"Error: {e}")

    elif report_type == "Equipment Utilization Report":
        if st.button("Generate Report"):
            try:
                query = """
                    SELECT 
                        e.eid as "Equipment ID",
                        e.type as "Type",
                        e.daily_price as "Daily Price",
                        COUNT(DISTINCT re.rid) as "Times Rented",
                        COALESCE(SUM(r.end_date - r.start_date + 1), 0) as "Total Days Rented",
                        COALESCE(SUM((r.end_date - r.start_date + 1) * e.daily_price), 0) as "Total Revenue"
                    FROM equipment e
                    LEFT JOIN rental_equipment re ON e.eid = re.eid
                    LEFT JOIN rental r ON re.rid = r.rid
                    GROUP BY e.eid, e.type, e.daily_price
                    ORDER BY "Times Rented" DESC
                """

                df = pd.read_sql(query, conn)

                if not df.empty:
                    st.success("✅ Equipment Utilization Report")

                    # הצג מטריקות
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        most_rented = df.iloc[0]['Type']
                        st.metric("Most Rented", most_rented)
                    with col2:
                        total_revenue = df['Total Revenue'].sum()
                        st.metric("Total Revenue", f"₪{total_revenue:.2f}")
                    with col3:
                        avg_utilization = df['Times Rented'].mean()
                        st.metric("Avg Rentals/Item", f"{avg_utilization:.1f}")

                    # הצג טבלה
                    st.dataframe(df)

                    # הצג גרף ניצולת
                    if len(df) > 1:
                        st.write("Rental Frequency by Equipment Type:")
                        chart_data = df.set_index('Type')['Times Rented']
                        st.bar_chart(chart_data)
                else:
                    st.info("No equipment data found")

            except Exception as e:
                st.error(f"Error: {e}")

    elif report_type == "Monthly Rental Statistics":
        year = st.number_input("Select Year", min_value=2020, max_value=2025, value=2024)

        if st.button("Generate Report"):
            try:
                query = """
                    SELECT 
                        EXTRACT(MONTH FROM r.start_date) as "Month",
                        COUNT(DISTINCT r.rid) as "Number of Rentals",
                        COUNT(DISTINCT r.cid) as "Unique Customers",
                        COUNT(DISTINCT re.eid) as "Equipment Items Rented",
                        COALESCE(SUM(eq.daily_price * (r.end_date - r.start_date + 1)), 0) as "Revenue"
                    FROM rental r
                    JOIN rental_equipment re ON r.rid = re.rid
                    JOIN equipment eq ON re.eid = eq.eid
                    WHERE EXTRACT(YEAR FROM r.start_date) = %s
                    GROUP BY EXTRACT(MONTH FROM r.start_date)
                    ORDER BY "Month"
                """

                df = pd.read_sql(query, conn, params=[year])

                if not df.empty:
                    st.success(f"✅ Monthly Statistics for {year}")

                    # הצג סיכום שנתי
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Rentals", df['Number of Rentals'].sum())
                    with col2:
                        st.metric("Total Revenue", f"₪{df['Revenue'].sum():.2f}")
                    with col3:
                        st.metric("Avg Monthly Revenue", f"₪{df['Revenue'].mean():.2f}")

                    # הצג טבלה
                    df['Month'] = df['Month'].astype(int)
                    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    df['Month Name'] = df['Month'].apply(lambda x: month_names[x - 1] if x <= 12 else 'Unknown')

                    st.dataframe(df)

                    # הצג גרף הכנסות חודשיות
                    st.write("Monthly Revenue Trend:")
                    chart_data = df.set_index('Month Name')['Revenue']
                    st.line_chart(chart_data)
                else:
                    st.info(f"No rental data found for {year}")

            except Exception as e:
                st.error(f"Error: {e}")

    elif report_type == "Revenue by Equipment Type":
        if st.button("Generate Report"):
            try:
                query = """
                    SELECT 
                        e.type as "Equipment Type",
                        COUNT(DISTINCT re.rid) as "Rentals",
                        COALESCE(SUM(e.daily_price * (r.end_date - r.start_date + 1)), 0) as "Revenue",
                        COALESCE(AVG(r.end_date - r.start_date + 1), 0) as "Avg Rental Days"
                    FROM equipment e
                    LEFT JOIN rental_equipment re ON e.eid = re.eid
                    LEFT JOIN rental r ON re.rid = r.rid
                    GROUP BY e.type
                    HAVING COUNT(DISTINCT re.rid) > 0
                    ORDER BY "Revenue" DESC
                """

                df = pd.read_sql(query, conn)

                if not df.empty:
                    st.success("✅ Revenue by Equipment Type")

                    # הצג מטריקות
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        top_type = df.iloc[0]['Equipment Type']
                        st.metric("Top Revenue Type", top_type)
                    with col2:
                        total_revenue = df['Revenue'].sum()
                        st.metric("Total Revenue", f"₪{total_revenue:.2f}")
                    with col3:
                        avg_days = df['Avg Rental Days'].mean()
                        st.metric("Avg Rental Duration", f"{avg_days:.1f} days")

                    # הצג טבלה
                    st.dataframe(df)

                    # הצג גרף עמודות
                    st.write("Revenue Distribution by Equipment Type:")
                    if len(df) > 1:
                        chart_data = df.set_index('Equipment Type')['Revenue']
                        st.bar_chart(chart_data)

                        # אופציונלי - הצג אחוזים
                        df['Revenue %'] = (df['Revenue'] / df['Revenue'].sum() * 100).round(2)
                        st.write("Revenue Percentage by Type:")
                        percentage_data = df[['Equipment Type', 'Revenue %']].set_index('Equipment Type')
                        st.dataframe(percentage_data)

                else:
                    st.info("No revenue data found")

            except Exception as e:
                st.error(f"Error generating report: {e}")
                st.write("Debug - Full error:", str(e))

elif page == "📝 Original Queries":
    st.title("Original Queries from Stage 2")
    st.info("These are the original queries created in the previous stage of the project")

    conn = init_connection()

    # יצירת טאבים לכל שאילתה
    tab1, tab2, tab3 = st.tabs(["🎿 Customer Rentals by Month", "👥 Lesson Participants", "💰 Cashier Revenue"])

    with tab1:
        st.subheader("Customer Rentals Count by Month")
        st.write(
            "*Description:* This query shows customers who rented equipment in a specific month, counting how many rentals each customer made.")

        col1, col2 = st.columns(2)
        with col1:
            year = st.number_input("Select Year", min_value=2020, max_value=2025, value=2024, key="rentals_year")
        with col2:
            month = st.number_input("Select Month", min_value=1, max_value=12, value=11, key="rentals_month")

        if st.button("Run Query", key="run_rentals"):
            try:
                query = """
                    SELECT
                        c.full_name AS customer_name,
                        c.phone,
                        COUNT(r.rid) AS rentals_count,
                        EXTRACT(YEAR FROM r.start_date) AS rental_year,
                        EXTRACT(MONTH FROM r.start_date) AS rental_month
                    FROM
                        customer c
                        JOIN rental r ON c.cid = r.cid
                    WHERE
                        EXTRACT(MONTH FROM r.start_date) = %s
                        AND EXTRACT(YEAR FROM r.start_date) = %s
                    GROUP BY
                        c.full_name, c.phone,
                        EXTRACT(YEAR FROM r.start_date),
                        EXTRACT(MONTH FROM r.start_date)
                    ORDER BY
                        rentals_count DESC
                """

                df = pd.read_sql(query, conn, params=[month, year])

                if not df.empty:
                    st.success(f"✅ Found {len(df)} customers with rentals in {month}/{year}")

                    # מטריקות
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Customers", len(df))
                    with col2:
                        st.metric("Total Rentals", df['rentals_count'].sum())
                    with col3:
                        st.metric("Max Rentals by Customer", df['rentals_count'].max())

                    # טבלת תוצאות
                    st.dataframe(df, use_container_width=True)

                    # גרף
                    if len(df) > 1:
                        st.bar_chart(df.set_index('customer_name')['rentals_count'].head(10))
                else:
                    st.warning(f"No rentals found for {month}/{year}")

            except Exception as e:
                st.error(f"Error: {e}")

    with tab2:
        st.subheader("Lesson Participants Count")
        st.write(
            "*Description:* This query counts the number of participants in each lesson for a specific month, helping identify popular lessons.")

        col1, col2 = st.columns(2)
        with col1:
            year = st.number_input("Select Year", min_value=2020, max_value=2025, value=2025, key="lesson_year")
        with col2:
            month = st.number_input("Select Month", min_value=1, max_value=12, value=1, key="lesson_month")

        if st.button("Run Query", key="run_lessons"):
            try:
                query = """
                    SELECT
                        l.lid,
                        EXTRACT(YEAR FROM l.ldate) AS lesson_year,
                        EXTRACT(MONTH FROM l.ldate) AS lesson_month,
                        COUNT(lp.cid) AS participants_count
                    FROM
                        lesson l
                        JOIN lesson_participants lp ON l.lid = lp.lid
                    WHERE
                        EXTRACT(YEAR FROM l.ldate) = %s
                        AND EXTRACT(MONTH FROM l.ldate) = %s
                    GROUP BY
                        l.lid, EXTRACT(YEAR FROM l.ldate), EXTRACT(MONTH FROM l.ldate)
                    ORDER BY
                        participants_count DESC
                """

                df = pd.read_sql(query, conn, params=[year, month])

                if not df.empty:
                    st.success(f"✅ Found {len(df)} lessons in {month}/{year}")

                    # מטריקות
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Lessons", len(df))
                    with col2:
                        st.metric("Total Participants", df['participants_count'].sum())
                    with col3:
                        st.metric("Avg Participants/Lesson", f"{df['participants_count'].mean():.1f}")

                    # טבלת תוצאות
                    st.dataframe(df, use_container_width=True)

                    # גרף התפלגות
                    if len(df) > 1:
                        st.write("Participants Distribution:")
                        fig_data = df['participants_count'].value_counts().sort_index()
                        st.bar_chart(fig_data)
                else:
                    st.warning(f"No lessons found for {month}/{year}")

            except Exception as e:
                st.error(f"Error: {e}")

    with tab3:
        st.subheader("Cashier Revenue Report")
        st.write(
            "*Description:* This query shows the total revenue generated by each cashier per month, filtering only cashiers with revenue above a threshold.")

        revenue_threshold = st.number_input(
            "Minimum Revenue Threshold",
            min_value=0,
            max_value=10000,
            value=1000,
            step=100,
            help="Only show cashiers with revenue above this amount"
        )

        if st.button("Run Query", key="run_cashier"):
            try:
                query = """
                    SELECT
                        e.fname || ' ' || e.lname AS cashier_name,
                        EXTRACT(YEAR FROM p.pdate) AS pay_year,
                        EXTRACT(MONTH FROM p.pdate) AS pay_month,
                        SUM(p.amount) AS total_revenue
                    FROM
                        cashier c
                        JOIN employee e ON c.eid = e.eid
                        JOIN payment p ON c.eid = p.eid
                    GROUP BY
                        e.fname, e.lname,
                        EXTRACT(YEAR FROM p.pdate),
                        EXTRACT(MONTH FROM p.pdate)
                    HAVING
                        SUM(p.amount) > %s
                    ORDER BY
                        total_revenue DESC
                """

                df = pd.read_sql(query, conn, params=[revenue_threshold])

                if not df.empty:
                    st.success(f"✅ Found {len(df)} cashier records with revenue > ₪{revenue_threshold}")

                    # מטריקות
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        unique_cashiers = df['cashier_name'].nunique()
                        st.metric("Unique Cashiers", unique_cashiers)
                    with col2:
                        st.metric("Total Revenue", f"₪{df['total_revenue'].sum():,.2f}")
                    with col3:
                        st.metric("Highest Monthly Revenue", f"₪{df['total_revenue'].max():,.2f}")

                    # טבלת תוצאות
                    df_display = df.copy()
                    df_display['total_revenue'] = df_display['total_revenue'].apply(lambda x: f"₪{x:,.2f}")
                    df_display['Month/Year'] = df_display.apply(
                        lambda row: f"{int(row['pay_month'])}/{int(row['pay_year'])}", axis=1)

                    st.dataframe(
                        df_display[['cashier_name', 'Month/Year', 'total_revenue']].rename(columns={
                            'cashier_name': 'Cashier Name',
                            'total_revenue': 'Total Revenue'
                        }),
                        use_container_width=True
                    )

                    # גרף עמודות לפי קופאי
                    st.write("Revenue by Cashier:")
                    cashier_totals = df.groupby('cashier_name')['total_revenue'].sum().sort_values(ascending=False)
                    st.bar_chart(cashier_totals.head(10))

                    # גרף מגמה לאורך זמן
                    if len(df) > 1:
                        st.write("Revenue Trend Over Time:")
                        df['date'] = pd.to_datetime(df[['pay_year', 'pay_month']].assign(day=1))
                        time_series = df.groupby('date')['total_revenue'].sum()
                        st.line_chart(time_series)

                else:
                    st.warning(f"No cashiers found with revenue above ₪{revenue_threshold}")

            except Exception as e:
                st.error(f"Error: {e}")

    # הוסף הסבר כללי
    with st.expander("📖 Query Explanations"):
        st.write("""
        ### Query 1: Customer Rentals by Month
        - *Purpose*: Track customer activity and identify frequent renters
        - *Use Case*: Marketing campaigns, customer loyalty programs
        - *Parameters*: Year and Month

        ### Query 2: Lesson Participants Count
        - *Purpose*: Measure lesson popularity and capacity utilization
        - *Use Case*: Instructor scheduling, lesson planning
        - *Parameters*: Year and Month

        ### Query 3: Cashier Revenue Report
        - *Purpose*: Performance tracking and commission calculations
        - *Use Case*: Employee evaluation, financial reporting
        - *Parameters*: Minimum revenue threshold
        """)

elif page == "🎿 Equipment":
    st.title("Equipment Management")

    # CRUD tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 View All", "➕ Create", "✏ Update", "🗑 Delete", "📊 Analytics"])

    conn = init_connection()
    cur = conn.cursor()

    with tab1:
        st.subheader("All Equipment")

        # פילטרים
        col1, col2, col3 = st.columns(3)
        with col1:
            equipment_types = pd.read_sql("SELECT DISTINCT type FROM equipment ORDER BY type", conn)
            filter_type = st.selectbox("Filter by Type", ["All"] + equipment_types['type'].tolist())
        with col2:
            min_price = st.number_input("Min Price", min_value=0, value=0)
        with col3:
            max_price = st.number_input("Max Price", min_value=0, value=1000)

        # שאילתה עם פילטרים
        if filter_type == "All":
            query = "SELECT * FROM equipment WHERE daily_price >= %s AND daily_price <= %s ORDER BY eid"
            params = [min_price, max_price]
        else:
            query = "SELECT * FROM equipment WHERE daily_price >= %s AND daily_price <= %s AND type = %s ORDER BY eid"
            params = [min_price, max_price, filter_type]

        df = pd.read_sql(query, conn, params=params)

        if not df.empty:
            # הצג סטטיסטיקות
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Items", len(df))
            with col2:
                st.metric("Unique Types", df['type'].nunique())
            with col3:
                st.metric("Avg Price", f"₪{df['daily_price'].mean():.2f}")
            with col4:
                # בדוק כמה פריטים מושכרים כרגע
                rented_query = """
                    SELECT COUNT(DISTINCT re.eid) 
                    FROM rental_equipment re
                    JOIN rental r ON re.rid = r.rid
                    WHERE r.end_date >= CURRENT_DATE
                """
                rented_count = pd.read_sql(rented_query, conn).iloc[0, 0]
                st.metric("Currently Rented", rented_count)

            # הצג טבלה
            st.dataframe(df, use_container_width=True)

            # הוסף אפשרות להוריד כ-CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name='equipment_list.csv',
                mime='text/csv'
            )
        else:
            st.info("No equipment found matching the criteria")

    with tab2:
        st.subheader("Add New Equipment")

        with st.form("create_equipment"):
            col1, col2 = st.columns(2)

            with col1:
                eid = st.number_input("Equipment ID", min_value=1, help="Unique identifier for the equipment")
                equipment_type = st.text_input("Equipment Type", placeholder="e.g., Skis, Snowboard, Boots")

            with col2:
                daily_price = st.number_input("Daily Price (₪)", min_value=0.0, step=10.0)

            submitted = st.form_submit_button("Create Equipment", type="primary")

            if submitted:
                if not equipment_type:
                    st.error("Please enter equipment type")
                else:
                    try:
                        # בדוק אם ID כבר קיים
                        existing = pd.read_sql("SELECT COUNT(*) FROM equipment WHERE eid = %s", conn, params=[eid])
                        if existing.iloc[0, 0] > 0:
                            st.error(f"Equipment ID {eid} already exists!")
                        else:
                            cur.execute(
                                "INSERT INTO equipment (eid, type, daily_price) VALUES (%s, %s, %s)",
                                (eid, equipment_type, daily_price)
                            )
                            conn.commit()
                            st.success(f"✅ Equipment {equipment_type} (ID: {eid}) created successfully!")
                            st.balloons()
                            time.sleep(1)
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                        conn.rollback()

    with tab3:
        st.subheader("Update Equipment")

        # בחר ציוד לעדכון
        equipment_list = pd.read_sql("SELECT eid, type, daily_price FROM equipment ORDER BY eid", conn)

        if not equipment_list.empty:
            equipment_to_update = st.selectbox(
                "Select Equipment to Update",
                equipment_list['eid'].tolist(),
                format_func=lambda
                    x: f"ID: {x} - {equipment_list[equipment_list['eid'] == x]['type'].iloc[0]} (₪{equipment_list[equipment_list['eid'] == x]['daily_price'].iloc[0]}/day)"
            )

            # טען נתונים נוכחיים
            current_data = equipment_list[equipment_list['eid'] == equipment_to_update].iloc[0]

            st.write("### Current Details:")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"*Type:* {current_data['type']}")
            with col2:
                st.write(f"*Daily Price:* ₪{current_data['daily_price']}")

            st.write("### Update to:")
            with st.form("update_equipment"):
                new_type = st.text_input("New Equipment Type", value=current_data['type'])
                new_price = st.number_input("New Daily Price (₪)", value=float(current_data['daily_price']),
                                            min_value=0.0, step=10.0)

                submitted = st.form_submit_button("Update Equipment")

                if submitted:
                    try:
                        cur.execute(
                            "UPDATE equipment SET type = %s, daily_price = %s WHERE eid = %s",
                            (new_type, new_price, equipment_to_update)
                        )
                        conn.commit()
                        st.success("✅ Equipment updated successfully!")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                        conn.rollback()
        else:
            st.info("No equipment found in the database")

    with tab4:
        st.subheader("Delete Equipment")

        equipment_list = pd.read_sql("SELECT eid, type, daily_price FROM equipment ORDER BY eid", conn)

        if not equipment_list.empty:
            equipment_to_delete = st.selectbox(
                "Select Equipment to Delete",
                equipment_list['eid'].tolist(),
                format_func=lambda x: f"ID: {x} - {equipment_list[equipment_list['eid'] == x]['type'].iloc[0]}"
            )

            # הצג פרטי הציוד
            selected_equipment = equipment_list[equipment_list['eid'] == equipment_to_delete].iloc[0]

            col1, col2 = st.columns(2)
            with col1:
                st.write(f"*Type:* {selected_equipment['type']}")
            with col2:
                st.write(f"*Daily Price:* ₪{selected_equipment['daily_price']}")

            # בדוק אם הציוד מושכר כרגע
            active_rentals_query = """
                SELECT COUNT(*) 
                FROM rental_equipment re
                JOIN rental r ON re.rid = r.rid
                WHERE re.eid = %s AND r.end_date >= CURRENT_DATE
            """
            active_rentals_result = pd.read_sql(active_rentals_query, conn, params=[equipment_to_delete])
            active_rentals = active_rentals_result.iloc[0, 0]

            if active_rentals > 0:
                st.error(f"❌ Cannot delete: This equipment is currently rented in {active_rentals} active rental(s)")
            else:
                # בדוק היסטוריה
                history_query = "SELECT COUNT(*) FROM rental_equipment WHERE eid = %s"
                history_result = pd.read_sql(history_query, conn, params=[equipment_to_delete])
                has_history = history_result.iloc[0, 0] > 0

                if has_history:
                    st.warning("⚠ This equipment has rental history. Deleting will affect historical records.")

                st.warning("⚠ This action cannot be undone!")

                confirm_delete = st.checkbox("I understand and want to delete this equipment")

                if confirm_delete:
                    if st.button("Delete Equipment", type="secondary"):
                        try:
                            cur.execute("DELETE FROM equipment WHERE eid = %s", (equipment_to_delete,))
                            conn.commit()
                            st.success("✅ Equipment deleted successfully!")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                            if "violates foreign key constraint" in str(e):
                                st.error(
                                    "Cannot delete equipment that has rental history. Consider marking as inactive instead.")
                            conn.rollback()
        else:
            st.info("No equipment found in the database")

    with tab5:
        st.subheader("Equipment Analytics")

        # ניתוח לפי סוג ציוד
        st.write("### Equipment Distribution by Type")
        type_dist_query = """
            SELECT type, COUNT(*) as count, AVG(daily_price) as avg_price
            FROM equipment
            GROUP BY type
            ORDER BY count DESC
        """
        type_dist = pd.read_sql(type_dist_query, conn)

        if not type_dist.empty:
            col1, col2 = st.columns(2)

            with col1:
                st.write("*Equipment Count by Type*")
                fig_data = type_dist.set_index('type')['count']
                st.bar_chart(fig_data)

            with col2:
                st.write("*Average Price by Type*")
                price_data = type_dist.set_index('type')['avg_price']
                st.bar_chart(price_data)

            # הצג טבלת סיכום
            st.write("*Summary Table*")
            type_dist['avg_price'] = type_dist['avg_price'].round(2)
            st.dataframe(type_dist, use_container_width=True)

        # ניתוח ניצולת
        st.write("### Equipment Utilization Analysis")

        utilization_query = """
            SELECT 
                e.eid,
                e.type,
                e.daily_price,
                COUNT(DISTINCT re.rid) as times_rented,
                COALESCE(SUM(r.end_date - r.start_date + 1), 0) as total_days_rented,
                COALESCE(SUM((r.end_date - r.start_date + 1) * e.daily_price), 0) as total_revenue
            FROM equipment e
            LEFT JOIN rental_equipment re ON e.eid = re.eid
            LEFT JOIN rental r ON re.rid = r.rid
            GROUP BY e.eid, e.type, e.daily_price
            ORDER BY total_revenue DESC
        """

        utilization_df = pd.read_sql(utilization_query, conn)

        if not utilization_df.empty:
            # מטריקות ניצולת
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                never_rented = len(utilization_df[utilization_df['times_rented'] == 0])
                st.metric("Never Rented", never_rented)
            with col2:
                avg_rentals = utilization_df[utilization_df['times_rented'] > 0]['times_rented'].mean() if len(
                    utilization_df[utilization_df['times_rented'] > 0]) > 0 else 0
                st.metric("Avg Rentals/Item", f"{avg_rentals:.1f}")
            with col3:
                total_revenue = utilization_df['total_revenue'].sum()
                st.metric("Total Revenue", f"₪{total_revenue:,.2f}")
            with col4:
                most_rented = utilization_df.iloc[0]['type'] if len(utilization_df) > 0 else "N/A"
                st.metric("Most Rented Type", most_rented)

            # טבלת ניצולת מפורטת
            st.write("### Top 10 Equipment by Revenue")
            display_df = utilization_df.head(10)[
                ['eid', 'type', 'daily_price', 'times_rented', 'total_days_rented', 'total_revenue']].copy()
            display_df.columns = ['ID', 'Type', 'Daily Price (₪)', 'Times Rented', 'Total Days', 'Revenue (₪)']
            display_df['Revenue (₪)'] = display_df['Revenue (₪)'].round(2)
            st.dataframe(display_df, use_container_width=True)

            # המלצות
            st.write("### Insights")
            if never_rented > 0:
                st.info(f"💡 {never_rented} items have never been rented. Consider price adjustments or promotions.")

            if len(utilization_df) > 0:
                top_revenue_type = utilization_df.groupby('type')['total_revenue'].sum().idxmax()
                st.success(f"🌟 '{top_revenue_type}' generates the most revenue")

elif page == "⚙ Functions":
    st.title("System Functions")

    conn = init_connection()
    cur = conn.cursor()

    # חלק את המסך לשתי עמודות
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Customer Spending Analysis")
        customer_id = st.number_input("Enter Customer ID", min_value=1, value=1)

        if st.button("Calculate Customer Spending"):
            try:
                # קריאה לפונקציה
                query = "SELECT * FROM calculate_customer_total_spending(%s)"
                df = pd.read_sql(query, conn, params=[customer_id])

                if not df.empty:
                    # הצג את התוצאות
                    st.success("✅ Analysis Complete!")

                    # הצג את הנתונים
                    customer_data = df.iloc[0]

                    st.write(f"*Customer Name:* {customer_data['customer_name']}")
                    st.write(f"*Rental Costs:* ₪{customer_data['rental_costs']:.2f}")
                    st.write(f"*Lesson Costs:* ₪{customer_data['lesson_costs']:.2f}")
                    st.write(f"*Total Spent:* ₪{customer_data['total_spent']:.2f}")
                    st.write(f"*Last Activity:* {customer_data['last_activity']}")

                    if customer_data['is_vip']:
                        st.balloons()
                        st.success("🌟 This is a VIP customer!")
                    else:
                        st.info("Regular customer")

                    # הצג את הנתונים בטבלה
                    st.dataframe(df)
                else:
                    st.warning("No data found for this customer")

            except Exception as e:
                st.error(f"Error: {e}")

    with col2:
        st.subheader("🔍 Equipment Availability Check")
        check_date = st.date_input("Select Date", value=pd.Timestamp.now().date())
        equipment_type = st.text_input("Equipment Type (optional)", placeholder="Leave empty for all types")

        if st.button("Check Availability"):
            try:
                # קריאה לפונקציה
                if equipment_type:
                    query = "SELECT * FROM find_available_equipment(%s, %s)"
                    params = [check_date, equipment_type]
                else:
                    query = "SELECT * FROM find_available_equipment(%s)"
                    params = [check_date]

                df = pd.read_sql(query, conn, params=params)

                if not df.empty:
                    st.success(f"✅ Found {len(df)} available items!")

                    # הצג סטטיסטיקות
                    col1_stats, col2_stats = st.columns(2)
                    with col1_stats:
                        st.metric("Available Items", len(df))
                    with col2_stats:
                        avg_price = df['daily_price'].mean()
                        st.metric("Average Daily Price", f"₪{avg_price:.2f}")

                    # הצג את הציוד הזמין
                    st.write("*Available Equipment:*")
                    st.dataframe(
                        df[['eid', 'type', 'daily_price']].rename(columns={
                            'eid': 'Equipment ID',
                            'type': 'Type',
                            'daily_price': 'Daily Price (₪)'
                        })
                    )

                    # הצג גרף מחירים
                    if len(df) > 1:
                        st.bar_chart(df.set_index('type')['daily_price'])
                else:
                    st.warning("No equipment available for this date")

            except Exception as e:
                st.error(f"Error: {e}")

    # הוסף סעיף לפרוצדורות
    st.divider()
    st.subheader("🔧 System Procedures")

    col3, col4 = st.columns(2)

    with col3:
        st.write("*Archive Old Rentals*")
        days_old = st.number_input("Days to keep", min_value=30, value=365)

        if st.button("Run Archive"):
            try:
                # יצירת משתנים לפלט
                cur.execute("""
                    DO $$
                    DECLARE
                        v_count INT;
                        v_revenue NUMERIC;
                    BEGIN
                        CALL archive_old_rentals(v_count, v_revenue, %s);
                        RAISE NOTICE 'Archived %% rentals worth %%', v_count, v_revenue;
                    END $$;
                """, [days_old])
                conn.commit()

                st.success("✅ Archive process completed!")
                st.info("Check the archived_rentals table for moved records")

            except Exception as e:
                st.error(f"Error: {e}")
                conn.rollback()

    with col4:
        st.write("*Smart Price Update*")
        analysis_days = st.number_input("Analysis period (days)", min_value=7, value=30)
        increase_threshold = st.slider("Increase threshold %", 50, 90, 70)
        decrease_threshold = st.slider("Decrease threshold %", 10, 50, 30)

        if st.button("Update Prices"):
            try:
                cur.execute("CALL smart_price_update(%s, %s, %s)",
                            [analysis_days, increase_threshold, decrease_threshold])
                conn.commit()

                st.success("✅ Prices updated successfully!")
                st.info("Check the equipment table to see the new prices")

                # הצג את השינויים
                st.write("*Current Equipment Prices:*")
                df_prices = pd.read_sql(
                    "SELECT eid, type, daily_price FROM equipment ORDER BY daily_price DESC LIMIT 10",
                    conn
                )
                st.dataframe(df_prices)

            except Exception as e:
                st.error(f"Error: {e}")
                conn.rollback()

# Run the app
if __name__ == "__main__":
    st.write("App is running!")
