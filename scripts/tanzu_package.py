#!/usr/bin/env python3

# Makes sure that the tanzu package repo is available in the cluster.
# Assumes kapp controller is already installed.

import helper
import os
import pmsg
#import pdb

tanzu_package_registry = os.environ["tanzu_package_registry"]
tanzu_standard_package_repo_name = os.environ["tanzu_standard_package_repo_name"]
tanzu_package_registry_version = os.environ["tanzu_package_registry_version"]
repo = tanzu_standard_package_repo_name + ":" + tanzu_package_registry_version 
#pdb.set_trace()
expression = tanzu_standard_package_repo_name + '.*' + tanzu_package_registry + '.*' + tanzu_package_registry_version + '.*Reconcile succeeded'

if not helper.check_for_result(["tanzu", "package", "repository", "list", "-A"], expression):
    # Run command to create the local repository
    rc = helper.run_a_command("tanzu package repository add " + tanzu_standard_package_repo_name + " -n tanzu-package-repo-global --url " + tanzu_package_registry + ":" + tanzu_package_registry_version)
    if rc != 0:
        pmsg.fail("Can't add " + tanzu_standard_package_repo_name + " repository to this cluster.")
        exit(1)

    # Double check ...
    repo_ready = helper.check_for_result_for_a_time(["tanzu", "package", "repository", "list", "-A"], expression, 2, 45)
    if not repo_ready:
        pmsg.fail("Can't create local repo " + tanzu_standard_package_repo_name + ".")
        exit(1)

# And check for cert-manager and contour
found_contour = helper.check_for_result(["tanzu", "package", "available", "list", "-A"], "contour")
if not found_contour:
    pmsg.fail("Can't find contour in the list of available packages.")
    exit(1)

pmsg.green("Local package repo " + tanzu_standard_package_repo_name + " OK.")
exit(0)
