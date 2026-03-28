# Cubelelo Support Tool

## Project Overview

Cubelelo Support Tool is a data analysis and visualization dashboard designed to help support managers quickly understand customer issues. It transforms raw support ticket data into meaningful insights that can be used for faster decision-making.

## Problem Statement

Cubelelo handles multiple customer support tickets every week related to delivery delays, defective products, wrong shipments, and refund issues. Managers often do not have a quick way to:

* Identify the most common problems
* Track unresolved tickets
* Detect operational bottlenecks

This tool solves that problem by providing a clear and structured summary of support data.

## Features

* Top issue category identification
* Unresolved ticket tracking with reasons
* Risk scoring for critical tickets
* Aging analysis of tickets
* Product-wise complaint analysis
* Smart alerts for high-risk situations
* Data-driven manager insights
* Actionable recommendations
* Interactive dashboard with sidebar navigation

## Technology Stack

* Python
* Pandas
* Streamlit

## File Structure

* app.py → Main application file
* Dataset - Sheet1.csv → Input dataset
* requirements.txt → Required libraries

## How to Run

1. Install dependencies:
   pip install streamlit pandas openai

2. Place the dataset file in the same folder as app.py

3. Run the application:
   streamlit run app.py

4. Open in browser:
   http://localhost:8501

## Output

The tool provides:

* Dashboard with key metrics
* Charts for issue categories
* Tables for unresolved and high-risk tickets
* Manager insights based on real data
* Recommended actions for improvement

## Key Insights

* Most frequent issue categories
* Percentage of unresolved tickets
* High-priority pending tickets
* Delivery and refund-related patterns

## Purpose

The purpose of this tool is to help support managers quickly understand operational issues and take action without manually analyzing data.

## Future Improvements

* Real-time ticket integration
* Advanced filters (date, priority, product)
* Downloadable reports
* AI-based predictive analytics

## Author

Developed as part of an assignment to demonstrate problem-solving using data analysis and dashboard tools.
