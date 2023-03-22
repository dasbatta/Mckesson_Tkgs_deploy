# Terraform Details
Terraform is being used to check/create objects in vSphere per a configuration file and, for some objects, object names and attributes may be hard-coded into terraform .tf files where those attributes will not vary between distribution centers (for the McKesson work).

The following files are used:

- main.tf - This file contains checks for roles and also privileges on given objects
- <add more here as created during development>

## Running terraform
Run using the parent folder python function: run_pipeline.py --config_file config.yaml

This run_pipeline script will run terraform for you. The steps it follows are equivalent to:

1. Run this to generate the state file: $ terraform init
2. Run this to create the plan: $ terraform plan -var-file=variables.tfvars -out myplan.tfplan or: $ terraform plan -var="vcenter_folder=sample_folder"
3. Run this to run the plan and check/create the user: $ terraform apply myplan.tfplan
