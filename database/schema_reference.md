# Schema Reference

This project stores retail sales data in a MySQL database named `retail_agent_assignment`.

## Source files

- `data/stores.csv` → `stores`
- `data/products.csv` → `products`
- `data/customers.csv` → `customers`
- `data/sales_transactions.csv` → `sales_transactions`
- `data/returns.csv` → `returns`

## Tables

### stores
- `store_id` (PRIMARY KEY)
- `store_name`
- `region`
- `city`
- `store_type`

### products
- `product_id` (PRIMARY KEY)
- `product_name`
- `category`
- `sub_category`
- `base_price`

### customers
- `customer_id` (PRIMARY KEY)
- `customer_segment`
- `signup_date`
- `preferred_channel`
- `city`

### sales_transactions
- `order_id` (PRIMARY KEY)
- `order_date`
- `store_id`
- `product_id`
- `customer_id`
- `sales_channel`
- `units_sold`
- `unit_price`
- `discount_pct`
- `payment_status`
- `delivery_status`

Foreign keys:
- `store_id` → `stores(store_id)`
- `product_id` → `products(product_id)`
- `customer_id` → `customers(customer_id)`

### returns
- `return_id` (PRIMARY KEY)
- `order_id`
- `return_date`
- `return_reason`

Foreign key:
- `order_id` → `sales_transactions(order_id)`

## Import order

The CSV files should be loaded in this order to preserve relationships:
1. `stores`
2. `products`
3. `customers`
4. `sales_transactions`
5. `returns`

## Loader script

The import logic is implemented in `database/load_data.py`.
Run it with:

```bash
python database/load_data.py
```

If your MySQL server uses non-default credentials, set:
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DATABASE`
