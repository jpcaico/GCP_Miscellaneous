# add the terraform block
terraform {
    required_version = ">= 1.0.11"
    required_providers {
      google = {
        source = "hashicorp/google"
        version = ">= 4.5.0"
      }
    }
}

module "cloud-run" {
  source  = "GoogleCloudPlatform/cloud-run/google"
  version = "0.4.0"
  # insert the 4 required variables here

  service_name = "my-app"
  project_id = "using-terraf-263-952c3e06"
  location = "us-central1"
  image = "gcr.io/cloudrun/Hello"
  members = ["allUsers"] #make myapp servers public available, no need to authenticate  
}

output "url" {
    value = module.cloud-run.service_url
}



