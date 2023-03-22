#!/usr/bin/env python3

# Interpolates yaml into a template file and generates a combined output file.
# This can be used as a importable library
#  or can be run from the terminal command line. Try ./interpolate.py --help

import argparse
from jinja2 import Template
import os
import yaml

class interpolate():
    """
    Class used to do interpolation.
    """

#########################################################
def __init__(self):
    pass

#########################################################
def interpolate_from_yaml_to_template(yaml_source, template_file, output_file):
    """
    Interpolate a template_file given variables and values from the yaml_source file.
    Create a results output file interpolated.

    :param yaml_source: String file name of yaml_source values
    :param template_file: String file name of the template file to interpolate yaml source values into.
    :param output_file: String file name of the resulting file.
    :returns: boolean - True, interpolation succeded.
    :rtype: bool
    """

    with open(yaml_source,'r') as y:
        # build interp_dict from yaml
        interp_dict = yaml.load(y, Loader=yaml.FullLoader)

        with open(template_file) as jt:
            all_jt_lines = jt.read()
            template = Template(all_jt_lines)
            interpolated_string = template.render(interp_dict)

            j = open(output_file, "w")
            j.write(interpolated_string)
            j.close()
            if len(interpolated_string) > 1:
                return True
    return False
