# CREATING BUCKET FOR TEMP STORAGE (DATAFLOW)
resource "google_storage_bucket" "bucket" {
    name = var.data_flow_bucket
    location = var.location
    force_destroy = true
}

# CREATING TOPIC
 resource "google_pubsub_topic" "log-topic" {
    name = "log-topic"
 }

# CREATING SUBSCRIPTION
resource "google_pubsub_subscription" "log-topic-sub" {
    name = "log-topic-sub"
    topic = google_pubsub_topic.log-topic.name
}

# CREATING BIGQUERY THAT WILL GET THE MESSAGE
resource "google_bigquery_dataset" "logs_dataset" {
  dataset_id = "logs_dataset"
  description = "dataset to store tables related to log data"
  location = var.location
}

resource "google_bigquery_table" "logs_data_streaming_summary" {
    dataset_id = google_bigquery_dataset.logs_dataset.dataset_id
    table_id = "logs_data_streaming_summary"
    depends_on = [
      google_bigquery_dataset.logs_dataset
    ]
    schema = file("bq_logs_summary_schema.json")
    deletion_protection = false

}

# CREATING THE DATAFLOW JOB

resource "google_dataflow_job" "dataflow_job" {
    name = "dataflow_pubsub_bigquery"
    region = var.region
    template_gcs_path = "gs://beam-dataflow-jpcaico-templates/template/streaming_job"
    temp_gcs_location = "gs://${var.data_flow_bucket}/temp"
    enable_streaming_engine = true

    parameters = {
        inputSubscription= google_pubsub_subscription.log-topic-sub.id
        outputTableSpec= "${var.project}:${google_bigquery_dataset.logs_dataset.dataset_id}.${google_bigquery_table.logs_data_streaming_summary.table_id}"
    }
    
    depends_on = [google_bigquery_table.logs_data_streaming_summary,  google_pubsub_subscription.log-topic-sub, google_pubsub_topic.log-topic]
}