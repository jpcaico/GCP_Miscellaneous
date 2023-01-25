#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sqlalchemy import create_engine
from google.oauth2 import service_account
from google.cloud import bigquery


# In[2]:


df = pd.read_parquet('green_tripdata_2022-01.parquet', columns = ['VendorID','store_and_fwd_flag','RatecodeID','PULocationID','DOLocationID'])


# In[5]:


engine = create_engine('postgresql://root:root@localhost:5432/bq_data')


# In[6]:


engine.connect()


# In[7]:


df.to_sql(con=engine, name='green_taxi_data', if_exists='replace')


# In[9]:


# Set the path to your service account key
path_to_key = "/path/to/serviceKey.json"

# Set the dataset and table names
project_id = 'bcs-field-solutions-sbx'
dataset_id = "bq_dataset"
table_id = 'green_taxi'


# In[10]:


# Build the credentials object
creds = service_account.Credentials.from_service_account_file(path_to_key)


# In[11]:


# Initialize a BigQuery client
client = bigquery.Client(credentials=creds, project=project_id)


# In[12]:


# Lets create a simple query
query = "SELECT * FROM green_taxi_data;"


# In[13]:


dtypes = {
    'FLOAT': float,
    'STRING': str,
    'INTEGER': int,
    'BOOLEAN': bool,
    'BYTES': bytes,
    'TIMESTAMP': str
}


# In[14]:


# loading data from postgresl in chunks
#let's add some noise to the data. If the chunk number is even number, we will convert some columns
# just to have different data types for each chunk
# and then load append each chunk to bigquery


chunksize = 1000
index = 1

# we first check if there's already a schema there (a table created)
try:
    table_schema = client.get_table(f'{dataset_id}.{table_id}')
    # getting table schema
    existing_schema = table_schema.schema
    print(f"Schema for {table_id} captured from BigQuery...")
    print(existing_schema)

except: 

    print(f"This is the first batch for table {table_id}, schema will be auto-infered ...")
    existing_schema = None
        
        
for chunk in pd.read_sql(query, engine, chunksize=chunksize):
    print(f'Running chunk {index}...')
    if index % 2 == 0:
        # Convert the values in store_and_fwd_flag to an integer
        chunk['store_and_fwd_flag'] = 1
    
    #Now we start playing with the schema
    
    # if this is the first chunk (table not created in BigQuery)
    if existing_schema == None:
        print(f"Schema is  None, This is the first chunk")
        print(f'Loading data to bigquery for table {table_id}')
        
        #loading the first chunk
        chunk.to_gbq(project_id=project_id,
                                destination_table=f'{dataset_id}.{table_id}',
                                credentials=creds,
                                if_exists='append')
        print(chunk.dtypes)
        
        print(f'Chunk {index} loaded successfully')
        
        #Now we capture the schema generated
        print(f"Fetching schema from {table_id} ")
        new_table_schema = client.get_table(f'{dataset_id}.{table_id}')
        # we replace existing_schema to the schema from the first chunk
        existing_schema = new_table_schema.schema
        print(f"Schema for {table_id} captured from BigQuery...")
        print(existing_schema)
     
    # if there is already a chunk loaded, it will enter this condition
    else: 
        print(f"Schema is not None, there's already a chunck loaded")

        # Now we convert the chunk column types to match the dictionary
        for col_type in existing_schema:
            chunk[col_type.name] = chunk[col_type.name].astype(dtypes[col_type.field_type])
        
        print(chunk.dtypes)
        print(f"Loading {table_id} to BigQuery...")
        #loading the next chunka
        chunk.to_gbq(project_id=project_id,
                                destination_table=f'{dataset_id}.{table_id}',
                                credentials=creds,
                                if_exists='append')
        
        
    index +=1
    


# In[ ]:




