terraform {
    required_version = ">= 1.0.11"
    required_providers {
      google = {
        source = "hashicorp/google"
        version = ">= 4.5.0"
      }
    }
}

#1st part
# resource "google_project_iam_custom_role" "custom-role" {
#     role_id = "ComputeAudit"
#     title = "Compute Audit Role"
#     description = "A role for compute auditors"
#     permissions = split("\n", file("./compute_audit.txt"))
# }


resource "google_project_iam_custom_role" "custom-role" {
    for_each = fileset(path.module.txt, "*.txt")
    role_id = split(".", each.value)[0]
    title = split(".", each.value)[0]
    description = "A role containing permissions from ${each.value}"
    permissions = split("\n", file(each.value))
}
