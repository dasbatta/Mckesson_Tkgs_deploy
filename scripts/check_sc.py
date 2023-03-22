#!/usr/bin/env python3

# Checks to see if the storage class (named in the configuration file) is the default.
# If not, uses 'kubectl patch' to make it so.

import subprocess
import re
import os
import pmsg

storage_class = os.environ["storage_class"]

def storage_class_is_default(storage_class):
    # check the storage class. Is it the default?
    # Return True or False

    process = subprocess.Popen(["kubectl", "get", "sc"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()
    storage_classes = output.splitlines()
    rc = False
    for sc in storage_classes:
        if re.search("^" + storage_class + "\\s+\\(default", sc.decode("utf-8")) is not None:
            rc = True
            pmsg.green("Default storage class OK.")
            break
    return rc


# ######################### Main #########################
if not storage_class_is_default(storage_class):
    process = subprocess.Popen(["kubectl", "patch", "storageclass", storage_class, "-p", '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}"'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()

    # Check again to verify...
    if not storage_class_is_default(storage_class):
        exit(1)
exit(0)
