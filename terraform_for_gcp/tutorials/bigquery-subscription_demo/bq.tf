# Creating the dataset

resource "google_bigquery_dataset" "dataset_bigquery_subscription_demo" {
    project = "your-project-name"
    dataset_id = "bigquery_subscription_demo"
    friendly_name = "bigquery subscription demo"
    description = "a demo dataset to show how it works"
}

resource "google_bigquery_table" "table_event_demo" {
    project = "your-project-name"
    dataset_id = google_bigquery_dataset.dataset_bigquery_subscription_demo.dataset_id
    table_id = "demo_event"
    description = "Example table"
    schema = <<EOF
    [
      {"name": "creation_time", "type": "DATETIME", "mode": "REQUIRED"},
      {"name": "event_name", "type": "STRING", "mode": "REQUIRED"}  
    ]
    EOF
}