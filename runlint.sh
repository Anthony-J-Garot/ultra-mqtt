#!/bin/bash

PYLINT=/usr/local/bin/pylint

PYLINT_OPTS="-j 0 -v -f colorized"

# I suppose I could run it on the unit tests, too; but for now,
# this will do.
CMD="$PYLINT $PYLINT_OPTS ./src"
echo $CMD
eval $CMD
