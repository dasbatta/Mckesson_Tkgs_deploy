#!/usr/bin/env python3

import helper
import interpolate
import pmsg
import os

yaml_source = "config.yaml"
template_file = "templates/workload-cluster-template.yaml"
output_file = "/tmp/tkc_result"
interpolate.interpolate_from_yaml_to_template(yaml_source, template_file, output_file)
workload_cluster = os.environ["workload_cluster"]

# does this workload cluster already exist?
if helper.run_a_command("kubectl get tkc " + workload_cluster) == 0:
    pmsg.green("Workload cluster is RUNNING")
    exit(0)

# Construct the kubectl apply command
pmsg.normal("Creating workload cluster...")
cmd = ['kubectl', 'apply', '-f', output_file]
if helper.check_for_result(cmd,"tanzukubernetescluster.* created") :
    if helper.check_for_result_for_a_time(["kubectl","get","tkc",workload_cluster,"-o","jsonpath='{.status.phase}'"],"running", 60, 50):
        pmsg.green("Workload cluster is RUNNING")   
    else: 
        pmsg.fail("Failed to create cluster in time, check logs for more details")
        exit(1)
else:
    pmsg.fail ("Failed to apply the Cluster Create YAML")
    exit(1)
exit(0)
