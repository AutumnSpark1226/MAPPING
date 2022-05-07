#!/bin/zsh
# test performance

# pybricks-micropython
START0=$(date +%s)
pybricks-micropython test.py > /dev/null
STOP0=$(date +%s)

# python3
START1=$(date +%s)
python3 test.py > /dev/null
STOP1=$(date +%s)

# calculate time
TIME0=$((STOP0 - START0))
TIME1=$((STOP1 - START1))

# print results
echo "pybricks-micropython: $TIME0 s"
echo "python3: $TIME1 s"
