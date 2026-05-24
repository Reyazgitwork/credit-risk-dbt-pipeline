<div align="center">

# 🏦 Credit Risk Analytics Pipeline

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=16&pause=1000&color=58A6FF&center=true&vCenter=true&width=700&lines=End-to-end+Credit+Risk+Analytics+with+dbt+%2B+DuckDB+%2B+Airflow;Staging+%E2%86%92+Intermediate+%E2%86%92+Mart+Layered+Architecture;Automated+KPI+Computation+%7C+Risk+Tier+Classification;Production-Grade+ELT+Pipeline+%F0%9F%9A%80" alt="Typing SVG" />

<br/>

![dbt](https://img.shields.io/badge/dbt_Core-FF694B?style=for-the-badge&logo=dbt&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)
![Airflow](https://img.shields.io/badge/Apache_Airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-Advanced-003B57?style=for-the-badge&logo=postgresql&logoColor=white)

[![Stars](https://img.shields.io/github/stars/Reyazgitwork/credit-risk-dbt-pipeline?style=social)](https://github.com/Reyazgitwork/credit-risk-dbt-pipeline/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/Reyazgitwork/credit-risk-dbt-pipeline?color=58A6FF)](https://github.com/Reyazgitwork/credit-risk-dbt-pipeline/commits/main)
[![License](https://img.shields.io/github/license/Reyazgitwork/credit-risk-dbt-pipeline)](LICENSE)

</div>

---

## 📌 Overview

A **production-grade credit risk analytics pipeline** built on the modern data stack. This project ingests raw borrower, loan, and payment data, transforms it through a structured **Staging → Intermediate → Fact** dbt layer, and surfaces key credit risk KPIs — all orchestrated by **Apache Airflow**.

Designed to mirror real-world **financial analytics workflows** used at banks, fintechs, and credit institutions.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                             │
│         CSV Files (Borrowers · Loans · Payments)                │
│                   [ data_generator/ ]                           │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     ORCHESTRATION LAYER                         │
│              Apache Airflow DAG  [ airflow/dags/ ]              │
│   ┌──────────┐  ┌──────────────┐  ┌──────────┐  ┌──────────┐  │
│   │ Ingest   │→ │  dbt run     │→ │ dbt test │→ │  Alert   │  │
│   └──────────┘  └──────────────┘  └──────────┘  └──────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   dbt TRANSFORMATION LAYERS                     │
│                                                                 │
│  STAGING (raw → clean)                                          │
│  ├── stg_borrowers        ← borrower demographics & scores      │
│  ├── stg_loans            ← loan terms, amounts, status         │
│  └── stg_payments         ← payment history & schedules         │
│                                                                 │
│  INTERMEDIATE (business logic)                                  │
│  ├── int_loan_performance ← on-time rates, delinquency flags    │
│  └── int_borrower_risk_profile ← risk tier classification       │
│                                                                 │
│  FACT / MART (analytics-ready)                                  │
│  └── fct_credit_risk_kpis ← portfolio KPIs & health scores      │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     ANALYTICAL LAYER                            │
│              DuckDB  (in-process OLAP engine)                   │
│         Fast local querying · Zero infrastructure overhead      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 dbt Models

### 🥉 Staging Layer — Raw → Cleaned

| Model | Description |
|-------|-------------|
| `stg_borrowers` | Cleans and casts borrower demographics, credit scores, employment info |
| `stg_loans` | Standardizes loan amounts, terms, interest rates, and statuses |
| `stg_payments` | Normalizes payment records, timestamps, and scheduled vs actual amounts |

### 🥈 Intermediate Layer — Business Logic

| Model | Description |
|-------|-------------|
| `int_loan_performance` | Computes on-time payment rates, days past due, delinquency & NPA flags |
| `int_borrower_risk_profile` | Calculates repayment ratios and assigns borrower risk tiers (Low / Medium / High) |

### 🥇 Fact / Mart Layer — KPI Output

| Model | Description |
|-------|-------------|
| `fct_credit_risk_kpis` | Aggregates all metrics into a single portfolio health scorecard |

---

## 📈 Key Metrics Produced

| Metric | Description |
|--------|-------------|
| **Collection Efficiency** | % of expected payments successfully collected |
| **Borrower Risk Tier** | Categorical risk classification: Low / Medium / High |
| **Delinquency Flag** | Identifies loans with missed or late payments |
| **NPA Flag** | Non-Performing Asset classification trigger |
| **Repayment Ratio** | Total repaid vs total disbursed across loan lifecycle |
| **Portfolio Health Score** | Composite score summarizing overall credit portfolio quality |

---

## 🗂️ Project Structure

```
credit-risk-dbt-pipeline/
│
├── airflow/
│   └── dags/                    # Airflow DAG definitions
│       └── credit_risk_dag.py   # Main pipeline orchestration DAG
│
├── data_generator/              # Synthetic data generation scripts
│   └── generate_data.py         # Creates borrowers, loans, payments CSVs
│
├── dbt_project/                 # dbt Core project
│   ├── models/
│   │   ├── staging/             # stg_borrowers, stg_loans, stg_payments
│   │   ├── intermediate/        # int_loan_performance, int_borrower_risk_profile
│   │   └── marts/               # fct_credit_risk_kpis
│   ├── tests/                   # Custom dbt data tests
│   ├── macros/                  # Reusable SQL macros
│   ├── dbt_project.yml
│   └── profiles.yml
│
├── .gitignore
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Data Generation | Python | Synthetic borrower/loan/payment data |
| Transformation | dbt Core | Modular SQL models, tests, documentation |
| Query Engine | DuckDB | In-process OLAP — fast, zero setup |
| Orchestration | Apache Airflow | DAG scheduling, task dependencies, failure alerting |
| Version Control | Git & GitHub | Code management and collaboration |

---

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.9+
pip install dbt-duckdb apache-airflow
```

### 1. Clone the repository

```bash
git clone https://github.com/Reyazgitwork/credit-risk-dbt-pipeline.git
cd credit-risk-dbt-pipeline
```

### 2. Generate synthetic data

```bash
cd data_generator
python generate_data.py
```

### 3. Run dbt models

```bash
cd dbt_project
dbt deps
dbt run
dbt test
```

### 4. Run the full pipeline with Airflow

```bash
# Initialize Airflow
export AIRFLOW_HOME=$(pwd)/airflow
airflow db init

# Copy DAG
cp airflow/dags/credit_risk_dag.py $AIRFLOW_HOME/dags/

# Start Airflow
airflow standalone
```

Then open `http://localhost:8080` → trigger the `credit_risk_pipeline` DAG.

### 5. Query results directly with DuckDB

```python
import duckdb

con = duckdb.connect("dbt_project/dev.duckdb")
df = con.execute("SELECT * FROM fct_credit_risk_kpis LIMIT 10").df()
print(df)
```

---

## 🧪 Data Quality & Testing

dbt tests are configured at every layer:

- ✅ `not_null` — critical ID and metric fields
- ✅ `unique` — borrower_id, loan_id primary keys
- ✅ `accepted_values` — risk_tier, loan_status, delinquency_flag
- ✅ `relationships` — referential integrity between staging models
- ✅ Custom tests — repayment ratio range, NPA flag logic validation

Run all tests:

```bash
dbt test
```

---

## 🤝 Connect

**Mohammad Reyaz Shaik**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mohammad-reyaz-shaik)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Reyazgitwork)

---

<div align="center">
<sub>Built with ❤️ using dbt · DuckDB · Airflow · Python</sub>
</div>
