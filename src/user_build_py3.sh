#!/bin/bash

# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "${SCRIPT}")

/bin/bash "${SCRIPTPATH}/_build.sh" --python="${PYTHON:-python3.3}" "$@"
