# =============================
# Cubelelo Support Insights Tool (DARK UI FINAL)
# =============================

import pandas as pd
import streamlit as st

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Cubelelo Dashboard", layout="wide")

# -----------------------------
# DARK THEME + COMPACT UI
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: white;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

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
# SIDEBAR NAVIGATION
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
# DASHBOARD PAGE
# -----------------------------
if page == "Dashboard":

    st.title("📊 Cubelelo Support Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tickets", total_tickets)
    col2.metric("Unresolved", unresolved_count)
    col3.metric("High Priority", high_priority_unresolved)

    st.divider()

    st.subheader("📊 Top Issue Categories")
    st.bar_chart(top_issues)

    st.subheader("📦 Product Complaints")
    st.bar_chart(df['Product'].value_counts().head(5))


# -----------------------------
# UNRESOLVED PAGE
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
# RISK ANALYSIS PAGE
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
# MANAGER INSIGHTS PAGE
# -----------------------------
elif page == "Manager Insights":

    st.title("🧠 Manager Insights")

    top_issue = top_issues.idxmax()
    top_issue_percent = round((top_issues.max() / total_tickets) * 100, 1)
    unresolved_percent = round((unresolved_count / total_tickets) * 100, 1)

    delivery_issues = df[df['Category'].str.lower().str.contains("delivery")]
    refund_issues = df[df['Category'].str.lower().str.contains("refund|replacement")]

    # Compact colored insights
    if top_issue_percent > 30:
        st.error(f"🔴 {top_issue} highest issue ({top_issue_percent}%)")
    else:
        st.success(f"🟢 {top_issue} under control ({top_issue_percent}%)")

    if unresolved_percent > 40:
        st.error(f"🔴 {unresolved_count}/{total_tickets} unresolved ({unresolved_percent}%)")
    else:
        st.warning(f"🟡 {unresolved_count}/{total_tickets} unresolved")

    if high_priority_unresolved > 5:
        st.error(f"🔴 {high_priority_unresolved} high-priority pending")
    else:
        st.success(f"🟢 High-priority under control ({high_priority_unresolved})")

    st.info(f"🚚 Delivery Issues: {len(delivery_issues)}")
    st.info(f"💸 Refund Issues: {len(refund_issues)}")

    st.divider()

    st.subheader("✅ Recommended Actions")

    if top_issue_percent > 30:
        st.write("👉 Improve product quality checks")

    if unresolved_percent > 40:
        st.write("👉 Increase support response speed")

    if high_priority_unresolved > 5:
        st.write("👉 Escalate high-priority tickets")

    if len(delivery_issues) > 3:
        st.write("👉 Fix logistics/delivery partners")

    if len(refund_issues) > 3:
        st.write("👉 Improve refund process")
