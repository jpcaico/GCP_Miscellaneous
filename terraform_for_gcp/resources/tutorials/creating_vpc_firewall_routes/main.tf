# CREATING NETWORK

module "network" {
    source = "terraform-google-modules/network/google"
    version = "1.1.0"
    network_name = "my-vpc-network"
    project_id = var.project

    subnets = [
{
        subnet_name = "subnet_01"
        subnet_ip = var.cidr
        subnet_region = var.region
},
# private subnet
 {
     subnet_name = "subnet_02",
     subnet_ip = "10.1.0.0/16",
     subnet_region = var.region
     google_private_access = true

}
    ]

secondary_ranges = {
    subnet_01 = [ ]
}

}

# ROUTES CONFIGURATION

module "network_routes" {
    # https://registry.terraform.io/modules/terraform-google-modules/network/google/latest/submodules/routes
    source = "terraform-google-modules/network/google/modules/routes"
    version = "2.1.1"
    network_name = module.network.network_name
    project_id = var.project

    routes = [
        {

            name = "egress-internet"
            description = "route through IGW to access internet"
            destination_range = "0.0.0.0/0"
            tags = "egress_inet"
            next_hop_internet = true
        
        },

    ]


}


# CREATING FIREWALL RULES
# https://registry.terraform.io/modules/terraform-google-modules/network/google/3.3.0/submodules/fabric-net-firewall

module "network_fabric-net-firewall" {
    source  = "terraform-google-modules/network/google//modules/fabric-net-firewall"
    project_id = var.project
    network = module.network.network_name
    internal_ranges_enabled = true
    internal_ranges = ["10.0.0/16"]
}