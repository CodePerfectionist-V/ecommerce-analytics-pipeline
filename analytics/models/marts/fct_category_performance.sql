with orders as (
    select * from {{ ref('stg_ecom_orders') }}
),

category_aggregations as (
    select
        category_name,
        count(*)                          as total_transactions,
        count(distinct customer_id)       as unique_customers,
        sum(total_revenue_usd)           as gross_revenue_usd,
        round(avg(total_revenue_usd), 2) as average_order_value_usd
    from orders
    group by 1
)

select
    category_name,
    total_transactions,
    unique_customers,
    gross_revenue_usd,
    average_order_value_usd,
    dense_rank() over (order by gross_revenue_usd desc) as revenue_rank
from category_aggregations