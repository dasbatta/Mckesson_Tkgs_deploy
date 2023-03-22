#!/usr/bin/env python3

# Importable library of routines for printing messages with color.

# CONSTANTS
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GREY = '\033[36m'

class pmsg():
    """
    Class used to print messages in color.
    """
def __init__(self):
    pass

def notice(msg):
    print (bcolors.HEADER + "NOTICE: " + bcolors.ENDC + " " + msg)

def dry_run(msg):
    print (bcolors.WARNING + "WARNING: " + bcolors.ENDC + " " + msg + " " + bcolors.FAIL + "The dry_run flag is on." + bcolors.ENDC)

def warning(msg):
    print (bcolors.WARNING + "WARNING: " + bcolors.ENDC + " " + msg)

def fail(msg):
    print (bcolors.FAIL + "ERROR: " + bcolors.ENDC + " " + msg)

def green(msg):
    print (bcolors.OKGREEN + msg + bcolors.ENDC)

def blue(msg):
    print (bcolors.OKBLUE + msg + bcolors.ENDC)

def debug(msg):
    print (bcolors.GREY + "  DEBUG: " + msg + bcolors.ENDC)

def normal(msg):
    print (msg)

def running(msg):
    print (bcolors.BOLD + "  Running: " + msg + bcolors.ENDC)

def underline(msg):
    print ("   " + bcolors.UNDERLINE + bcolors.OKBLUE + msg + bcolors.ENDC)