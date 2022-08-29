#!/usr/bin/python3

# update-super-project.py - Updates the submodules of the superproject.
#
# Instructions:
#
# install ConfigArgParse: "pip3 install ConfigArgParse"
#
# Run ./update-super-project.py -h to view help commmands.
#
# Create a config file with the following contents and run the command ./update-super-project.py -c config.yml
#
# ---
# superproject-branches:
#   - develop
#   - master


import os
import subprocess
import configargparse
import functools
print = functools.partial(print, flush=True)

parser = configargparse.ArgParser(description='This script updates the submodules of the superproject.', default_config_files=['*superprojectconfig.yml'], config_file_parser_class=configargparse.YAMLConfigFileParser)
# (the * wildcard in *superprojectconfig.yml allows for the possibility the config file is missing, which is ok we will display an error shortly.)
parser.add('-c','--config', is_config_file=True, help='config file path')
parser.add('--superproject-branches', help='branches that will be processed', action='append')
parser.add('--pushtorepo', help='push updates to repo. Enabled by default.', action='store_true', default=True)
parser.add('--no-pushtorepo', dest='pushtorepo', help='disable push updates to repo', action='store_false')
parser.add('--gh-user', help='github user', default='', env_var='GH_USER')
parser.add('--gh-token', help='github token', default='', env_var='GH_TOKEN')
parser.add('--gh-repo', help='github repository', default='https://github.com/boostorg/boost')
parser.add('-v','--verbose', help='verbose', action='store_true')

options = parser.parse_args()

# Validation section

if options.superproject_branches is None:
    print("")
    print("The variable superproject-branches hasn't been set. Create a config file in this directory named superprojectconfig.yml, or in any location with -c config.yml, \
and add the following contents. Then rerun the script.")
    print("---")
    print("superproject-branches:")
    print("  - develop")
    print("  - master")
    print("")
    exit(1)
elif options.superproject_branches == [''] or options.superproject_branches == '':
    print("")
    print("The variable superproject-branches is empty which may mean you have intentionally cleared it. If you'd like this script to process the submodules, \
configure superproject-branches. Exiting.")
    print("")
    exit(0)

# Check that GH_USER and GH_TOKEN are present. Set them based on the config if necessary. Github uses env variables.

if not os.getenv('GH_USER'):
    if options.gh_user:
        print("Setting env variable GH_USER based on options.gh_user")
        os.environ['GH_USER'] = options.gh_user
    else:
        print("Please set the environment variable GH_USER")
        exit(1)
if not os.getenv('GH_TOKEN'):
    if options.gh_token:
        print("Setting env variable GH_TOKEN based on options.gh_token")
        os.environ['GH_TOKEN'] = options.gh_token
    else:
        print("Please set the environment variable GH_TOKEN")
        exit(1)


for branch in options.superproject_branches:
    directory="/opt/github/boostworkspace/" + branch
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)
    if not os.path.exists(directory + "/boost"):
        print('Running subprocess.run(["git", "clone", "-b", branch, options.gh_repo])')
        subprocess.run(["git", "clone", "-b", branch, options.gh_repo])
    print("Changing directory to " + directory + "/boost")
    os.chdir(directory + "/boost")
    # allow git credentials to be read from $GH_USER and $GH_TOKEN env variables
    credentialhelperscript='!f() { sleep 1; echo "username=${GH_USER}"; echo "password=${GH_TOKEN}"; }; f'
    subprocess.run(['git', 'config', 'credential.helper', '%s'%(credentialhelperscript)])
    # git checkout is redundant, but that's ok
    print('Running subprocess.run(["git", "checkout", branch])')
    subprocess.run(["git", "checkout", branch])
    print('Running subprocess.run(["git", "pull"])')
    subprocess.run(["git", "pull"])
    print('Running subprocess.run(["git","submodule","update","--init","--recursive"])')
    subprocess.run(["git","submodule","update","--init","--recursive"])
    allsubmodules=[]
    # cut -f2 before checking out submodules, and cut -f3 after.
    commandresult=subprocess.run(["git submodule |cut -d' ' -f3"], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    allsubmodules=commandresult.stdout.split() 
    limit = 10000
    for index, submodulepath in enumerate(allsubmodules):
        if index == limit: 
            break
        print("submodule path is " + submodulepath)
        commandresult=subprocess.run(["git -C " + submodulepath + " config --get remote.origin.url"], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        submoduleurl=commandresult.stdout
        print("submodule url is " + submoduleurl)
        submodulereponame = os.path.basename(submoduleurl)
        submodulename = submodulereponame.split('.')[0]
        print("submodule name is " + submodulename)
        print('Running subprocess.run(["git", "submodule", "update", "--remote","--",submodulepath])')
        subprocess.run(["git", "submodule", "update", "--remote","--",submodulepath])
        commandresult=subprocess.run(["git diff --quiet"], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        if commandresult.returncode != 0:
            print("submodule " + submodulepath + " changed.")
            message="Update " + submodulename + " from " + branch
            print('Running subprocess.run(["git", "add", "."])')
            subprocess.run(["git", "add", "."])
            print('Running subprocess.run(["git", "commit", "-m", message])')
            subprocess.run(["git", "commit", "-m", message])
            if options.pushtorepo:
                print('Running subprocess.run(["git", "push"])')
                subprocess.run(["git", "push"])
   # One final "git push" (which isn't "git push --force") to recover from any network or authentication errors earlier.
    if options.pushtorepo:
        print('Completed branch ' + branch + ', running subprocess.run(["git", "push"])')
        subprocess.run(["git", "push"])
