table_and_descriptions = {
    "order_values": "This table contains order information aggregated across multiple sources for an e-commerce brand. The table is unique at an Order ID - SKU ID level. The table includes, but is not limited to, all pricing information (like gross sales, tax, net sales, shipping charge, duties, etc.), information related to the product (like SKU, product id/title, price, etc.), order related information (timestamp of order), payment information and shipping information.",
}

table_to_column_mapping = {
    "order_values": {
        "order_line_item_id": {
            "description": "Unique identifier for each line item in an order",
            "values_sample": ["shopify_5667598663969_14461737632033"],
        },
        "source": {
            "description": "Channel the order was placed on",
            "values_sample": ["shopify"],
        },
        "order_id": {
            "description": "Unique identifier for each order",
            "values_sample": ["shopify_5667598663969"],
        },
        "ordered_quantity": {
            "description": "Quantity of each item of a line item",
            "values_sample": [1],
        },
        "tax_percent": {
            "description": "Tax percentage applied to the order",
            "values_sample": [0.17999949556658],
        },
        "gross_sales_price_before_tax": {
            "description": "Gross sales for the line item in an order",
            "values_sample": [846.610531405632],
        },
        "total_discount_before_tax": {
            "description": "Discount for the line item in an order",
            "values_sample": [0],
        },
        "total_cancellation_returns_before_tax": {
            "description": "Amount of cancelled orders",
            "values_sample": [846.610531405632],
        },
        "total_rto_returns_before_tax": {
            "description": "Amount of RTO (Return to Origin) orders",
            "values_sample": [846.610531405632],
        },
        "total_returns_refund_before_tax": {
            "description": "Amount of Returned Orders excluding RTO",
            "values_sample": [846.610531405632],
        },
        "total_returns_before_tax": {
            "description": "Total Amount of Returned Orders including RTO",
            "values_sample": [846.610531405632],
        },
        "net_sales_before_tax": {
            "description": "Net sales amount before applying tax",
            "values_sample": [0],
        },
        "item_shipping_charge": {
            "description": "Shipping income/revenue collected from the customer for an item",
            "values_sample": [0],
        },
        "item_duties": {
            "description": "Duties collected from the customer for an item",
            "values_sample": [0],
        },
        "item_additional_feels": {
            "description": "Additional fees collected from the customer for an item",
            "values_sample": [0],
        },
        "total_tax": {"description": "Total tax amount", "values_sample": [0]},
        "gros_merchandise_value": {
            "description": "Gross Merchandise Value (GMV) for an item",
            "values_sample": [0],
        },
        "sku_id": {
            "description": "Unique identifier for each stock keeping unit (SKU)",
            "values_sample": ["shopify_8848983261473_47478863036705"],
        },
        "sku_code": {
            "description": "Code assigned to each stock keeping unit (SKU)",
            "values_sample": ["BSL-D-SIP-0001"],
        },
        "product_category": {
            "description": "Category of the product",
            "values_sample": ["Insulated Sipper"],
        },
        "product_id": {
            "description": "Unique identifier for each product",
            "values_sample": ["shopify_8848983261473"],
        },
        "product_title": {
            "description": "Title of the product",
            "values_sample": ["Kids Sipper (430 ml)"],
        },
        "product_price": {
            "description": "Price of the product",
            "values_sample": [999],
        },
        "customer_id": {
            "description": "Unique identifier for each customer",
            "values_sample": ["shopify_7694075199777"],
        },
        "first_ordered_at": {
            "description": "Timestamp of the first order",
            "values_sample": ["2024-02-14 16:00:13.000000"],
        },
        "order_refund_line_item_id": {
            "description": "Unique identifier for each refunded line item in an order",
            "values_sample": ["shopify_5667598663969_14461737632033"],
        },
        "order_date_time": {
            "description": "Date and time of the order",
            "values_sample": ["2024-02-14 16:00:13.000000"],
        },
        "order_date": {
            "description": "Date of the order",
            "values_sample": ["2024-02-14"],
        },
        "order_year": {"description": "Year of the order", "values_sample": [2024]},
        "order_quarter": {
            "description": "Quarter of the year of the order",
            "values_sample": [1],
        },
        "order_month": {"description": "Month of the order", "values_sample": [2]},
        "order_day_of_month": {
            "description": "Day of the month of the order",
            "values_sample": [14],
        },
        "order_week": {
            "description": "Week of the year of the order",
            "values_sample": [7],
        },
        "order_day_of_week": {
            "description": "Day of the week of the order",
            "values_sample": [4],
        },
        "order_hour": {
            "description": "Hour of the day of the order",
            "values_sample": [16],
        },
        "order_minute": {
            "description": "Minute of the hour of the order",
            "values_sample": [0],
        },
        "order_time": {"description": "Time of the order", "values_sample": ["16:00"]},
        "cancellation_status": {
            "description": "Status of order cancellation",
            "values_sample": ["false"],
        },
        "rto_status": {
            "description": "Status of RTO for the order",
            "values_sample": ["false"],
        },
        "refund_status": {
            "description": "Status of order refund",
            "values_sample": ["false"],
        },
        "order_status": {
            "description": "Status of the order",
            "values_sample": ["fulfilled"],
        },
        "payment_status": {
            "description": "Status of payment for the order",
            "values_sample": ["pending"],
        },
        "billing_address_city": {
            "description": "City in the customer address",
            "values_sample": ["Surat"],
        },
        "billing_address_state": {
            "description": "State in the customer address",
            "values_sample": ["Gujarat"],
        },
        "billing_address_country": {
            "description": "Country in the customer address",
            "values_sample": ["India"],
        },
        "packaging_expense": {
            "description": "Expenses associated with packaging of goods",
            "values_sample": [0],
        },
        "handling_expense": {
            "description": "Expenses associated with handling of goods",
            "values_sample": [0],
        },
        "shipping_expense": {
            "description": "Shipping/logistics expense for the items",
            "values_sample": [56.05],
        },
        "marketplace_expense": {
            "description": "Fees paid to the marketplace like Amazon/Flipkart",
            "values_sample": [79.34],
        },
        "payment_gateway_expense": {
            "description": "Expenses associated with collecting payments",
            "values_sample": [0],
        },
        "other_adjustments": {
            "description": "Other miscellaneous expenses",
            "values_sample": [0],
        },
        "sku_cost": {
            "description": "Cost of Goods Sold (COGS)",
            "values_sample": [198.32],
        },
        "gross_profit": {
            "description": "Gross Profit/Margin for the item",
            "values_sample": [475.24],
        },
        "profit_cm1": {
            "description": "Contribution Margin 1 (CM1 Profit) for the item",
            "values_sample": [339.83],
        },
    },
}
