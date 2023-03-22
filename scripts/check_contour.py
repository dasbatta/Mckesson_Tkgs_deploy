#!/usr/bin/env python3

# Checks to see if contour.tanzu.vmware.com is installed and running.
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
contour_template_file = "templates/contour-data-values.yaml"

# Is contour already running?
if helper.check_for_result(["tanzu", "package", "installed", "list", "-A"], 'contour.*Reconcile succeeded'):
    pmsg.green("The contour.tanzu.vmware.com package is OK.")

else:
    # Check for contour.tanzu.vmware.com as an available package: tanzu package installed list -A |grep -i contour.tanzu.vmware.com
    found_contour = False
    lines = helper.run_a_command_get_stdout(["tanzu", "package", "available", "list", "contour.tanzu.vmware.com"])
    if lines is not None:
        for line in lines:
            if re.match('\\s*contour.tanzu.vmware.com', line) is not None:
                contour_version = re.split('\\s+', line)[1]
                found_contour = True

    if found_contour:
        helper.run_a_command_list(["tanzu", "package", "install", "contour", "--package-name", "contour.tanzu.vmware.com", "--namespace", package_namespace, "--version", contour_version, "--values-file", contour_template_file])
        # Run the command to check for reconciliation complete...
        print("Checking for reconcile...")
        if helper.check_for_result_for_a_time(["tanzu", "package", "installed", "list", "-A"], 'contour.*Reconcile succeeded', 10, 36):
            pmsg.green("The contour.tanzu.vmware.com package is OK.")
        else:
            pmsg.fail("Failed to install the contour.tanzu.vmware.com. Check the logs.")
    else:
        pmsg.fail("The contour.tanzu.vmware.com package can't be found.")
        exit(1)
exit(0)