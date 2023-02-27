from google.cloud.sql.connector import Connector
from google.cloud import storage
import sqlalchemy
from sqlalchemy import text

import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/jpalvim/Desktop/keys/ecommerce-e2e.json"

project_id = 'ecommerce-e2e-378902'
region = 'us-central1'
instance_name = 'ecommerce-instance'


# GCS file details
bucket_name = 'ecommerce_endtoend'  # 'your-bucket-name'
gcs_dir = "raw"

# GCS bucket and file handling
storage_client = storage.Client()
# credentials=credentials)
bucket = storage_client.get_bucket(bucket_name)

print("Bucket name: {}".format(bucket.name))
print("Bucket location: {}".format(bucket.location))
print("Bucket storage class: {}".format(bucket.storage_class))

INSTANCE_CONNECTION_NAME = f"{project_id}:{region}:{instance_name}" 
print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")
DB_USER = "root"
DB_PASS = "root"
DB_NAME = "ecommerce"

# initialize Connector object
connector = Connector()

# function to return the database connection object
def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    return conn

# create connection pool with 'creator' argument to our connection object function
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)


# define a dictionary mapping table names to file names
table_files = {
    "customers": "raw/olist_customers_dataset.csv",
    "geolocation": "raw/olist_geolocation_dataset.csv",
    "order_items": "raw/olist_order_items_dataset.csv",
    "orders": "raw/olist_orders_dataset.csv",
    "payments": "raw/olist_order_payments_dataset.csv",
    "products": "raw/olist_products_dataset.csv",
    "sellers": "raw/olist_sellers_dataset.csv",
    "reviews": "raw/olist_order_reviews_dataset.csv"
}

for table, filename in table_files.items():

    blob = bucket.get_blob(filename)
    print(f"Working on table {table}..")
    # Download the file to a local temporary file
    temp_file_name = '/home/jpalvim/Desktop/github/GCP_Miscellaneous/ecommerce/mysql/data/temp_file.csv'
    blob.download_to_filename(temp_file_name)
    print(f"Downloaded {table} to temporary file..")
    # Execute the LOAD DATA INFILE command to load the data into the table
    # connect to connection pool
    with pool.connect() as db_conn:
        # build the LOAD DATA INFILE statement and execute it
        load_sql = f"LOAD DATA LOCAL INFILE '{temp_file_name}' INTO TABLE {table} FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\\n' IGNORE 1 ROWS"
        print(load_sql)
        db_conn.execute(text(load_sql))

        print(f"Data loaded for table {table}")
 

# # close the database connection
connector.close()