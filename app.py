# =============================
# Cubelelo Support Insights Tool (FINAL - FIXED CATEGORY)
# =============================

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Cubelelo Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("Dataset - Sheet1.csv")

df = load_data()

# Clean columns + nulls
df.columns = df.columns.str.strip()
df = df.fillna("")

# -----------------------------
# 🔥 CATEGORY NORMALIZATION FIX
# -----------------------------
df['Category'] = df['Category'].str.lower().str.strip()

df['Category'] = df['Category'].replace({
    'product quality issue': 'product quality',
    'quality issue': 'product quality',
    'defective product': 'product quality',
    'damaged product': 'product quality',
    'product defect': 'product quality'
})

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", [
    "Dashboard",
    "Unresolved Tickets",
    "Risk Analysis",
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

    st.title("📊 Cubelelo Support Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tickets", total_tickets)
    col2.metric("Unresolved Tickets", unresolved_count)
    col3.metric("High Priority", high_priority_unresolved)

    st.divider()

    st.header("📊 Top Issue Categories")
    st.bar_chart(top_issues)

    st.header("📦 Product Complaint Ranking")
    st.bar_chart(df['Product'].value_counts().head(5))


# -----------------------------
# UNRESOLVED
# -----------------------------
elif page == "Unresolved Tickets":

    st.title("📋 Unresolved Tickets")

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
elif page == "Risk Analysis":

    st.title("🚨 Risk Analysis")

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

    st.subheader("Top Risk Tickets")
    st.dataframe(unresolved.sort_values(by='Risk Score', ascending=False).head(5))

    st.subheader("⏳ Aging Analysis")

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Days Open'] = (pd.Timestamp.today() - df['Date']).dt.days

    aging = {
        "<1 day": len(df[df['Days Open'] <= 1]),
        "1-3 days": len(df[(df['Days Open'] > 1) & (df['Days Open'] <= 3)]),
        ">3 days": len(df[df['Days Open'] > 3])
    }

    st.write(aging)


# -----------------------------
# MANAGER INSIGHTS
# -----------------------------
elif page == "Manager Insights":

    st.title("🧠 Manager Insights")

    top_issue = top_issues.idxmax()
    top_issue_count = top_issues.max()

    delivery_issues = df[df['Category'].str.contains("delivery")]
    refund_issues = df[df['Category'].str.contains("refund|replacement")]

    # Top issue
    if top_issue_count > 5:
        st.error(f"🔴 {top_issue} is the major issue ({top_issue_count} tickets)")
    else:
        st.warning(f"🟡 {top_issue} is the leading issue ({top_issue_count} tickets)")

    # Unresolved
    if unresolved_count > 10:
        st.error(f"🔴 {unresolved_count} tickets are unresolved")
    elif unresolved_count > 5:
        st.warning(f"🟡 {unresolved_count} tickets are unresolved")
    else:
        st.success("🟢 Unresolved tickets under control")

    # High priority
    if high_priority_unresolved > 5:
        st.error(f"🔴 {high_priority_unresolved} high-priority tickets pending")
    else:
        st.success(f"🟢 High-priority under control ({high_priority_unresolved})")

    # Patterns
    st.info(f"🚚 Delivery Issues: {len(delivery_issues)}")
    st.info(f"💸 Refund Issues: {len(refund_issues)}")

    # Summary
    st.subheader("Summary")

    summary = f"""
    - {top_issue} is the most common issue with {top_issue_count} tickets.
    - {unresolved_count} tickets remain unresolved.
    - {high_priority_unresolved} high-priority tickets need attention.
    - {len(delivery_issues)} delivery-related issues observed.
    - {len(refund_issues)} refund/replacement cases identified.
    """

    st.success(summary)
