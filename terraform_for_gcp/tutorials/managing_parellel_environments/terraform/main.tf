terraform {
    required_version = ">= 1.0.11"
    required_providers {
      google = {
        source = "hashicorp/google"
        version = ">= 4.5.0"
      }
    }
    backend "gcs" {
      bucket = ""
      prefix = "terraform/app"
    }
}

module "web_app" {
    source = "./modules/app"
}

output "ip" {
    value = module.web_app.web_server_ip
}