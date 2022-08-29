#!/bin/bash

source env/bin/activate
export SECRETKEY=$(echo $RANDOM | md5sum | head -c 20; echo;)
gunicorn -w 2 'main:app'
