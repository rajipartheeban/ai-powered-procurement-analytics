# AI-Powered Procurement Analytics

An end-to-end procurement analytics project that combines data analytics and AI to analyze vendor spending, savings, delivery performance, quality, and procurement risk.

## Project Overview

This project transforms procurement data into actionable business insights using Python, SQL, Power BI, and an AI-powered procurement assistant.

The project workflow is:

**Procurement Data → Python → SQL → Power BI → AI Assistant**

## Technologies Used

- Python
- Pandas
- SQL
- MySQL
- Power BI
- DAX
- Streamlit
- Ollama
- Llama 3.1 8B

## Key Analysis

- Vendor spending analysis
- Procurement savings analysis
- Delivery performance
- Vendor quality analysis
- Defect rate analysis
- Procurement risk analysis
- Category-level spending
- Monthly procurement trends
- Cost optimization opportunities

## AI Procurement Assistant

The project includes a Streamlit-based AI assistant that allows users to ask natural-language questions about the procurement data.

The assistant uses:

- Python and Pandas for data-based analysis
- Ollama for local AI model execution
- Llama 3.1 8B for natural-language responses

## Project Structure

```text
ai-powered-procurement-analytics/
│
├── README.md
│
├── data/
│   └── Procurement_KPI_Analysis_Dataset.csv
│
├── python/
│   ├── data_cleaning.py
│   └── create_kpis.py
│
├── sql/
│   └── procurement_analysis.sql
│
├── power-bi/
│   └── screenshots/
│       ├── dashboard-page-1.png
│       ├── dashboard-page-2.png
│       └── dashboard-page-3.png
│
└── ai/
    ├── procurement_ai_assistant.py
    └── screenshots/
        └── ai-assistant-demo.png
