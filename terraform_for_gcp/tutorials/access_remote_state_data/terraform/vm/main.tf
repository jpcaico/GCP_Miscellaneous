terraform {
    required_version = ">= 1.0.11"
    required_providers {
      google = {
        source = "hashicorp/google"
        version = ">= 4.5.0"
      }
    }

backend "gcs" {
    bucket = "project-bucket" # bucket already created
    prefix = "terraform/vm"
}
}


data "terraform_remote_state" "network" {
    backend = "gcs"
    config = {
        bucket = "project-bucket" #same bucket as the one created in network
        prefix = "terraform/network" #match exactly on the terraform config file
    }
}

resource "google_compute_instance" "vm" {
    name = "terraform-vm"
    machine_type = "f1-micro"
    zone = "us-central1-a"
    boot_disk {
      initialize_params{
        image = "debian-cloud/debian-11"
      }
    }
    network_interface {
      subnetwork = data.terraform_remote_state.network.outputs.subnet_name
    }
}