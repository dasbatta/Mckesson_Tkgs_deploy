#!/usr/bin/env python3

# merges files into one resulting file.
# The resulting file contains all of the lines of all the source files.

import argparse
import os

class merge_files():
    """
    Class used to merge files.
    """

    #########################################################
    def __init__(self):
        pass

    #########################################################
    def yamlize(self, source_file, varname, result_file):
        """
        Converts the source_file (only the first line) into a yaml line.
        Uses 'varname' as the yaml variable name.
        and puts them in to result_file.

        :param source_file: String file name of the source file.
        :param varname: variable name to put in front of the value
        :param result_file: String file name of combined file
        :returns: boolean - True, merge succeded.
        :rtype: bool
        """

        lines_copied = 0

        if not os.path.exists(source_file):
            print ("Source file: " + source_file + " does not exist.")
            return ""

        s = open(source_file, "r")
        r = open(result_file, "w")
        line = s.readline()
        r.write(varname + ": " + line)
        r.close()
        s.close()
        return result_file

    #########################################################
    def merge_files(self, source_files, result_file):
        """
        Merges all of the lines from source_files...
        and puts them in to result_file.

        :param source_files: Array of String file names of the source files.
        :param result_file: String file name of combined file
        :returns: boolean - True, merge succeded.
        :rtype: bool
        """

        lines_copied = 0

        # Do the source files exist?
        for file in source_files:
            if not os.path.exists(file):
                print ("Source file: " + file + " does not exist.")
                exit(1)

        # Open the result_file
        r = open(result_file, "w")

        for file in source_files:
            with open(file,'r') as s:
                r.write("\n# " + file + "\n")
                for line in s:
                    r.write(line)
                    lines_copied += 1
            #close(s)

        r.close()

        if lines_copied > 0:
            return True
        else:
            return False

    #########################################################
    def command_line_main(self):
        """
        Merge files after parsing command line arguments.
        """

        help_text="Merge multiple files into a resulting output file.\n"
        help_text+="Examples:\n"
        help_text+="./merge_files.py --help\n"
        help_text+="./merge_files.py -s \"<sourcefile1,sourcefile2,...>\" -o <output_file>\n"

        parser = argparse.ArgumentParser(description=help_text, formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('-s', '--source_files', help='Source filenames, comma separated.', required=True)
        parser.add_argument('-o', '--output', help='Output filename.', required=True)
        args = parser.parse_args()

        # Make an array of source files from the comma separated string...
        source_file_array = args.source_files.split(",")
    
        return self.merge_files(source_file_array, args.output)

################# Start here ###############
if __name__ == "__main__":
  merge_obj = merge_files()
  rc = merge_obj.command_line_main()
  if rc:
    exit(0)
  else:
    exit(1)
