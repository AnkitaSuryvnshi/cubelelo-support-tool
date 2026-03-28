# =============================
# Cubelelo Support Insights Tool (FINAL FIXED + SMART LOGIC)
# =============================

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Cubelelo Dashboard", layout="wide")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("Dataset - Sheet1.csv")

df = load_data()

df.columns = df.columns.str.strip()
df = df.fillna("")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Dashboard",
    "Unresolved",
    "Risk",
    "Manager Insights"
])

# -----------------------------
# BASIC CALCULATIONS
# -----------------------------
unresolved = df[df['Status'] != 'Resolved'].copy()
total_tickets = len(df)
unresolved_count = len(unresolved)
high_priority_unresolved = len(unresolved[unresolved['Priority'] == 'High'])

top_issues = df['Category'].value_counts()

# -----------------------------
# DASHBOARD
# -----------------------------
if page == "Dashboard":

    st.title("Cubelelo Support Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tickets", total_tickets)
    col2.metric("Unresolved", unresolved_count)
    col3.metric("High Priority", high_priority_unresolved)

    st.bar_chart(top_issues)
    st.bar_chart(df['Product'].value_counts().head(5))

# -----------------------------
# UNRESOLVED
# -----------------------------
elif page == "Unresolved":

    st.title("Unresolved Tickets")

    def get_reason(issue):
        if issue == "":
            return "No data"
        issue = str(issue).lower()
        if "delay" in issue:
            return "Logistics delay"
        elif "refund" in issue:
            return "Refund process slow"
        elif "quality" in issue or "defect" in issue:
            return "Quality issue"
        else:
            return "Needs investigation"

    unresolved['Reason'] = unresolved['Category'].apply(get_reason)

    st.dataframe(unresolved[['Ticket ID', 'Category', 'Priority', 'Reason']])

# -----------------------------
# RISK
# -----------------------------
elif page == "Risk":

    st.title("Risk Analysis")

    def risk_score(row):
        score = 0
        if row['Priority'] == 'High':
            score += 3
        if "refund" in str(row['Category']).lower():
            score += 2
        if row['Status'] != 'Resolved':
            score += 2
        return score

    unresolved['Risk Score'] = unresolved.apply(risk_score, axis=1)

    st.dataframe(unresolved.sort_values(by='Risk Score', ascending=False).head(5))

# -----------------------------
# MANAGER INSIGHTS (SMART FIX)
# -----------------------------
elif page == "Manager Insights":

    st.title("Manager Insights")

    # ---- TOP ISSUE LOGIC (FIXED)
    top_two = top_issues.head(2)

    top_issue = top_two.index[0]
    top_issue_count = top_two.iloc[0]
    second_issue_count = top_two.iloc[1] if len(top_two) > 1 else 0

    top_issue_percent = round((top_issue_count / total_tickets) * 100, 1)

    if top_issue_count >= second_issue_count * 1.5:
        st.error(f"{top_issue} is dominating issue ({top_issue_percent}%)")
    elif top_issue_count > second_issue_count:
        st.warning(f"{top_issue} is leading issue ({top_issue_percent}%)")
    else:
        st.success("Issues are evenly distributed")

    # ---- UNRESOLVED LOGIC (IMPROVED)
    unresolved_percent = round((unresolved_count / total_tickets) * 100, 1)

    if unresolved_percent > 50:
        st.error(f"{unresolved_count}/{total_tickets} unresolved ({unresolved_percent}%)")
    elif unresolved_percent > 25:
        st.warning(f"{unresolved_count}/{total_tickets} unresolved ({unresolved_percent}%)")
    else:
        st.success("Unresolved tickets under control")

    # ---- HIGH PRIORITY
    if high_priority_unresolved > 5:
        st.error(f"{high_priority_unresolved} high-priority pending")
    else:
        st.success("High-priority under control")

    # ---- PATTERNS
    delivery_issues = df[df['Category'].str.lower().str.contains("delivery")]
    refund_issues = df[df['Category'].str.lower().str.contains("refund|replacement")]

    st.info(f"Delivery Issues: {len(delivery_issues)}")
    st.info(f"Refund Issues: {len(refund_issues)}")

    # ---- SUMMARY (DATA-DRIVEN)
    st.subheader("Summary")

    summary = f"""
    - {top_issue} is the most frequent issue.
    - {unresolved_count} out of {total_tickets} tickets remain unresolved.
    - {high_priority_unresolved} high-priority tickets require immediate attention.
    - {len(delivery_issues)} delivery-related complaints observed.
    - {len(refund_issues)} refund/replacement delays identified.
    """

    st.success(summary)
