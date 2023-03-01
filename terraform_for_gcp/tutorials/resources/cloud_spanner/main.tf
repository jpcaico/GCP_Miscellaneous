# CREATE SPANNER INSTANCE #
#https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/spanner_instance

resource "google_spanner_instance" "spanner_tf" {
  name = "spannertf"
  config = "regional-us-east1"
  display_name = "Spanner from TF"
  num_nodes = 1
  # processing_units    = 200
  labels = {
    "env" = "instance_through_tf"
  }
  
}

# CREATE SPANNER DATABASE #
resource "google_spanner_database" "database"{
    name = "db_spanner"
    instance =  google_spanner_instance.spanner_tf.name
    # version_retention_period = "3d"
    ddl = [
    "CREATE TABLE t1 (t1 INT64 NOT NULL,) PRIMARY KEY(t1)",
    "CREATE TABLE t2 (t2 INT64 NOT NULL,) PRIMARY KEY(t2)",
    ]
    deletion_protection = false
}