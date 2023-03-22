# mckesson-dscsa-deployment
Code to deploy clusters for the McKesson DSCSA project - Drug Distribution Centers

The code directory struction looks like this:
root directory - Contains run_pipeline.py, config.yaml and steps.conf
| - scripts subdirectory - Contains all scripts that actually check/deploy things (except terraform stuff)
| - terraform subdirectory - Contains terraform .tf file(s). You can add as many of these directories as you need. The run_pipeline.py will find them if they are referenced in the steps.conf file.


## How to run this

In order to run this code, you have to 
1. Update the config.yaml - This contains all the variables needed to build up a TKGs cluster starting from vSphere 7.0.3
2. Check the steps.conf - This file contains the list of steps (script names as found in the scripts subdirectory -OR- terrform subdirectory names) that will be run.

After these two things are complete, run the following

$ ./run_pipeline.py -c config.yaml -s steps.config

## How to add steps

Note that all config lines in the config.yaml are added to the environment (environment variables) so that your scripts don't need to read the config.yaml file or take in arguments. All scripts have access to all the config data in the environment. The same is true for terraform scripts noting that terraform can read environment variables that have "TF_VAR_" prepended to them. For example: if you want to use the "cluster_name" variable in terraform, you can use 'var.cluster_name'. You will notice that the environment has "TF_VAR_cluster_name" in it when terraform is invoked by the 'run_pipeline.py' script.

In order to add steps to this TKGs deployment system

### add a new script
1. Create a new script in the 'scripts' subdirectory. Access the config.yaml data by using the environment variables by the same name.
1.1 Scripts should exit(0) if they ran correctly and exit(>0) if not
2. Add the script name in the appropriate place in the 'steps.conf' file. Note that you can have a steps config file with just what you want to test as long as all the dependencies are already met in the target system.

### add terraform
You can add terraform if that is best for adding capabilities to this deployment system by either
1. Add lines to an existing terraform .tf file
2. OR create a new terraform subdirectory and create .tf files in that. Then add this new terraform subdirectory to a steps file to test it.

### Helpful things if you are writing in python

1. There is a module for printing messages with color. If you use this, it will make the output look consistent. Use 'import pmsg'.
2. There is a module of interpolating yaml into templates. Use 'import interpolate'.
3. There is a function for running a shell command (e.g. tazu package installed list -A) and looping to check for a final state that you are waiting for. Use 'import helper' and use helper.check_for_result_for_a_time().
4. If you want to add helpful other functions into a module, add them to 'helper.py' (in the scripts subdirectory).