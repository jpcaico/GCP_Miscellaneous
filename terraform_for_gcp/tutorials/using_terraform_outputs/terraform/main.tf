
#This Terraform code defines a variable vm_names as a list of strings with default values of ["front-end", "back-end"].
# It then declares a module called vm, with a source path of ./modules/vm, which will be instantiated for each value in the vm_names list
# using the count parameter.

#The vm-name parameter of the module is set to var.vm_names[count.index],
# which means that each instance of the module will use the corresponding value from the vm_names list as its name.
# The count parameter is set to length(var.vm_names), which means that the module will be instantiated twice - once for each element 
#in the vm_names list.

#Overall, this Terraform code sets up a module to create two virtual machines with the names "front-end" and "back-end",
# respectively, using the configuration defined in the ./modules/vm directory.

terraform {
  required_version = ">= 1.0.11"
  required_providers {
    google = {
        source = "hashicorp/google"
        version =  ">= 4.5.0"
    }
    local = {
        source = "hashicorp/local"
        version = "> 2.1.0"
    }
  }
}

#list of names for our vms



variable "vm_names" {
    type = list(string)
    default = ["front-end", "back-end", "database"]
}

module "vm" {
    source = "./modules/vm"
    vm-name = var.vm_names[count.index]
    count = length(var.vm_names)
}


resource "local_file" "IPs" {
    filename = "./inventor.csv"
    content = templatefile("manifest.tftpl", {ip_addrs = module.vm.*.ip})
}