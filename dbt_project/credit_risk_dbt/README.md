# Credit Risk Analytics Pipeline

This project builds a credit risk analytics pipeline using dbt and DuckDB.

## Tech Stack
- Python
- dbt
- DuckDB
- CSV files

## Models

### Staging
- stg_borrowers
- stg_loans
- stg_payments

### Intermediate
- int_loan_performance
- int_borrower_risk_profile

### Final
- fct_credit_risk_kpis

## Metrics
- collection efficiency
- borrower risk tier
- delinquency flag
- NPA flag
- repayment ratio
- portfolio health score

## Run Project

```bash
dbt run
dbt test