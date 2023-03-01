### CREATE BUCKET ###
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket

resource "google_storage_bucket" "GCS-Bucket1" {
#bucket-name
name = "unique-bucket-name-jp-test"
#storage class
storage_class = "STANDARD"
#location
location = "US-CENTRAL1"
#labels
labels = {
  "env" = "tf_env"
  "dep" = "department"
}

# access control
uniform_bucket_level_access = true

#lifecycle rule
lifecycle_rule {
  condition {
    age = 5
  }
  action {
    type = "SetStorageClass"
    storage_class = "COLDLINE"
  }

}

 # retention policy
 retention_policy {
   is_locked = true
   retention_period = 864000
 }
}

### UPLOAD OBJECT ###
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket_object
resource "google_storage_bucket_object" "file" {

name = "text_file"
#reference created bucket (resource_type.resource_name.name)
bucket = google_storage_bucket.GCS-Bucket1.name 
source = "upload_text_file.txt"

}