terraform {
    required_version = ">= 1.0.11"
    required_providers {
      google = {
        source = "hashicorp/google"
        version = ">= 4.5.0"
      }
    }

backend "gcs" {
    bucket = "project-bucket"
    prefix = "terraform/network"
}
}

resource "google_compute_network" "vpc" {
    name = "terraform-vpc"
    auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "vpc-subnet" {
    name = "terraform-subnet"
    network = google_compute_network.vpc.name
    region = "us-central1"
    ip_cidr_range = "10.10.0.0/24"
}

output "subnet_name" {
    value = google_compute_subnetwork.vpc-subnet.name
}
