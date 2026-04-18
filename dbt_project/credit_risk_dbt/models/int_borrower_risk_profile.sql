with borrowers as (

    select * from {{ ref('stg_borrowers') }}

),

loan_perf as (

    select * from {{ ref('int_loan_performance') }}

),

borrower_summary as (

    select
        borrower_id,
        count(*) as total_loans,
        sum(principal_amount) as total_principal,
        sum(case when loan_status = 'defaulted' then 1 else 0 end) as defaulted_loans
    from loan_perf
    group by borrower_id

),

final as (

    select
        b.borrower_id,
        b.full_name,
        b.state_code,
        b.employment_type,
        b.annual_income,
        b.credit_score,
        b.debt_to_income_ratio,

        coalesce(s.total_loans, 0) as total_loans,
        coalesce(s.total_principal, 0) as total_principal,
        coalesce(s.defaulted_loans, 0) as defaulted_loans,

        case
            when b.credit_score >= 750 and b.debt_to_income_ratio <= 0.20 then 'LOW'
            when b.credit_score >= 680 and b.debt_to_income_ratio <= 0.35 then 'MEDIUM'
            when b.credit_score >= 620 and b.debt_to_income_ratio <= 0.50 then 'HIGH'
            else 'VERY_HIGH'
        end as borrower_risk_tier

    from borrowers b
    left join borrower_summary s
        on b.borrower_id = s.borrower_id

)

select * from final