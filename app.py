# Cubelelo Support Insights Tool (FINAL)

import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data():
    return pd.read_csv("Dataset - Sheet1.csv")

df = load_data()

st.title("📊 Cubelelo Support Insights Dashboard")

# Top Issue Categories
st.header("Top Issue Categories")
top_issues = df['Issue Category'].value_counts()
st.bar_chart(top_issues)

# Unresolved Tickets
st.header("Unresolved Tickets")
unresolved = df[df['Status'] != 'Resolved'].copy()

def get_reason(issue):
    issue = issue.lower()
    if "delay" in issue:
        return "Logistics delay"
    elif "refund" in issue:
        return "Refund process slow"
    elif "quality" in issue or "defect" in issue:
        return "Quality issue"
    else:
        return "Needs investigation"

unresolved['Reason'] = unresolved['Issue Category'].apply(get_reason)
st.dataframe(unresolved[['Ticket ID', 'Issue Category', 'Priority', 'Reason']])

# Risk Scoring
st.header("Top Risk Tickets")

def risk_score(row):
    score = 0
    if row['Priority'] == 'High':
        score += 3
    if "refund" in row['Issue Category'].lower():
        score += 2
    if row['Status'] != 'Resolved':
        score += 2
    return score

unresolved['Risk Score'] = unresolved.apply(risk_score, axis=1)
top_risk = unresolved.sort_values(by='Risk Score', ascending=False).head(5)
st.dataframe(top_risk)

# Aging Analysis
st.header("Aging Analysis")
df['Created At'] = pd.to_datetime(df['Created At'])
df['Days Open'] = (pd.Timestamp.today() - df['Created At']).dt.days

aging = {
    "<1 day": len(df[df['Days Open'] <= 1]),
    "1-3 days": len(df[(df['Days Open'] > 1) & (df['Days Open'] <= 3)]),
    ">3 days": len(df[df['Days Open'] > 3])
}
st.write(aging)

# Alerts
st.header("Alerts")
alerts = []
if top_issues.max() > 5:
    alerts.append("⚠️ High complaints in a category detected")
if len(unresolved) > 10:
    alerts.append("⚠️ Too many unresolved tickets")

for alert in alerts:
    st.warning(alert)

# Product Insights
st.header("Product Complaint Ranking")
product_issues = df['Product Name'].value_counts().head(5)
st.bar_chart(product_issues)

# AI Summary (fallback included)
st.header("Manager Summary")

try:
    from openai import OpenAI
    client = OpenAI()

    summary_input = (
        "Top Issues: " + str(top_issues.to_dict()) + "\n" +
        "Unresolved Tickets: " + str(len(unresolved)) + "\n" +
        "High Priority Unresolved: " + str(len(unresolved[unresolved['Priority'] == 'High']))
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Give a short summary for manager"},
            {"role": "user", "content": summary_input}
        ]
    )

    st.success(response.choices[0].message.content)

except:
    st.info("AI summary not available. Showing fallback.")
