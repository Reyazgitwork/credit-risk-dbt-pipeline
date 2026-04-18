with loans as (

    select * from {{ ref('int_loan_performance') }}

),

borrowers as (

    select * from {{ ref('int_borrower_risk_profile') }}

),

final as (

    select
        l.loan_id,
        l.borrower_id,
        b.borrower_risk_tier,
        l.loan_grade,
        l.principal_amount,
        l.total_expected_amount,
        l.total_paid_amount,
        l.loan_status,

        case when l.total_paid_amount < l.total_expected_amount then 1 else 0 end as is_delinquent,

        case when l.loan_status = 'defaulted' then 1 else 0 end as is_npa,

        case
            when l.total_expected_amount = 0 then 0
            else round(l.total_paid_amount / l.total_expected_amount, 4)
        end as repayment_ratio,

        round(
            100
            - (case when l.loan_status = 'defaulted' then 40 else 0 end)
            - (case when l.total_paid_amount < l.total_expected_amount then 20 else 0 end)
            - (case when b.borrower_risk_tier = 'VERY_HIGH' then 20
                    when b.borrower_risk_tier = 'HIGH' then 10
                    when b.borrower_risk_tier = 'MEDIUM' then 5
                    else 0 end)
        , 2) as portfolio_health_score

    from loans l
    left join borrowers b
        on l.borrower_id = b.borrower_id

)

select * from final