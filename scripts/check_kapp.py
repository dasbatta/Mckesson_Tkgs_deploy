#!/usr/bin/env python3

import pmsg
import helper
import time

# Check and install if not found, the kapp controller into the cluster.

# Assumes that we are logged into the cluster and the context is already set.
# Assumes there is a default storage class

# Uses Templates (templates sub-directory):
# - tanzu-system-kapp-ctrl-restricted.yaml
# - kapp-controller.yaml

### Is PSP already there?
if not helper.check_for_result(["kubectl", "get", "psp"], '^tanzu-system-kapp-ctrl-restricted'):
    rc = helper.run_a_command("kubectl apply -f templates/tanzu-system-kapp-ctrl-restricted.yaml")
    if rc != 0:
        pmsg.fail("Can't install the PSP that the kapp controller needs.")
        exit(1)

    # Double-check...
    if not helper.check_for_result(["kubectl", "get", "psp"], 'tanzu-system-kapp-ctrl-restricted'):
        pmsg.fail("Can't install the PSP that the kapp controller needs.")
        exit(1)

pmsg.green("Kapp PSP OK.")

### Now check for the Kapp Controller itself...
if not helper.check_for_result(["kubectl", "get", "pods", "-n", "tkg-system"], 'kapp-controller-.*Running'):
    rc = helper.run_a_command("kubectl apply -f templates/kapp-controller.yaml")
    if rc != 0:
        pmsg.warning("Can't install the kapp controller.")
        exit(1)

# Check for kapp-controller running...
kapp_running = helper.check_for_result_for_a_time(
    ["kubectl", "get", "pods", "-n", "tkg-system"],
    'kapp-controller-.*Running',
    10,
    30)
if not kapp_running:
    pmsg.fail("Kapp Controller pod not running.")
    exit(1)

# I'm adding a 10 second sleep here because I've noticed an error in subsequent steps
# if we try too quickly to use kapp.
time.sleep(10)
pmsg.green("Kapp Controller OK.")
exit(0)
