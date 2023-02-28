## Network Template

module "network" {
    source = "terraform-google-modules/network/google"
    version = "1.1.0"
    network_name = "my-vpc-network"
    project_id = var.project #references variable file

    subnets = [
        {
            subnet_name = "subnet-01"
            subnet_ip = var.cidr
            subnet_region = var.region

        },
    ]

    secondary_ranges = {
        subnet-01 = []
    }
}

### Module template for VPC Rules for Firewall

module "network_fabric-net-firewall" {

  source  = "terraform-google-modules/network/google//modules/fabric-net-firewall"
  version = "1.1.0"
    project_id          = var.project #references variables.tf
    network             = module.network.network_name #references network module
    internal_ranges_enabled = true
    internal_ranges = var.cidr #references variables.tf
}