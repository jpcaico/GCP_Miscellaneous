import mysql.connector
from google.oauth2 import service_account
from google.cloud import storage

# GCS credentials
# credentials = service_account.Credentials.from_service_account_file('/path/to/credentials.json')

# GCS file details
bucket_name = 'ecommerce_e2e'  # 'your-bucket-name'
gcs_dir = "raw"
# Cloud SQL credentials
conn = mysql.connector.connect(
    host='35.202.201.99', # 'your-db-host, Public IP address'
    database='ecommerce',
    user="root'@'%",
    password='root'
)

print("Connection Successfull")

# CREATE CURSOR
cur = conn.cursor()

# GCS bucket and file handling
storage_client = storage.Client()
# credentials=credentials)
bucket = storage_client.get_bucket(bucket_name)

# define a dictionary mapping table names to file names
table_files = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv"
}
for table, filename in table_files.items():
    blob = bucket.blob(filename)

    # Download the file to a local temporary file
    temp_file_name = '/tmp/temp_file.csv'
    blob.download_to_filename(temp_file_name)

    # Execute the LOAD DATA INFILE command to load the data into the table
    with conn.cursor() as cursor:
        # build the LOAD DATA INFILE statement and execute it
        load_sql = f"LOAD DATA INFILE '{temp_file_name}' INTO TABLE {table} FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\\n' IGNORE 1 ROWS"
        cur.execute(load_sql)
        conn.commit()

# close the database connection
cur.close()
conn.close()