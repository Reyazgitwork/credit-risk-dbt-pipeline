import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

fake = Faker()
random.seed(42)
np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

NUM_BORROWERS = 25000
NUM_LOANS = 75000

states = [
    "CA", "TX", "FL", "NY", "NJ", "IL", "WA", "AZ", "GA", "NC",
    "VA", "CO", "MA", "PA", "OH"
]

loan_grades = ["A", "B", "C", "D", "E", "F", "G"]
grade_weights = [0.10, 0.18, 0.22, 0.20, 0.15, 0.10, 0.05]

loan_purposes = [
    "Personal Loan", "Business Loan", "Medical", "Education",
    "Vehicle", "Home Improvement", "Debt Consolidation"
]

employment_types = ["Salaried", "Self-Employed", "Contract", "Business Owner"]

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def build_borrowers(n):
    rows = []
    for borrower_id in range(1, n + 1):
        annual_income = max(25000, int(np.random.normal(85000, 30000)))
        credit_score = int(np.clip(np.random.normal(680, 70), 300, 850))
        dti = round(np.clip(np.random.normal(0.28, 0.12), 0.01, 0.75), 2)

        rows.append({
            "borrower_id": borrower_id,
            "full_name": fake.name(),
            "state_code": random.choice(states),
            "employment_type": random.choice(employment_types),
            "annual_income": annual_income,
            "credit_score": credit_score,
            "debt_to_income_ratio": dti,
            "created_at": fake.date_time_between(start_date="-4y", end_date="now")
        })
    return pd.DataFrame(rows)

def build_loans(n, borrower_ids):
    rows = []
    start_date = datetime.now() - timedelta(days=365 * 3)
    end_date = datetime.now()

    for loan_id in range(1, n + 1):
        borrower_id = random.choice(borrower_ids)
        grade = random.choices(loan_grades, weights=grade_weights, k=1)[0]

        principal = random.choice([5000, 10000, 15000, 20000, 25000, 30000, 50000])
        interest_rate = round(np.clip(np.random.normal(12, 5), 5, 30), 2)
        term_months = random.choice([12, 24, 36, 48, 60])
        disbursal_date = random_date(start_date, end_date - timedelta(days=60))
        maturity_date = disbursal_date + timedelta(days=term_months * 30)

        status_probs = {
            "A": [0.85, 0.10, 0.04, 0.01],
            "B": [0.80, 0.12, 0.06, 0.02],
            "C": [0.72, 0.16, 0.08, 0.04],
            "D": [0.62, 0.20, 0.12, 0.06],
            "E": [0.52, 0.24, 0.16, 0.08],
            "F": [0.42, 0.26, 0.20, 0.12],
            "G": [0.30, 0.28, 0.24, 0.18],
        }

        loan_status = random.choices(
            ["active", "closed", "delinquent", "defaulted"],
            weights=status_probs[grade],
            k=1
        )[0]

        rows.append({
            "loan_id": loan_id,
            "borrower_id": borrower_id,
            "loan_grade": grade,
            "loan_purpose": random.choice(loan_purposes),
            "principal_amount": principal,
            "interest_rate": interest_rate,
            "term_months": term_months,
            "disbursal_date": disbursal_date,
            "maturity_date": maturity_date,
            "loan_status": loan_status,
            "created_at": disbursal_date,
            "updated_at": datetime.now()
        })
    return pd.DataFrame(rows)

def build_payments(loans_df):
    rows = []
    payment_id = 1

    for _, loan in loans_df.iterrows():
        loan_id = int(loan["loan_id"])
        principal = float(loan["principal_amount"])
        interest_rate = float(loan["interest_rate"])
        term_months = int(loan["term_months"])
        disbursal_date = pd.to_datetime(loan["disbursal_date"])
        loan_status = loan["loan_status"]
        monthly_due = round((principal * (1 + (interest_rate / 100))) / term_months, 2)

        months_elapsed = min(term_months, max(1, (datetime.now() - disbursal_date.to_pydatetime()).days // 30))

        for installment_no in range(1, months_elapsed + 1):
            due_date = disbursal_date + pd.Timedelta(days=installment_no * 30)

            if loan_status == "defaulted" and installment_no > max(1, months_elapsed // 2):
                payment_amount = 0
                payment_date = pd.NaT
            else:
                late_days = 0
                if loan_status == "delinquent":
                    late_days = random.randint(15, 120)
                elif random.random() < 0.08:
                    late_days = random.randint(1, 20)

                paid_ratio = 1.0
                if loan_status == "defaulted" and random.random() < 0.3:
                    paid_ratio = random.uniform(0.0, 0.5)

                payment_amount = round(monthly_due * paid_ratio, 2)

                if payment_amount == 0:
                    payment_date = pd.NaT
                else:
                    payment_date = due_date + pd.Timedelta(days=late_days)

            rows.append({
                "payment_id": payment_id,
                "loan_id": loan_id,
                "installment_no": installment_no,
                "due_date": due_date,
                "payment_date": payment_date,
                "payment_amount": payment_amount,
                "expected_amount": monthly_due,
                "created_at": datetime.now()
            })
            payment_id += 1

    return pd.DataFrame(rows)

def main():
    borrowers_df = build_borrowers(NUM_BORROWERS)
    loans_df = build_loans(NUM_LOANS, borrowers_df["borrower_id"].tolist())
    payments_df = build_payments(loans_df)

    borrowers_df.to_csv(os.path.join(OUTPUT_DIR, "borrowers.csv"), index=False)
    loans_df.to_csv(os.path.join(OUTPUT_DIR, "loans.csv"), index=False)
    payments_df.to_csv(os.path.join(OUTPUT_DIR, "payments.csv"), index=False)

    print("Files created successfully:")
    print(f"borrowers: {len(borrowers_df)}")
    print(f"loans: {len(loans_df)}")
    print(f"payments: {len(payments_df)}")

if __name__ == "__main__":
    main()