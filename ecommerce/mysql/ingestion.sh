#!/bin/bash


# Declare the table_files dictionary
declare -A countries=( [ALB]=Albania [BHR]=Bahrain [CMR]=Cameroon [DNK]=Denmark [EGY]=Egypt )

# Set the bucket name and Cloud SQL instance name
BUCKET_NAME="ecommerce_e2e"
INSTANCE_NAME="ecommerce-instance"

for key in "${!countries[@]}"; do echo $key; done
# Loop through each table and import its corresponding file
# for table in "${!table_files[@]}"
# do
#     file=${table_files[$table]}
#     echo "Importing $file into $table..."
#     gcloud sql import csv $INSTANCE_NAME gs://$BUCKET_NAME/raw/$file --database=ecommerce --table=$table
# done
