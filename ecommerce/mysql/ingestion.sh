#!/bin/bash


# Declare the table_files dictionary
declare -A table_files=(
  ["customers"]="olist_customers_dataset.csv"
  ["geolocation"]="olist_geolocation_dataset.csv"
  ["order_items"]="olist_order_items_dataset.csv"
  ["orders"]="olist_orders_dataset.csv"
  ["payments"]="olist_order_payments_dataset.csv"
  ["products"]="olist_products_dataset.csv"
  ["sellers"]="olist_sellers_dataset.csv"
  ["reviews"]="olist_order_reviews_dataset.csv"
)

# Set the bucket name and Cloud SQL instance name
BUCKET_NAME="ecommerce_endtoend"
INSTANCE_NAME="ecommerce-instance"

# Loop through each table and import its corresponding file
for table in "${!table_files[@]}"
do
    file=${table_files[$table]}
    echo "Importing $file into $table..."
    gcloud sql import csv $INSTANCE_NAME gs://$BUCKET_NAME/raw/$file --database=ecommerce --table=$table
done
