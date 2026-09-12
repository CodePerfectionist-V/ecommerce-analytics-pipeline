with source as (
    select * from {{ ref('cleaned_ecom_data') }}
),

renamed as (
    select
        cast(Customer_ID as text)            as customer_id,
        cast(Transaction_Date as date)       as transaction_date,
        lower(trim(Product_Category))        as category_name,
        cast(Revenue as numeric(12,2))       as total_revenue_usd,
        cast(Year as integer)                as transaction_year,
        cast(Month as integer)               as transaction_month,
        cast(Day as integer)                 as transaction_day,
        cast(Day_of_Week as text)            as transaction_day_of_week
    from source
)

select * from renamed