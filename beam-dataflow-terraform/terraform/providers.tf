# SET UP GOOGLE PROVIDER
provider "google" {
    # Configuration options
    project = var.project
    credentials = "/Users/jalvi/Downloads/beam-dataflow-376917-a23968b32b0a.json"
}

# SET UP BACKEND STATE STORAGING
# terraform {
#   backend "gcs" {
#     bucket = "terraform-project-backend"
#     prefix = "terraform"
#     credentials = "/Users/jalvi/Downloads/beam-dataflow-376917-a23968b32b0a.json"
#   }
# }