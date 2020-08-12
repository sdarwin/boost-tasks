#!/bin/bash

set -x
DIRNAME=$(dirname $0)
cat $DIRNAME/hosts >> /etc/hosts
service ssh start
service apache2 start
sleep 5 
service apache2 restart
