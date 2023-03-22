#!/usr/bin/env python3
import os
import helper
import re
import subprocess
import pmsg

os.environ["KUBECTL_VSPHERE_PASSWORD"] = os.environ["vsphere_password"]
supervisor_cluster = os.environ["supervisor_cluster"]
vsphere_username = os.environ["vsphere_username"]
vsphere_namespace = os.environ["vsphere_namespace"]
workload_cluster = os.environ["workload_cluster"]

# Login to the k8s workload cluster
command = "kubectl vsphere login --server " + supervisor_cluster + " --vsphere-username " + vsphere_username + " --insecure-skip-tls-verify --tanzu-kubernetes-cluster-namespace " + vsphere_namespace + " --tanzu-kubernetes-cluster-name " + workload_cluster
rc = helper.run_a_command(command)

if rc == 0:
    # Connect to the context
    command = "kubectl config use-context " + workload_cluster
    rc = helper.run_a_command(command)

    if rc == 0:
        # Verify that I'm logged in...
        process = subprocess.Popen(["kubectl", "config", "get-contexts"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = process.communicate()
        contexts = output.splitlines()
        rc = 1
        for context in contexts:
            if re.search("\\*\\s+"+workload_cluster+"\\s", context.decode('utf-8')) is not None:
                rc = 0
                pmsg.green("k8s cluster login OK.")
                break

exit(rc)
