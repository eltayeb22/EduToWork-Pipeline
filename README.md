# EduToWork-Pipeline
# EduToWork: Data Jobs Analytics Platform

An automated data pipeline and dashboard that aggregates, processes, and visualizes global remote job listings in the data field. It tracks technical skill demands to help professionals align their expertise with current market trends.

## How It Works

* **The Pipeline (`pipeline.py`)**: Fetches live postings across 12 data roles via API, extracts technical skills from descriptions, and stores the structured data in a local SQLite database.
* **The Dashboard (`app.py`)**: Reads the database to display interactive skill charts, high-level market metrics, and a searchable job board with direct application links.

## Supported Roles

The platform covers a wide range of data specializations:
* Data Engineering & Data Architecture
* Data Analytics & Business Intelligence
* Data Science, AI, and Machine Learning
* Data Product Management & Data Warehousing

## Tech Stack

* **Core**: Python 3
* **Data Processing**: Pandas, Requests
* **Storage**: SQLite3
* **Frontend & Charts**: Streamlit, Plotly Express

## Setup & Execution

### 1. Install Dependencies

```bash
pip install requests pandas streamlit plotly

# Run the Platform
python pipeline.py

python -m streamlit run app.py
