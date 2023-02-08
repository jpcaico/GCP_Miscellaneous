terraform {

required_providers {
  google = {
    source = "hashicorp/google"
    version = "4.27.0"
  }
}

}

provider "google" {
    # Configuration options
    project = "<project_id>"
}

resource "google_compute_instance" "terraform" {
    project = "<project-id>"
    name = "terraform"
    machine_type = "n1-standard-2"
    zone = "us-central1-c"
    boot_disk {
      initialize_params {
        image = "debian-cloud/debian-9"
      }
    }
    network_interface {
      network = "default"
      access_config {
        
      }
    }

}