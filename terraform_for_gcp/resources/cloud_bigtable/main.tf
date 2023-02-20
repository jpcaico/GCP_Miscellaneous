# CREATE INSTANCE
#https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigtable_instance
resource "google_bigtable_instance" "bt-from-tf" {
  
  name = "bt-from-tf"
  deletion_protection = false
  labels = {
    "env" = "testing"
  }
  cluster {
    cluster_id = "bt-from-tf-1"
    num_nodes = 1
    storage_type = "SSD"
  }

}



# CREATE TABLE
#https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigtable_table

resource "google_bigtable_table" "tb1" {
  name = "tb-from-tf"
  instance_name = google_bigtable_instance.bt-from-tf.name

  split_keys    = ["a", "b", "c"]

  lifecycle {
    prevent_destroy = true
  }

  column_family {
    family = "family-first"
  }

  column_family {
    family = "family-second"
  }
  
}