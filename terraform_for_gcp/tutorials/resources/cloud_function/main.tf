
# Create a bucket
# Upload a file
# Deploy function
# policy binding

# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloudfunctions_function

# Create a bucket
resource "google_storage_bucket" "example_bucket" {
    name = "example_bucket_tf"
    location = var.region
}
# Upload a file
resource "google_storage_bucket_object" "source_code" {
    name = "index.zip"
    bucket = google_storage_bucket.example_bucket.name
    source = "index.zip"
}
# Deploy function
resource "google_cloudfunctions_function" "function_from_tf" {
    name = "function-from-tf"
    runtime = "nodejs14"
    description = "Function from terraform script"

    available_memory_mb = 128
    source_archive_bucket = google_storage_bucket.example_bucket.name
    source_archive_object = google_storage_bucket_object.source_code.name

    trigger_http = true
    entry_point = "helloWorldtf"
}
# policy binding
resource "google_cloudfunctions_function_iam_member" "allowaccess" {
    region = google_cloudfunctions_function.function_from_tf.region
    cloud_function = google_cloudfunctions_function.function_from_tf.name

    role = "roles/cloudfunctions.invoker"
    member = "allUsers"
}