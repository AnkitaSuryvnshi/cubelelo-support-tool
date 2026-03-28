# =============================
# Cubelelo Support Insights Tool (FINAL - NO PERCENT)
# =============================

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Cubelelo Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("Dataset - Sheet1.csv")

df = load_data()

df.columns = df.columns.str.strip()
df = df.fillna("")

unresolved = df[df['Status'] != 'Resolved'].copy()

total_tickets = len(df)
unresolved_count = len(unresolved)
high_priority_unresolved = len(unresolved[unresolved['Priority'] == 'High'])

st.title("📊 Cubelelo Support Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Total Tickets", total_tickets)
col2.metric("Unresolved Tickets", unresolved_count)
col3.metric("High Priority", high_priority_unresolved)

st.divider()

# -----------------------------
# Top Issues
# -----------------------------
st.header("📊 Top Issue Categories")
top_issues = df['Category'].value_counts()
st.bar_chart(top_issues)

# -----------------------------
# Unresolved Tickets
# -----------------------------
st.header("📋 Unresolved Tickets")

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
# Risk Tickets
# -----------------------------
st.header("🚨 Top Risk Tickets")

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
top_risk = unresolved.sort_values(by='Risk Score', ascending=False).head(5)

st.dataframe(top_risk)

# -----------------------------
# Aging
# -----------------------------
st.header("⏳ Aging Analysis")

df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Days Open'] = (pd.Timestamp.today() - df['Date']).dt.days

aging = {
    "<1 day": len(df[df['Days Open'] <= 1]),
    "1-3 days": len(df[(df['Days Open'] > 1) & (df['Days Open'] <= 3)]),
    ">3 days": len(df[df['Days Open'] > 3])
}

st.write(aging)

# -----------------------------
# Alerts
# -----------------------------
st.header("⚠️ Alerts")

if top_issues.max() > 5:
    st.warning("⚠️ High complaints in a category")

if unresolved_count > 10:
    st.warning("⚠️ Too many unresolved tickets")

# -----------------------------
# Product Insights
# -----------------------------
st.header("📦 Product Complaint Ranking")

product_issues = df['Product'].value_counts().head(5)
st.bar_chart(product_issues)

# -----------------------------
# MANAGER INSIGHTS (NO %)
# -----------------------------
st.header("🧠 Manager Insights")

top_issue = top_issues.idxmax()
top_issue_count = top_issues.max()

delivery_issues = df[df['Category'].str.lower().str.contains("delivery")]
refund_issues = df[df['Category'].str.lower().str.contains("refund|replacement")]

# Top issue (count based)
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

# -----------------------------
# SUMMARY (NO %)
# -----------------------------
st.subheader("Summary")

summary = f"""
- {top_issue} is the most common issue with {top_issue_count} tickets.
- {unresolved_count} tickets remain unresolved.
- {high_priority_unresolved} high-priority tickets need attention.
- {len(delivery_issues)} delivery-related issues observed.
- {len(refund_issues)} refund/replacement cases identified.
"""

st.success(summary)
