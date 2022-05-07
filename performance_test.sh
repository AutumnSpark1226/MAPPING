#!/bin/zsh
# test performance

# pybricks-micropython
START0=$(date +%N)
pybricks-micropython test.py > /dev/null
STOP0=$(date +%N)

# python3
START1=$(date +%N)
python3 test.py > /dev/null
STOP1=$(date +%N)

# calculate time
TIME0=$((STOP0 - START0))
TIME1=$((STOP1 - START1))

# print results
echo "pybricks-micropython: $TIME0 ns"
echo "python3: $TIME1 ns"
