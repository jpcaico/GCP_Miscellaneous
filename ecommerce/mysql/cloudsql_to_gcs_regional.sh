bucket_name=ecommerce_endtoend

# CUSTOMER DATASET
gcloud sql export csv ecommerce-instance \
gs://$bucket_name/mysql_export/regional/southeast/customers.csv \
--database=ecommerce \
--offload \
--query='SELECT cust.* FROM customers cust 
JOIN geolocation geo
ON cust.customer_zip_code_prefix = geo.geolocation_zip_code_prefix
WHERE geo.geolocation_state IN ("SP", "MG", "RJ", "ES");'


# GEOLOCATION DATASET
gcloud sql export csv ecommerce-instance \
gs://$bucket_name/mysql_export/regional/southeast/geolocation.csv \
--database=ecommerce \
--offload \
--query='SELECT * FROM geolocation WHERE geolocation_state IN ("SP", "MG", "RJ", "ES");'


# ITEMS DATASET
gcloud sql export csv ecommerce-instance \
gs://$bucket_name/mysql_export/regional/southeast/items.csv \
--database=ecommerce \
--offload \
--query='SELECT itm.* FROM order_items itm 
JOIN orders ord ON ord.order_id = itm.order_id 
JOIN customers cust ON cust.customer_id = ord.customer_id
JOIN geolocation geo ON geo.geolocation_zip_code_prefix = cust.customer_zip_code_prefix
WHERE geo.geolocation_state IN ("SP", "MG", "RJ", "ES");'

# PAYMENTS DATASET
gcloud sql export csv ecommerce-instance \
gs://$bucket_name/mysql_export/regional/southeast/payments.csv \
--database=ecommerce \
--offload \
--query='SELECT pay.* FROM payments pay 
JOIN orders ord ON ord.order_id = pay.order_id
JOIN customers cust ON cust.customer_id = ord.customer_id
JOIN geolocation geo ON cust.customer_zip_code_prefix = geo.geolocation_zip_code_prefix
WHERE geo.geolocation_state IN ("SP", "MG", "RJ", "ES");'

# REVIEWS DATASET
gcloud sql export csv ecommerce-instance \
gs://$bucket_name/mysql_export/regional/southeast/reviews.csv \
--database=ecommerce \
--offload \
--query='SELECT rev.* FROM reviews rev
JOIN orders ord ON ord.order_id = rev.order_id
JOIN customers cust ON cust.customer_id = ord.customer_id
JOIN geolocation geo ON cust.customer_zip_code_prefix = geo.geolocation_zip_code_prefix
WHERE geo.geolocation_state IN ("SP", "MG", "RJ", "ES");'

# ORDERS DATASET
gcloud sql export csv ecommerce-instance \
gs://$bucket_name/mysql_export/regional/southeast/orders.csv \
--database=ecommerce \
--offload \
--query='SELECT ord.* FROM orders ord
JOIN customers cust ON cust.customer_id = ord.customer_id
JOIN geolocation geo ON cust.customer_zip_code_prefix = geo.geolocation_zip_code_prefix
WHERE geo.geolocation_state IN ("SP", "MG", "RJ", "ES");'

# PRODUCTS DATASET
gcloud sql export csv ecommerce-instance \
gs://$bucket_name/mysql_export/regional/southeast/products.csv \
--database=ecommerce \
--offload \
--query='SELECT prod.*, geo.geolocation_state from products prod
JOIN order_items ord_itm ON ord_itm.product_id = prod.product_id
JOIN orders ord ON ord.order_id = ord_itm.order_id
JOIN customers cust ON cust.customer_id = ord.customer_id
JOIN geolocation geo ON cust.customer_zip_code_prefix = geo.geolocation_zip_code_prefix
WHERE geo.geolocation_state IN ("SP", "MG", "RJ", "ES");'

# SELLERS DATASET
gcloud sql export csv ecommerce-instance \
gs://$bucket_name/mysql_export/regional/southeast/sellers.csv \
--database=ecommerce \
--offload \
--query='SELECT sel.* FROM sellers sel 
JOIN geolocation geo ON geo.geolocation_zip_code_prefix = sel.seller_zip_code_prefix
WHERE geo.geolocation_state IN ("SP", "MG", "RJ", "ES");'


