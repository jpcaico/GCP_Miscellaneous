## COMPUTE NETWORK ##

#https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_network

resource "google_compute_network" "auto-vpc-tf" {
    name = "auto-vpc-tf"
    auto_create_subnetworks = true

}

resource "google_compute_network" "custom-vpc-tf" {
    name = "custom-vpc-tf"
    auto_create_subnetworks = false

}

### SUBNET CREATION ###
#https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_subnetwork

resource "google_compute_subnetwork" "sub-sg" {
    name = "sub-sg"
    network = google_compute_network.custom-vpc-tf.id  #referencing network resource id
    ip_cidr_range = "10.1.0.0/24"
    region = var.region #referencing variables file
    private_ip_google_access = true

}

## CREATE FIREWALL RULE ##

resource "google_compute_firewall" "allow-icmp" {
    name = "allow-icmp"
    network = google_compute_network.custom-vpc-tf.id
    allow {
        protocol = "icmp"
    }
    source_ranges = ["49.36.82.10/32"]
    priority = 455
}
