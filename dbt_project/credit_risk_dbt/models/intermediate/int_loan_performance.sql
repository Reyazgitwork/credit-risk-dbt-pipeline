with loans as (

    select * from {{ ref('stg_loans') }}

),

payments as (

    select * from {{ ref('stg_payments') }}

),

payment_summary as (

    select
        loan_id,
        count(*) as total_installments,
        sum(expected_amount) as total_expected_amount,
        sum(payment_amount) as total_paid_amount
    from payments
    group by loan_id

),

final as (

    select
        l.loan_id,
        l.borrower_id,
        l.loan_grade,
        l.loan_purpose,
        l.principal_amount,
        l.interest_rate,
        l.term_months,
        l.loan_status,

        coalesce(p.total_installments, 0) as total_installments,
        coalesce(p.total_expected_amount, 0) as total_expected_amount,
        coalesce(p.total_paid_amount, 0) as total_paid_amount,

        case
            when coalesce(p.total_expected_amount, 0) = 0 then 0
            else round(p.total_paid_amount / p.total_expected_amount, 4)
        end as collection_efficiency

    from loans l
    left join payment_summary p
        on l.loan_id = p.loan_id

)

select * from final