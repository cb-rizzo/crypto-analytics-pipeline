# 🚀 Cloud-Native Real-Time Crypto Pipeline & Analytics Product

An end-to-end data engineering pipeline and analytical product designed to monitor cryptocurrency prices in real-time, built with modern cloud tools, automation, and interactive visualization.

---

## 📸 Dashboard Preview
> *Real-time Streamlit analytical dashboard displaying live Bitcoin price tracking and historical metrics.*

![Crypto Analytics Dashboard](assets/screenshot.png)

---

## 🏗️ Architecture & Problem Solved
Moving away from simple static scripts, this project implements a production-ready architecture focused on **resilience, cloud automation, and scalability**:
1. **Extraction (`crypto_pipeline.py`)**: Connects to Binance's public API to fetch live cryptocurrency prices with robust error handling (`try-except`) and structured logging.
2. **Storage (PostgreSQL on Neon.tech)**: Persists data incrementally into a relational cloud database hosted with low latency.
3. **Automation (GitHub Actions)**: Runs the ETL pipeline autonomously every hour via cloud cron jobs.
4. **Analytical Product (`app.py`)**: A lightweight, high-performance interactive web dashboard built with Streamlit.

---

## 🛠️ Tech Stack
* **Language:** Python (Pandas, Requests, SQLAlchemy, Streamlit)
* **Database:** PostgreSQL (Neon.tech - Cloud Serverless DB)
* **CI/CD Automation:** GitHub Actions (Cron Scheduler)
* **Environment Management:** python-dotenv, Git/GitHub

---

## 📁 Project Structure
crypto-analytics-pipeline/
```text
│
├── .github/
│   └── workflows/
│       └── pipeline.yml       # GitHub Actions hourly automation workflow
│
├── assets/
│   └── screenshot.png         # Dashboard preview image
│
├── crypto_pipeline.py         # Resilient ETL script (Binance -> PostgreSQL)
├── app.py                     # Streamlit analytical web dashboard
├── requirements.txt           # Project dependencies
├── .env.example               # Template for environment variables
└── .gitignore                 # Files and folders ignored by Git
```

## ⚙️ How to Install & Run Locally

**Prerequisites**
Make sure you have Python 3.10+ and Git installed on your system.

**Step 1: Clone the Repository**
```bash
git clone https://github.com/cb-rizzo/crypto-analytics-pipeline.git
cd crypto-analytics-pipeline
```

**Step 2: Set Up a Virtual Environment**
```bash
python -m venv venv

# Activate on Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Activate on Mac/Linux:
source venv/bin/activate
```

**Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Configure Environment Variables**
Duplicate the `.env.example` file and rename the copy to `.env`.
Open your `.env` file and replace the placeholder with your actual PostgreSQL connection string from Neon.tech:
```env
DATABASE_URL=postgresql://your_user:your_password@your_host/your_database?sslmode=require
```

**Step 5: Run the ETL Pipeline Manually**
Test the extraction and loading process locally:
```bash
python crypto_pipeline.py
```

**Step 6: Launch the Streamlit Dashboard**
Open the interactive analytical web application:
```bash
streamlit run app.py
```
