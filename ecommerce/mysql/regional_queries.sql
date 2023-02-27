# CUSTOMER DATASET

SELECT cust.* FROM CUSTOMERS cust
LEFT JOIN GEOLOCATION geo
ON cust.customer_zip_code_prefix = geo.zip_code_prefix
WHERE geo.geolocation_state IN ("SP", "MG", "RJ", "ES");

# GEOLOCATION DATASET

SELECT * FROM GEOLOCATION WHERE geolocation_state IN ("SP", "MG", "RJ", "ES");

# ITEMS DATASET

SELECT itm.* FROM ITEMS itm 
LEFT JOIN ORDERS ord ON ord.order_id = itm.order_id 
LEFT JOIN CUSTOMER cust ON cust.customer_id = ord.customer_id
LEFT JOIN GEOLOCATION geo ON geo.zip_code_prefix = cust.customer_zip_code_prefix
WHERE geo.geolocation_state IN ("SP", "MG", "RJ", "ES");

# PAYMENTS DATASET

SELECT pay.* FROM PAYMENTS pay 
LEFT JOIN ORDERS ord ON ord.order_id = pay.order_id
LEFT JOIN CUSTOMERS cust ON cust.customer_id = ord.customer_id
LEFT JOIN GEOLOCATION geo ON cust.customer_zip_code_prefix = geo.zip_code_prefix
WHERE geo.geolocation_state IN ("SP", "MG", "RJ", "ES");

# REVIEWS DATASET

SELECT rev.* FROM REVIEWS rev
LEFT JOIN ORDERS ord ON ord.order_id = rev.order_id
LEFT JOIN CUSTOMERS cust ON cust.customer_id = ord.customer_id
LEFT JOIN GEOLOCATION geo ON cust.customer_zip_code_prefix = geo.zip_code_prefix
WHERE geo.geolocation_state IN ("SP", "MG", "RJ", "ES");

# ORDERS DATASET

SELECT ord.* FROM ORDERS ord
LEFT JOIN CUSTOMERS cust ON cust.customer_id = ord.customer_id
LEFT JOIN GEOLOCATION geo ON cust.customer_zip_code_prefix = geo.zip_code_prefix
WHERE geo.geolocation_state IN ("SP", "MG", "RJ", "ES");

# PRODUCTS DATASET

SELECT prod.* from PRODUCTS prod
LEFT JOIN ORDER_ITEMS ord_itm ON ord_itm.product_id = prod.product_id
LEFT JOIN ORDERS ord ON ords.order_id = ord_itm.order_id
LEFT JOIN CUSTOMERS cust ON cust.customer_id = ord.customer_id
LEFT JOIN GEOLOCATION geo ON cust.customer_zip_code_prefix = geo.zip_code_prefix
WHERE geo.geolocation_state IN ("SP", "MG", "RJ", "ES");

# SELLERS DATASET

SELECT sel.* FROM SELLERS sel 
LEFT JOIN GEOLOCATION geo ON geo.zip_code_prefix = sel.seller_zip_code_prefix
WHERE geo.geolocation_state IN ("SP", "MG", "RJ", "ES");
