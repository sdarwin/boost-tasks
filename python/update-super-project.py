#!/usr/bin/python3

import os
import subprocess

boostrepository="https://github.com/boostorg/boost"
mainbranches=("master","develop")

# Get environment variables
GH_USER = os.getenv('GH_USER')
GH_TOKEN = os.environ.get('GH_TOKEN')

for branch in mainbranches:
    directory="/opt/github/boostworkspace/" + branch
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)
    if not os.path.exists(directory + "/boost"):
        subprocess.run(["git", "clone", "-b", branch, boostrepository])
    print("Changing directory to " + directory + "/boost")
    os.chdir(directory + "/boost")
    # allow git credentials to be read from $GH_USER and $GH_TOKEN env variables
    credentialhelperscript='!f() { sleep 1; echo "username=${GH_USER}"; echo "password=${GH_TOKEN}"; }; f'
    subprocess.run(['git', 'config', 'credential.helper', '%s'%(credentialhelperscript)])
    # git checkout is redundant, but that's ok
    subprocess.run(["git", "checkout", branch])
    subprocess.run(["git", "pull"])
    subprocess.run(["git","submodule","update","--quiet","--init","--recursive"])
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
            print('Running subprocess.run(["git", "push"])')
            subprocess.run(["git", "push"])

