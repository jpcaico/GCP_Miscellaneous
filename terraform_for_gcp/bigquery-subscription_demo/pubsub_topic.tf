# Create the pubsub topic. It contains an AVRO schema applied and the schema should confirm to the BigQuery table.

resource "google_pubsub_schema" "schema_event_demo" {
    project = "your-project-name"
    name = "event_demo_schema"
    type = "AVRO"
    definition = <<EOF
{
"type" : "record",
"name" : "event_demo",
"fields" : [
{
"name" : "creation_time",
"type" : "string"
},
{
"name" : "event_name",
"type" : "string"
}
]
}
EOF
}

resource "google_pubsub_topic" "topic_event_demo" {

project = "your-project-name"
name = "demo_event_topic"
depends_on = [
  google_pubsub_schema.schema_event_demo
]
schema_settings {
  schema = "projects/your-project-name/schemas/${google_pubsub_schema.schema_event_demo.name}"
  encoding = "JSON"
}

}

# give the pubsub engine permission to see the bigquery table and insert data

resource "google_project_iam_member" "permission_event_demo" {
    
for_each = toset(["roles/bigquery.dataEditor", "roles/bigquery.metadataViewer"])
  project  = "your-project-name"
  role     = each.value
  member   = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-pubsub.iam.gserviceaccount.com"

}
