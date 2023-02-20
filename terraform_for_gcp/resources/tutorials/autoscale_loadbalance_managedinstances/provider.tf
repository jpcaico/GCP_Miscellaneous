# SET UP GOOGLE PROVIDER
provider "google" {
    # Configuration options
    project = var.project
    region = var.region
    zone = var.zone
    credentials = "/Users/jalvi/Downloads/terraform.json"
}