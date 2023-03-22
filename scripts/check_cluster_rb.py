#!/usr/bin/env python3

# Checks to see if a psp is installed in the cluster.
# If not, installs it.
# Assumes that the command 'kubectl' is available.
# Assumes we are logged-in to the cluster and the context is already set.

import helper
import pmsg

cluster_role_binding = "auth-users"

# Check/Create:
# create clusterrolebinding cluster_role_binding --clusterrole=psp:vmware-system-privileged --group=system:authenticated

# Is the clusterrolebinding there?
if not helper.check_for_result(["kubectl", "get", "clusterrolebinding", cluster_role_binding], cluster_role_binding+".*ClusterRole"):
    # Create the cluster role binding...
    if helper.run_a_command("kubectl create clusterrolebinding " + cluster_role_binding + " --clusterrole=psp:vmware-system-privileged --group=system:authenticated") == 0:
        # Check it
        if helper.check_for_result(["kubectl", "get", "psp", cluster_role_binding], cluster_role_binding+".*ClusterRole"):
            pass
    else:
        pmsg.fail("Failed to create clusterrolebinding... Recommend running by hand.")
        exit(1)

pmsg.green("Cluster Role Binding OK.")
exit(0)
