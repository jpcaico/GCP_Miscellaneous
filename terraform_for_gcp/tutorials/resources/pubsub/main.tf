#https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/pubsub_topic


# DEFINE SCHEMA [OPTIONAL]
resource "google_pubsub_schema" "schema_def" {
  name = "schema_def"
  type = "AVRO"
  definition = "{\n  \"type\" : \"record\",\n  \"name\" : \"Avro\",\n  \"fields\" : [\n    {\n      \"name\" : \"StringField\",\n      \"type\" : \"string\"\n    },\n    {\n      \"name\" : \"IntField\",\n      \"type\" : \"int\"\n    }\n  ]\n}\n"
}

# DEFINE TOPIC DEPENDENT ON SCHEMA
resource "google_pubsub_topic" "topic_tf" {
  name = "topic-tf"

  labels = {
    foo = "bar"
  }

  message_retention_duration = "86600s"

# schema dependency

#   depends_on = [google_pubsub_schema.schema_def]
#   schema_settings {
#     schema = "projects/my-project-name/schemas/example"
#     encoding = "JSON"
#   }


}


# DEFINE SUBSCRIPTION #
#https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/pubsub_subscription

resource "google_pubsub_subscription" "sub_tf" {
  name = "sub_tf"
  topic = google_pubsub_topic.topic_tf.name
}