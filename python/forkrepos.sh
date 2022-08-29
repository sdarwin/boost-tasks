#!/bin/bash

# This script forks all submodules of boost to your own account.

SOURCEREPO=https://github.com/boostorg/boost
SOURCEBRANCH=develop

if [ -z "$GH_USER" ] || [ -z "$GH_TOKEN" ]; then
    echo "Please set github credentials"
    echo "export GH_USER="
    echo "export GH_TOKEN="
    exit 1
fi

if ! command -v gh &> /dev/null
then
    echo "gh could not be found. Installation instructions at https://cli.github.com/manual/installation"
    exit 1
fi

if [ ! -d "boost" ]; then
    git clone -b $SOURCEBRANCH $SOURCEREPO
fi

cd boost
git checkout $SOURCEBRANCH

git submodule update --init
git submodule foreach gh repo fork --remote

echo "And, fork the superproject itself, if it hasn't been done already:"
gh repo fork --remote
