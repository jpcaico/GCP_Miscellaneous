# Auto Scaling and Load Balancing

Using the Auto Scaling function within GCP allows you to create high
available and fault tolerant infrastructure that is very important to your production
environment.

Creating Managed Templates, Groups and Images are all apart of understanding how
Auto Scaling is very powerful through Terraform

Using Load Balancer will help direct traffic to healthy instances that 
you've created with your terraform config file

This allows you to scale out your resources based on any metric that you provide through terraform
to GCP.
Whether its through Pub/Sub or a Logging Agent, terraform can help you instantly setup the environment.