TABLE_DESCRIPTIONS = {
    "order_values": "This table contains order information aggregated across multiple sources for an e-commerce brand. The table is unique at an Order ID - SKU ID level. The table includes, but is not limited to, all pricing information (like gross sales, tax, net sales, shipping charge, duties, etc.), information related to the product (like SKU, product id/title, price, etc.), order related information (timestamp of order), payment information and shipping information."
}

COLUMNS = {
    "order_values": {
        "order_line_item_id": {
            "description": "Unique identifier for each line item in an order",
            "values_sample": ["shopify_5667598663969_14461737632033"],
        },
        "source": {"description": "Source of the order", "values_sample": ["shopify"]},
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
        "total_price_tax": {
            "description": "Total price including tax",
            "values_sample": [152.389468594368],
        },
        "gross_sales_price_before_tax": {
            "description": "Gross sales price before applying tax",
            "values_sample": [846.610531405632],
        },
        "total_discount_after_tax": {
            "description": "Total discount after applying tax",
            "values_sample": [0],
        },
        "total_discount_tax": {
            "description": "Total discount amount subject to tax",
            "values_sample": [0],
        },
        "total_discount_before_tax": {
            "description": "Total discount before applying tax",
            "values_sample": [0],
        },
        "total_returns_before_tax": {
            "description": "Total return/refund amount before tax",
            "values_sample": [846.610531405632],
        },
        "net_sales_before_tax": {
            "description": "Net sales amount before applying tax",
            "values_sample": [0],
        },
        "item_shipping_charge": {
            "description": "Shipping charge for an item",
            "values_sample": [0],
        },
        "item_duties": {
            "description": "Duties charged for an item",
            "values_sample": [0],
        },
        "item_additional_feels": {
            "description": "Additional fees charged for an item",
            "values_sample": [0],
        },
        "total_tax": {"description": "Total tax amount", "values_sample": [0]},
        "total_sales_after_tax": {
            "description": "Total sales amount after applying tax",
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
        "refund_status": {
            "description": "Status of order refund",
            "values_sample": ["false"],
        },
        "order_status": {
            "description": "Status of the order",
            "values_sample": ["unknown"],
        },
        "payment_status": {
            "description": "Status of payment for the order",
            "values_sample": ["pending"],
        },
        "shipping_address_city": {
            "description": "City of the shipping address",
            "values_sample": ["Surat"],
        },
        "shipping_address_state": {
            "description": "State of the shipping address",
            "values_sample": ["Gujarat"],
        },
        "shipping_address_country": {
            "description": "Country of the shipping address",
            "values_sample": ["India"],
        },
    }
}


# Sample queries for the entire database
# This will be of format: [{'question': <the sample user question>, 'query': <the sql query>, 'description': <description of the query>}, ...]
DATABASE_SAMPLE_QUERIES = [
    {
        "question": "sales trend for last 6 months",
        "query": "SELECT CONCAT(order_year, '-', LPAD(order_month, 2, '0')) AS order_date, SUM(COALESCE(net_sales_before_tax, 0)) AS net_sales FROM order_values WHERE TO_DATE(CONCAT(order_year, '-', LPAD(order_month, 2, '0')), 'yyyy-MM') >= DATE_TRUNC('month', ADD_MONTHS(CURRENT_DATE, -6)) AND TO_DATE(CONCAT(order_year, '-', LPAD(order_month, 2, '0')), 'yyyy-MM') < DATE_TRUNC('month', CURRENT_DATE) GROUP BY order_year, order_month ORDER BY order_year, order_month;",
        "logic": "This query calculates monthly sales for the last 6 months. Note that last 6 months does NOT mean last 180 days. If we're on May 15 2024,to get the last 6 full months excluding the current month (May 2024), we need the following: Start date: First day of the month six months ago. End date: Last day of the previous month. Finally we are concatenating the Order Year and Order Month because they are separate columns in the table and we only want 2 columns in the output for ease of plotting. As the net_sales_before_tax column might contain null values, we use coalesce.",
        "response": "Sure, here is a trend of net sales for the last 6 months. I have not included the numbers of the current month since you asked for the last 6 months.",
        "chart": {
            "type": "line",
            "x_axis": ["order_date"],
            "y_axis": ["net_sales"],
            "logic": "Since it is a trend, we'll use a line chart.",
        },
    },
    {
        "question": "What are my sales for the last quarter?",
        "query": "WITH last_completed_quarter AS (SELECT CASE WHEN order_quarter = 1 THEN order_year - 1 ELSE order_year END AS last_quarter_year, CASE WHEN order_quarter = 1 THEN 4 ELSE order_quarter - 1 END AS last_quarter FROM order_values GROUP BY order_year,order_quarter ORDER BY order_year DESC, order_quarter DESC LIMIT 1) SELECT SUM(COALESCE(net_sales_before_tax, 0)) AS total_sales_last_quarter FROM order_values o JOIN last_completed_quarter lq ON o.order_year = lq.last_quarter_year AND o.order_quarter = lq.last_quarter;",
        "logic": "This query calculates the sales for the last quarter in the data. Note that the query dynamically calculates the last completed quarter using a series of CASE WHEN statements instead of hardcoding a value. We use coalesce as the net_sales_before_tax_column might contain null values.",
        "response": "Certainly, your net sales for last quarter are below.",
        "chart": {
            "type": "null",
            "x_axis": ["null"],
            "y_axis": ["null"],
            "logic": "The question asks for a single value. So no chart is needed.",
        },
    },
    {
        "question": "Give me the revenue split for the last month by channel.",
        "query": "SELECT source, SUM(net_sales_before_tax) AS net_sales FROM order_values WHERE order_year = YEAR(DATE_SUB(CURRENT_DATE, DAY(CURRENT_DATE))) AND order_month = MONTH(DATE_SUB(CURRENT_DATE, DAY(CURRENT_DATE))) GROUP BY source;",
        "logic": "This query retrieves the revenue split for the last month, comparing the channels, e.g. Amazon and Shopify.",
        "response": "Here you go! Here's the trend of orders for the last 4 quarters. I have also included the current quarter.",
        "chart": {
            "type": "pie",
            "x_axis": ["source"],
            "y_axis": ["net_sales"],
            "logic": "Since we're showing a distribution over a small number of values, we will use a pie chart.",
        },
    },
    {
        "question": "net revenue for the last 180 days",
        "query": "SELECT SUM(net_sales_before_tax) AS total_sales_last_180_days FROM order_values WHERE order_date >= DATE_ADD(CURRENT_DATE, -180);",
        "logic": "This query calculates the net sales for the 180 days. Net revenue and net sales are the same thing. For this query, since the data for last 180 days is needed, the DATE_ADD function is used with the syntax DATE_ADD(date, numDays).",
        "response": "Certainly, your net revenue for the last 180 days are below.",
        "chart": {
            "type": "null",
            "x_axis": ["null"],
            "y_axis": ["null"],
            "logic": "The question asks for a single value. So no chart is needed.",
        },
    },
    {
        "question": "What is the average order value of first time customers?",
        "query": "WITH order_totals AS (SELECT order_id, SUM(net_sales_before_tax) AS total_net_sales_before_tax FROM order_values GROUP BY order_id), first_orders AS (SELECT customer_id, MIN(order_date) AS first_order_date FROM order_values GROUP BY customer_id) SELECT AVG(ot.total_net_sales_before_tax) AS avg_net_sales_aov_first_time_customers FROM order_totals ot JOIN order_values o ON ot.order_id = o.order_id JOIN first_orders f ON o.customer_id = f.customer_id AND o.order_date = f.first_order_date;",
        "logic": "Since the table order_values is at an Order ID - SKU ID level, the order_totals CTE calculates the total sales at an Order ID level. Then the first order date for customers is calculated in the first_orders CTE. Finally in the main query everything is merged to get the average order value for first time customers. Note that net_sales_before_tax is used for average order value calculation. The question asks for a single value. So no chart is needed.",
        "response": "Sure, the Average Order Value for first time customers, i.e. orders for which the first order date = order date is below. I have used net sales to calculate AOV.",
        "chart": {
            "type": "null",
            "x_axis": ["null"],
            "y_axis": ["null"],
            "logic": "The question asks for a single value. So no chart is needed.",
        },
    },
    {
        "question": "weekly breakdown of gross sales for the current year",
        "query": "SELECT CONCAT(order_year, '-W', LPAD(order_week, 2, '0')) AS year_week,SUM(gross_sales_price_before_tax) AS total_gross_sales FROM order_values WHERE order_year = YEAR(CURRENT_DATE) GROUP BY order_year, order_week ORDER BY order_year, order_week;",
        "logic": "This query calculates the weekly gross sales for the current year. The current year is calculated dynamically based on the current date. The week and year columns are concatenated so that the final output can have 2 columns for ease of plotting.",
        "response": "Here you go! I plotted the weekly breakdown of gross sales for this year.",
        "chart": {
            "type": "line",
            "x_axis": ["year_week"],
            "y_axis": ["total_gross_sales"],
            "logic": "Since it is a trend, we'll use a line chart.",
        },
    },
    {
        "question": "What was the AOV for last month?",
        "query": "SELECT AVG(total_net_sales) AS avg_order_value FROM (SELECT order_id, SUM(net_sales_before_tax) AS total_net_sales FROM order_values WHERE order_date >= DATE_TRUNC('month', ADD_MONTHS(CURRENT_DATE, -1)) AND order_date < DATE_TRUNC('month', CURRENT_DATE) GROUP BY order_id) AS order_totals;",
        "logic": "This query calculates the average order value for the month prior to the current month dynamically. Since the table order_values is unique at an Order ID - SKU ID level, first we aggregate the net sales by order ID for the last month. Then we get the average of the net sales. Note that last month means the month prior to the current month and not last 30 days. The question asks for a single value. So no chart is needed.",
        "response": "Here you go! The Average Order Value for last month is below. I have used net sales to calculate AOV. Also, I have calculated this for the last month and NOT for the last 30 days",
        "chart": {
            "type": "null",
            "x_axis": ["null"],
            "y_axis": ["null"],
            "logic": "The question asks for a single value. So no chart is needed.",
        },
    },
    {
        "question": "Show me the trend of sales by source for the last 6 months",
        "query": "SELECT CONCAT(order_year, '-', LPAD(order_month, 2, '0')) AS order_date, source, SUM(COALESCE(net_sales_before_tax, 0)) AS net_sales FROM order_values WHERE TO_DATE(CONCAT(order_year, '-', LPAD(order_month, 2, '0')), 'yyyy-MM') >= DATE_TRUNC('month', ADD_MONTHS(CURRENT_DATE, -6)) AND TO_DATE(CONCAT(order_year, '-', LPAD(order_month, 2, '0')), 'yyyy-MM') < DATE_TRUNC('month', CURRENT_DATE) GROUP BY order_year, order_month, source ORDER BY order_year, order_month, source;",
        "logic": "This query aggregates net sales by source and month for the last 6 months, excluding the current month.",
        "response": "Absolutely! Here is the trend of sales by source for the last 6 months.",
        "chart": {
            "type": "line",
            "x_axis": ["order_date"],
            "y_axis": ["source", "net_sales"],
            "logic": "Since it is a trend, we'll use a line chart. Since we're aggregating by both order_date and source, we have put both in the x-axis so that we can have 2 series.",
        },
    },
    {
        "question": "How many of my customers have purchased more than once within the last 12 months?",
        "query": "SELECT COUNT(DISTINCT customer_id) AS customers_with_multiple_purchases FROM (SELECT customer_id, COUNT(DISTINCT order_id) AS number_of_orders FROM order_values WHERE order_date BETWEEN DATE_SUB(CURRENT_DATE, 365) AND CURRENT_DATE GROUP BY customer_id HAVING COUNT(DISTINCT order_id) > 1) AS subquery;",
        "logic": "This query calculates the number of customers who have purchased more than one time in the last 12 months. For this query, since the data for last 12 months is needed, the DATE_SUB function is used with the syntax DATE_SUB(date, numDays). The question asks for a single value. So no chart is needed.",
        "response": "Sure! Here is the data you requested for. I found the unique count of customers who have made more than 1 order within the last 365 days.",
        "chart": {
            "type": "null",
            "x_axis": ["null"],
            "y_axis": ["null"],
            "logic": "The question asks for a single value. So no chart is needed.",
        },
    },
    {
        "question": "orders by state for April?",
        "query": "SELECT LOWER(shipping_address_state) AS state, COUNT(DISTINCT order_id) AS order_count FROM order_values WHERE order_month = 4 AND order_year = YEAR(CURRENT_DATE) AND shipping_address_state IS NOT NULL GROUP BY LOWER(shipping_address_state) ORDER BY order_count DESC;",
        "logic": "This query calculates the number of orders by state. Note here that since we have to perform operation on a text column, it must be cast into lowercase, since the data in the database may contain multiple entries with different cases. Note that null values are filtered out since the state column has a high probability of containing null values. Also the year is set to the current year to avoid incorrectly calculating the values for April across all years. Colloquially, when we say April, we mean the most recent April.",
        "response": "Sure! Here is the total number of orders for April by state. Note that this number also includes cancelled and returned orders",
        "chart": {
            "type": "bar",
            "x_axis": ["state"],
            "y_axis": ["order_count"],
            "logic": "We'll use a bar chart since the question asks for an aggregation of a numerical field by a categorical field which is not a date/month.",
        },
    },
    {
        "question": "What is the quarterly trend of orders for the last 4 quarters?",
        "query": "SELECT CONCAT(order_year, '-Q', order_quarter) AS year_quarter, COUNT(DISTINCT order_id) AS total_orders FROM order_values WHERE (order_year, order_quarter) IN (SELECT order_year, order_quarter FROM order_values GROUP BY order_year, order_quarter ORDER BY order_year DESC, order_quarter DESC LIMIT 4) GROUP BY order_year, order_quarter ORDER BY order_year DESC, order_quarter DESC;",
        "logic": "This query aggregates net sales for the last 4 quarters, including the ongoing one. Since the trend of orders is requested, the distinct count of order_id is taken as the table is unique at an Order ID - SKU ID level. We'll plot it in a line chart since it is a trend.",
        "response": "Here you go! Here's the trend of orders for the last 4 quarters. I have also included the current quarter.",
        "chart": {
            "type": "bar",
            "x_axis": ["year_quarter"],
            "y_axis": ["total_orders"],
            "logic": "Since it is a trend, we'll use a line chart.",
        },
    },
]
