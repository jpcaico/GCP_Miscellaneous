provider "google" {
    credentials = "<NAME>.json"
    project = "<PROJECT_ID>"
    region = "<region>"
    zone = "<zone>"
}

# SET UP BACKEND STATE STORAGING
terraform {
  backend "gcs" {
    bucket = "bucket-name"
    prefix = "folder-name"
    credentials = "credentials.json"
  }
}



#SET UP RESOURCES
# VPC
resource  "google_compute_network" "vpc_network" {
    name = "terraform-network"
}

# COMPUTE ENGINE INSTANCE
resource "google_compute_instance" "vm_instance" {
    name = "terraform-instance"
    machine_type = "f1-micro"

    boot_disk {
      initialize_params {
        image = "debian-cloud/debian-11"
      }
    }

    network_interface {
      network = google_compute_network.vpc_network.name
      access_config {
        
      }
    }
}

# STATIC IP
resource "google_compute_address" "vm_static_ip" {
    name = "terraform-static-ip"
}