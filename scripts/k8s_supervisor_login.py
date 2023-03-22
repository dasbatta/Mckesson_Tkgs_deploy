#!/usr/bin/env python3
import os
import helper
import re
import subprocess
import pmsg

supervisor_cluster = os.environ["supervisor_cluster"]
vsphere_username = os.environ["vsphere_username"]
vsphere_namespace = os.environ["vsphere_namespace"]
os.environ["KUBECTL_VSPHERE_PASSWORD"] = os.environ["vsphere_password"]

# Login to the k8s workload cluster
command = "kubectl vsphere login --server " + supervisor_cluster + " --vsphere-username " + vsphere_username + " --insecure-skip-tls-verify"

rc = 1
if helper.run_a_command(command) == 0:
    # Connect to the context
    command = "kubectl config use-context " + vsphere_namespace

    if helper.run_a_command(command) == 0:
        # Verify that I'm logged in...
        process = subprocess.Popen(["kubectl", "config", "get-contexts"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = process.communicate()
        contexts = output.splitlines()
        for context in contexts:
            if re.search("\\*\\s+"+vsphere_namespace+"\\s", context.decode('utf-8')) is not None:
                rc = 0
                pmsg.green("k8s supervisor cluster login OK.")
                break

exit(rc)
