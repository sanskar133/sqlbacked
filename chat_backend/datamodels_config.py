TABLE_DESCRIPTIONS = {
    "transformed_order": "This table contains order level data",
    "transformed_order_line_item": "This table contains line item level data for all orders. ",
    "transformed_product_variant": "Each row of this table contains information about a variant of a product as a single product can have multiple variants with their own properties",
    "transformed_user": "This table contains information about the customer",
    "transformed_product": "This table has product level data. Any data about the variants of a product are not captured in this table but in the product variant table",
}

TABLE_COLUMN_SAMPLEVALUES_MAPPING = {
    "transformed_order": {
        "order_id": {
            "description": 'Primary Key for this table: source + "_" +  ',
            "values_sample": [],
        },
        "source_platform_name": {
            "description": "Data source such as Amazon, shopify",
            "values_sample": [],
        },
        "source_platform_row_id": {
            "description": "The primary key in the source table",
            "values_sample": [],
        },
        "Final_discount_on_the_order": {
            "description": "The total order level discount",
            "values_sample": [],
        },
        "sum_of_line_item_discount": {
            "description": "The total line item level discount",
            "values_sample": [],
        },
        "order_total_price": {
            "description": "Current Total order price after taking into account all the refunds, tax, discounts, refunds",
            "values_sample": [],
        },
        "order_total_tax": {
            "description": "Total tax calculated on the subtotal",
            "values_sample": [],
        },
        "order_subtotal_price": {
            "description": "Price with discounts without tax",
            "values_sample": [],
        },
        "order_total_weight": {
            "description": "Total weight of all the line items in the order",
            "values_sample": [],
        },
        "order_fulfillment_status": {
            "description": "fulfilled,null,partial,restocked",
            "values_sample": [],
        },
        "order_status_explanation": {
            "description": "Reason for the status of the order",
            "values_sample": [],
        },
        "ordered_at": {
            "description": "Order creation timestamp as per the source",
            "values_sample": [],
        },
        "order_changed_at": {
            "description": "Order updation timestamp as per the source",
            "values_sample": [],
        },
        "internal_created_at": {
            "description": "The timestamp of creation of this entry",
            "values_sample": [],
        },
        "internal_updated_at": {
            "description": "Te timestamp of updation of this entry",
            "values_sample": [],
        },
        "currency": {"description": "Currency of the payment", "values_sample": []},
        "customer_id": {
            "description": "Foreign key to the customer table",
            "values_sample": [],
        },
        "source_platform_customer_id": {
            "description": "Customer id from the customer table",
            "values_sample": [],
        },
        "customer_email": {
            "description": "email address of the customer",
            "values_sample": [],
        },
        "payment_status": {
            "description": "Paid/due/partially refunded",
            "values_sample": [],
        },
        "billing_address_city": {
            "description": "City in the billing address",
            "values_sample": [],
        },
        "billing_address_state": {
            "description": "State in the billing address",
            "values_sample": [],
        },
        "billing_address_company": {
            "description": "Company in the billing address",
            "values_sample": [],
        },
        "billing_address_country": {
            "description": "Country in the billing address",
            "values_sample": [],
        },
        "billing_address_zip": {
            "description": "Zip code of the billing address",
            "values_sample": [],
        },
        "billing_address_name": {
            "description": "Name in the billing address",
            "values_sample": [],
        },
        "shipping_address_city": {
            "description": "City in the shipping address",
            "values_sample": [],
        },
        "shipping_address_state": {
            "description": "State in the shipping address",
            "values_sample": [],
        },
        "shipping_address_country": {
            "description": "Country in the shipping address",
            "values_sample": [],
        },
        "shipping_address_zip": {
            "description": "Zip code of the shipping address",
            "values_sample": [],
        },
        "shipping_address_name": {
            "description": "Name in the shipping address",
            "values_sample": [],
        },
        "internal_is_deleted": {
            "description": "A flag for deleted row",
            "values_sample": [],
        },
        "total_shipping_price": {
            "description": "Shipping price of the order",
            "values_sample": [],
        },
        "order_adjustment_amount": {
            "description": "adjustment amount covering refunds",
            "values_sample": [],
        },
        "order_adjustment_tax_amount": {
            "description": "tax calculated on the adjustment amount",
            "values_sample": [],
        },
        "refund_subtotal": {"description": "Total Refund", "values_sample": []},
        "line_item_count": {
            "description": "Total number of line items in the order",
            "values_sample": [],
        },
        "number_of_fulfilments": {
            "description": "Total number of fulfilments in the order",
            "values_sample": [],
        },
        "order_status": {"description": "pending/cancelled", "values_sample": []},
    },
    "transformed_order_line_item": {
        "order_line_item_id": {"description": "id of this table", "values_sample": []},
        "source_platform_order_line_item_id": {
            "description": "order line item id from the source table ",
            "values_sample": [],
        },
        "source_platform_name": {
            "description": "Source of the data like amazon/shopify",
            "values_sample": [],
        },
        "source_platform_order_id": {
            "description": "Order id from the source table",
            "values_sample": [],
        },
        "source_line_item_id": {
            "description": "line item id from the source table",
            "values_sample": [],
        },
        "order_id": {
            "description": "Foreign keyReference to the order table",
            "values_sample": [],
        },
        "line_item_ordered_at": {
            "description": "Order creation timestamp as per the source",
            "values_sample": [],
        },
        "line_item_updated_at": {
            "description": "Order updation timestamp as per the source",
            "values_sample": [],
        },
        "internal_created_at": {
            "description": "The timestamp of creation of this entry",
            "values_sample": [],
        },
        "internal_updated_at": {
            "description": "The timestamp of updation of this entry",
            "values_sample": [],
        },
        "order_line_item_status": {
            "description": "placed/confirmed/shipped/fulfilled/fully refunded/partially refunded",
            "values_sample": [],
        },
        "order_line_item_status_explanation": {
            "description": "Reason for the status of the order",
            "values_sample": [],
        },
        "line_item_price_per_piece": {
            "description": "price of 1 number of the line item",
            "values_sample": [],
        },
        "line_item_quantity": {
            "description": "the fullfillable quantity",
            "values_sample": [],
        },
        "line_item_total_price": {
            "description": "total price after accounting for tax, discounts, refunds",
            "values_sample": [],
        },
        "line_item_subtotal_price": {
            "description": "total price with discount without tax",
            "values_sample": [],
        },
        "line_item_tax": {
            "description": "total tax on this line item",
            "values_sample": [],
        },
        "total_line_item_discount": {
            "description": "total discount on this line item",
            "values_sample": [],
        },
        "sku_code": {"description": "the sku id", "values_sample": []},
        "source_variant_id": {
            "description": "variant id from the source table",
            "values_sample": [],
        },
        "sku_id": {
            "description": "variant id from the product variant table",
            "values_sample": [],
        },
        "sku_title": {"description": "title of the variant", "values_sample": []},
        "line_item_name": {"description": "name of the line item", "values_sample": []},
        "internal_is_deleted": {
            "description": "A flag for deleted row",
            "values_sample": [],
        },
    },
    "transformed_product_variant": {
        "sku_id": {"description": "Table id", "values_sample": []},
        "sku_listing_date": {
            "description": "Order creation timestamp as per the source",
            "values_sample": [],
        },
        "sku_update_date": {
            "description": "Order updation timestamp as per the source",
            "values_sample": [],
        },
        "internal_created_at": {
            "description": "The timestamp of creation of this entry",
            "values_sample": [],
        },
        "internal_updated_at": {
            "description": "The timestamp of updation of this entry",
            "values_sample": [],
        },
        "source_platform": {
            "description": "Data source such as Amazon, shopify",
            "values_sample": [],
        },
        "source_platform_row_id": {
            "description": "The primary key in the source table",
            "values_sample": [],
        },
        "source_platform_product_id": {
            "description": "Product id as per the source table",
            "values_sample": [],
        },
        "source_platform_sku_id": {
            "description": "Variant id as per the source table",
            "values_sample": [],
        },
        "sku_code": {
            "description": "sku id as per the source table",
            "values_sample": [],
        },
        "sku_title": {"description": "title of the variant", "values_sample": []},
        "inventory_item_id": {
            "description": "inventory item id attached to it as per the source",
            "values_sample": [],
        },
        "sku_item_quantity_in_inventory": {
            "description": "Quantity of the variany in the inventory as per the source",
            "values_sample": [],
        },
        "sku_weight_per_unit": {
            "description": "weight of the single unit",
            "values_sample": [],
        },
        "sku_weight_unit": {
            "description": "the unit of measurement of the weight",
            "values_sample": [],
        },
        "internal_is_deleted": {
            "description": "A flag for deleted row",
            "values_sample": [],
        },
        "sku_unit_sale_price": {
            "description": "Price of the variant",
            "values_sample": [],
        },
        "sku_unit_list_price": {
            "description": "Original Price of the variant",
            "values_sample": [],
        },
        "product_id": {
            "description": "foreign key to the product table",
            "values_sample": [],
        },
    },
    "transformed_user": {
        "customer_id": {"description": "Table id", "values_sample": []},
        "user_created_at": {
            "description": "Order creation timestamp as per the source",
            "values_sample": [],
        },
        "user_updated_at": {
            "description": "Order updation timestamp as per the source",
            "values_sample": [],
        },
        "internal_created_at": {
            "description": "The timestamp of creation of this entry",
            "values_sample": [],
        },
        "internal_updated_at": {
            "description": "The timestamp of updation of this entry",
            "values_sample": [],
        },
        "source_platform": {
            "description": "Data source such as Amazon, shopify",
            "values_sample": [],
        },
        "source_platform_row_id": {
            "description": "The primary key in the source table",
            "values_sample": [],
        },
        "internal_is_deleted": {
            "description": "A flag for deleted row",
            "values_sample": [],
        },
        "customer_name": {"description": "name of the customer", "values_sample": []},
        "customer_city": {"description": "City of the customer", "values_sample": []},
        "customer_state": {"description": "State of the customer", "values_sample": []},
        "customer_country": {
            "description": "Country of the customer",
            "values_sample": [],
        },
        "customer_zip_code": {
            "description": "Zip code of the customer",
            "values_sample": [],
        },
        "customer_phone_number": {
            "description": "phone number of the customer",
            "values_sample": [],
        },
        "customer_email": {
            "description": "email address of the customer",
            "values_sample": [],
        },
        "customer_order_count_till_date": {
            "description": "total number of fulfilled orders of the customer",
            "values_sample": [],
        },
        "customer_total_spent_till_date": {
            "description": "total amount of money spent by the customer",
            "values_sample": [],
        },
    },
    "transformed_product": {
        "product_id": {"description": "Table id", "values_sample": []},
        "product_listing_date": {
            "description": "Order creation timestamp as per the source",
            "values_sample": [],
        },
        "product_update_date": {
            "description": "Order updation timestamp as per the source",
            "values_sample": [],
        },
        "internal_created_at": {
            "description": "The timestamp of creation of this entry",
            "values_sample": [],
        },
        "internal_updated_at": {
            "description": "The timestamp of updation of this entry",
            "values_sample": [],
        },
        "source_platform": {
            "description": "Data source such as Amazon, shopify",
            "values_sample": [],
        },
        "source_platform_row_id": {
            "description": "The primary key in the source table",
            "values_sample": [],
        },
        "internal_deleted_at": {
            "description": "A flag for deleted row",
            "values_sample": [],
        },
        "product_category": {
            "description": "category of the product",
            "values_sample": [],
        },
        "product_title": {"description": "title of the product", "values_sample": []},
    },
}

# Sample queries for the entire database
# This will be of format: [{'question': <the sample user question>, 'query': <the sql query>, 'description': <description of the query>}, ...]
DATABASE_SAMPLE_QUERIES = []
