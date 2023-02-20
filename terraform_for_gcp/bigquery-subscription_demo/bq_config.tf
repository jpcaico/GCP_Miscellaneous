# create the bigquery subscription
resource "google_pubsub_subscription" "subscription_event_demo" {
    project = "your-project-name"
    name = "event_demo_subscription"
    topic = google_pubsub_topic.topic_event_demo.name
    bigquery_config {
    table            = "your-project-name:${google_bigquery_table.table_event_demo.dataset_id}.${google_bigquery_table.table_event_demo.table_id}"
    use_topic_schema = true
  }
  depends_on = [google_project_iam_member.permissions_event_demo]
}