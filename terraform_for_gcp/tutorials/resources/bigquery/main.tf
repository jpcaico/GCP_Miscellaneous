# CREATE DATASET
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset_tf" {
  dataset_id = "dataset_tf"
  default_table_expiration_ms = 3600000
}

# CREATE TABLE
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table
resource "google_bigquery_table" "table_tf" {
  table_id = "table_from_tf"
  dataset_id = google_bigquery_dataset.dataset_tf.dataset_id

    time_partitioning {
    type = "DAY"
  }

  labels = {
    env = "default"
  }

  schema = <<EOF
[
  {
    "name": "permalink",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "The Permalink"
  },
  {
    "name": "state",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "State where the head office is located"
  }
]
EOF

}