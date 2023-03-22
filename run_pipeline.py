#!/usr/bin/env python3

import argparse
import importlib.util
import os
import sys
import yaml
import re
import getpass

#import pdb
# pdb.set_trace()
sys.path.append(r'./scripts')
import pmsg
import helper

# CONSTANTS
vcenter_version = "7.0.3"

# Global variables
total_errors = 0
errors = 0

# This script will prepare an on-premise vSphere environment for
# its first deployment of a TKGs workload cluster.


def dprint(msg):
    if verbose is True:
        pmsg.debug(msg)


def confirm_file(filename):
    for fname in os.listdir("."):
        if fname == filename:
            return True
    return False


def need_terraform_init():
    if confirm_file("terraform.tfstate"):
        return False
    return True


def next_step_is_abort(steps, idx):
    if idx >= len(steps) - 1:
        # last line. 
        return False
    if re.search('abort', steps[idx+1], re.IGNORECASE) is not None:
        # next line must be 'Abort' so return True
        return True
    return False


def run_terraform(tfolder):
    exit_code = 1
    pmsg.blue("=-=-=-=-=-=-= Running Terraform in " + tfolder + " =-=-=-=-=-=-=-=")
    # cd to that folder
    dir_orig = os.getcwd()
    os.chdir(tfolder)

    # verify that a "main.tf" is here...
    if confirm_file("main.tf"):
        # run terraform init
        result = 0
        if need_terraform_init():
            result = helper.run_a_command("terraform init")
        if result == 0:
            # run terrafor plan
            result = helper.run_a_command("terraform plan -out=myplan.tfplan")
            if result == 0:
                # run terraform apply
                result = helper.run_a_command("terraform apply myplan.tfplan")
                if result == 0:
                    dprint("Terraform of " + tfolder + " completed successfully.")
                    exit_code = 0
                else:
                    pmsg.fail("Terraform apply failed in " + tfolder + ".")
            else:
                pmsg.fail ("Terraform plan -out=myplan.tfplan failed in " + tfolder + ".")
        else:
            pmsg.fail("Terraform init failed in " + tfolder + ".")
    else:
        pmsg.fail("The main.tf file not found in " + tfolder + ".")
    # Leave us back in the original directory
    os.chdir(dir_orig)
    return exit_code

# ########################### Main ################################
# setup args...
help_text = "Run a a pipeline to setup a TKGs "+vcenter_version+" workload cluster on vSphere.\n"
help_text += "Examples:\n"
help_text += "./run_pipeline.py --help\n"

parser = argparse.ArgumentParser(description='Pipeline main script to deploy a TKGs workload cluster.')
parser.add_argument('-c', '--config_file', required=True, help='Name of yaml file which contains config params')
parser.add_argument('-s', '--steps_file', required=True, help='Name of steps file; what scripts will run this time.')
parser.add_argument('-d', '--dry_run', default=False, action='store_true', required=False, help='Just check things... do not make any changes.')
parser.add_argument('-v', '--verbose', default=False, action='store_true', required=False, help='Verbose output.')

args = parser.parse_args()
verbose = args.verbose
dry_run = args.dry_run

dry_run_flag = ""
if dry_run:
    dry_run_flag = " --dry_run"

verbose_flag = ""
if verbose:
    verbose_flag = " --verbose"

# Read configuration file.
if os.path.exists(args.config_file):
    with open(args.config_file, "r") as cf:
        try:
            configs = yaml.safe_load(cf)
        except yaml.YAMLError as exc:
            pmsg.fail(exc)
            exit (1)
else:
    pmsg.fail("The config file does not exist. Please check the command line and try again.")
    exit(1)

# Read the steps file
if os.path.exists(args.steps_file):
    with open(args.steps_file, "r") as sf:
        steps = sf.read().splitlines()
else:
    pmsg.fail("The steps file does not exist. Please check the command line and try again.")
    exit(1)

# Check Pre-requisites
# 1. Need pyvmomi tools
#if "pyVmomi" in sys.modules:
    #dprint("pyVmomi tools found in sys.modules.")
#elif (spec := importlib.util.find_spec("pyVmomi")) is not None:
    #dprint("pyVmomi tools found using importlib.util.find_spec.")
#else:
    #pmsg.FAIL(" You need to install pyVmomi. See https://pypi.org/project/pyvmomi/ (or just run $ pip3 install --upgrade pyvmomi.)")
    #exit(1)

###################### Put all the config parameters into the environment ########################
# Setup the environment with all the variables found in the configuration file.
for varname in configs:
    if configs[varname] is not None:
        dprint("Putting " + str(varname) + " in the environment...")
        os.environ[varname] = configs[varname]
        os.environ["TF_VAR_"+varname] = configs[varname]

# Prompt for password...
pw = getpass.getpass(prompt="Password: ", stream=None)
os.environ["vsphere_password"] = pw
os.environ["tkg_user_password"] = pw

###################### Execute all the steps in order ########################
abort_exit = False
for idx, step in enumerate(steps):
    step_type = ""
    if abort_exit:
        break

    # Ignore comment/empty lines..match.
    if re.search("^\\s*#|^\\s*$", step) is not None:
        continue

    # What kind of step is this?
    # Is it a script?
    stepname = "./scripts/" + step.strip()
    if os.path.exists(stepname):
        # Must be a script...
        step_type = "script"
        errors = helper.run_a_command(stepname)
        total_errors += errors
        if errors > 0 and next_step_is_abort(steps, idx):
            pmsg.fail("This last script had errors." + steps[idx+1])
            abort_exit = True
        continue

    # Is it a terraform directory?
    try:
        files = os.listdir(step)
        for afile in files:
            if re.search("\\.tf", afile) is not None:
                # I found a .tf file. So must be terraform
                step_type = "terraform"
                errors = run_terraform(step)
                total_errors += errors
                if errors > 0 and next_step_is_abort(steps, idx):
                    pmsg.fail("This last terraform had errors.", steps[idx+1])
                    abort_exit = True
                break
        if step_type == "terraform":
            continue
    except:
        pass

    pmsg.notice("This step is ignored: " + step)

###################### Done ########################
print ("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
if total_errors > 0:
    pmsg.warning("Number of errors/warnings encountered: " + str(total_errors) + ".")
else:
    pmsg.green("Success! There were no errors or warnings.")
pmsg.blue ("Done.")