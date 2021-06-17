#!/bin/bash

echo "Running setting environment"
./usr/local/bin/set-env.sh

echo "Running bootstrap.py"
python3 /opt/serverboi/scripts/bootstrap.py

echo "Bootstrap complete"