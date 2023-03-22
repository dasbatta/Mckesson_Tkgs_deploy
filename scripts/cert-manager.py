#!/usr/bin/env python3

# Checks to see if cert-manager is installed and running.
# If not, installs it.
# Assumes the package is in the cluster already.
# Assumes that the commands 'tanzu' and 'kubectl' are available.
# Assumes we are logged-in to the cluster and the context is already set.

# Assumes there is a default storage class.

import helper
import pmsg
import re
import os

package_namespace = os.environ["installed_packages_namespace"]

# Is cert-manager already running?
if helper.check_for_result(["tanzu", "package", "installed", "list", "-A"], 'cert-manager.*Reconcile succeeded'):
    pmsg.green("The cert-manager is OK.")

else:
    # Check for cert-manager as an available package: tanzu package available list -A | grep cert-manager
    found_cm = False
    lines = helper.run_a_command_get_stdout(["tanzu", "package", "available", "list", "cert-manager.tanzu.vmware.com"])
    if lines is not None:
        for line in lines:
            if re.match('\\s*cert-manager.tanzu.vmware.com', line) is not None:
                cm_version = re.split('\\s+', line)[1]
                found_cm = True

    if found_cm:
        helper.run_a_command_list(["tanzu", "package", "install", "cert-manager", "--package-name", "cert-manager.tanzu.vmware.com", "--namespace", package_namespace, "--version", cm_version, "--create-namespace"])
        # Run the command to check for reconciliation complete...
        print("Checking for reconcile...")
        if helper.check_for_result_for_a_time(["tanzu", "package", "installed", "list", "-A"], 'cert-manager.*Reconcile succeeded', 10, 36):
            pmsg.green("The cert-manager is OK.")
        else:
            pmsg.fail("Failed to install the cert-manager. Check the logs.")
            exit(1)
    else:
        pmsg.fail("The cert-manager package can't be found.")
        exit(1)
exit(0)
