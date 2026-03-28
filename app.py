# =============================
# Cubelelo Support Insights Tool (ULTIMATE FINAL)
# =============================

import pandas as pd
import streamlit as st

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("Dataset - Sheet1.csv")

df = load_data()

# Clean data
df.columns = df.columns.str.strip()
df = df.fillna("")

st.title("📊 Cubelelo Support Insights Dashboard")

# -----------------------------
# Top Issue Categories
# -----------------------------
st.header("Top Issue Categories")
top_issues = df['Category'].value_counts()
st.bar_chart(top_issues)

# -----------------------------
# Unresolved Tickets
# -----------------------------
st.header("Unresolved Tickets")

unresolved = df[df['Status'] != 'Resolved'].copy()

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
# Risk Scoring
# -----------------------------
st.header("Top Risk Tickets")

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
# Aging Analysis
# -----------------------------
st.header("Aging Analysis")

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
st.header("Alerts")

alerts = []

if top_issues.max() > 5:
    alerts.append("High complaints detected in a category")

if len(unresolved) > 10:
    alerts.append("Too many unresolved tickets")

for alert in alerts:
    st.warning("⚠️ " + alert)

# -----------------------------
# Product Insights
# -----------------------------
st.header("Product Complaint Ranking")

product_issues = df['Product'].value_counts().head(5)
st.bar_chart(product_issues)

# -----------------------------
# SMART Manager Summary
# -----------------------------
st.header("Manager Summary")

total_tickets = len(df)
unresolved_count = len(unresolved)
high_priority_unresolved = len(unresolved[unresolved['Priority'] == 'High'])

top_issue = top_issues.idxmax()
top_issue_count = top_issues.max()
top_issue_percent = round((top_issue_count / total_tickets) * 100, 1)

unresolved_percent = round((unresolved_count / total_tickets) * 100, 1)

delivery_issues = df[df['Category'].str.lower().str.contains("delivery")]
refund_issues = df[df['Category'].str.lower().str.contains("refund|replacement")]

# -----------------------------
# COLOR CODED INSIGHTS
# -----------------------------

# Top issue
if top_issue_percent > 30:
    st.error(f"🔴 {top_issue} is the biggest issue ({top_issue_percent}% of tickets)")
else:
    st.info(f"🟢 {top_issue} is under control ({top_issue_percent}%)")

# Unresolved
if unresolved_percent > 40:
    st.error(f"🔴 {unresolved_count}/{total_tickets} tickets unresolved ({unresolved_percent}%)")
else:
    st.warning(f"🟡 {unresolved_count}/{total_tickets} tickets unresolved")

# High priority
if high_priority_unresolved > 5:
    st.error(f"🔴 {high_priority_unresolved} high-priority tickets pending")
else:
    st.info(f"🟢 High-priority tickets under control ({high_priority_unresolved})")

# Delivery
st.warning(f"🚚 {len(delivery_issues)} delivery-related issues found")

# Refund
st.warning(f"💸 {len(refund_issues)} refund/replacement cases found")

# -----------------------------
# AUTO RECOMMENDATIONS
# -----------------------------
st.header("Recommended Actions")

if top_issue_percent > 30:
    st.write("👉 Improve product quality checks and supplier control")

if unresolved_percent > 40:
    st.write("👉 Increase support team response speed")

if high_priority_unresolved > 5:
    st.write("👉 Escalate high-priority tickets immediately")

if len(delivery_issues) > 3:
    st.write("👉 Review logistics and delivery partners")

if len(refund_issues) > 3:
    st.write("👉 Optimize refund and replacement workflow")

# -----------------------------
# Run:
# streamlit run app.py
# -----------------------------
