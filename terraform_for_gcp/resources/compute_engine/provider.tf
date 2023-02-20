# SET UP GOOGLE PROVIDER
provider "google" {
    # Configuration options
    project = var.project
    region = var.region
    zone = var.zone
    credentials = "/Users/jalvi/Downloads/terraform.json"
}

# SET UP BACKEND STATE STORAGING
terraform {
  backend "gcs" {
    bucket = "terraformstatetest1"
    prefix = "terraform1"
    credentials = "/Users/jalvi/Downloads/terraform.json"
  }
}