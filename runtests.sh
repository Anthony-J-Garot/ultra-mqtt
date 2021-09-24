#!/bin/bash

PYTHON=/usr/bin/python3         # Specifies exact python since can be more than 1
export PYTHONPATH="./src/"      # Tests need to know location of source files

# This allows me to simply put "breakpoint()" in code.
#export PYTHONBREAKPOINT="ipdb.set_trace"
export PYTHONBREAKPOINT="pudb.set_trace"

# Python arguments
# 		-Wa = tells python to display warnings (can get noisy)
ARGS="-Wa -m unittest --failfast"

if [[ "$1" == "" ]]; then
	# Unit Test All The Things!
	CMD="$PYTHON $ARGS"
	echo $CMD
	eval $CMD
else
	if [[ "$2" == "" ]]; then
		# Specific file of tests, e.g. test_utils
		CMD="$PYTHON $ARGS tests.$1"
		echo $CMD
		eval $CMD

	else
		# Specific test within a file
		CMD="$PYTHON $ARGS tests.$1.UltraMqttTestCase.$2"
		echo $CMD
		eval $CMD
	fi
fi
