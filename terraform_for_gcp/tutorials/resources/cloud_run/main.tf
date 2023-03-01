# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloud_run_service

resource "google_cloud_run_service" "run-app-from-tf" {
    name = "run-app-from-tf"
    location = var.region


template {
    spec {
        containers {
            # revision 1
            #image = "gcr.io/google-samples/hello-app:1.0"
            # revision 2
            image = "gcr.io/google-samples/hello-app:2.0"
        }
    }
}

## SPLITTING TRAFFIC BETWEEN REVISIONS ##
# traffic {
#     revision_name = "run-app-from-tf-revision1"
#     percent = 50
# }

# traffic {
#     revision_name = "run-app-from-tf-revision2"
#     percent = 50
# }
}

### ALLOWING ACCESS PERMISSION to allUsers ###

# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloud_run_service_iam
resource "google_cloud_run_service_iam_policy" "pub_access" {
    service = google_cloud_run_service.run-app-from-tf.name
    location = google_cloud_run_service.run-app-from-tf.location
    policy_data = data.google_iam_policy.public_access-1.policy_data
}

### CREATE POLICY TO ATTACH TO IAM POLICY ABOVE ###
data "google_iam_policy" "public_access-1" {
    binding {
      role = "roles/run.invoker"
      members = ["allUsers"]
    }
}