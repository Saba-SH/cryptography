#!/bin/bash

# TESTING SCRIPT FOR THE CHALLENGES IN THIS REPOSITORY

# "./test.sh <challenge_index>" runs all testcases for a specific challenge
# "./test.sh all" runs all testcases for all challenges here

# for each testcase, runs challenge code with testcase input as stdin
# outputs either "SUCCESSFUL" or "FAILED", 
# depending on whether the simulation output matches the expected output

# at the end of all testcases, notifies whether all of them passed or some failed

if [ "$#" -ne 1 ]; then
    echo "Usage:"
    echo "to run a single test: $0 <challenge_index>"
    echo "to run all tests:     $0 all"
    exit 1
fi

challenge_index=$1

if [ "$challenge_index" == "all" ]; then 
    for i in {1..6}; do
        echo "---------------------------------"
        $0 $i
    done
    echo "---------------------------------"
    exit 0
fi

echo "TESTING CHALLENGE $challenge_index"
echo

all_good=1

for i in {0..4}; do
    expected=$(cat tests/tests_${challenge_index}/out_${i}.txt)
    output=$(python3 challenge${challenge_index}.py < tests/tests_${challenge_index}/in_${i}.txt)

    expected=$(echo -n "$expected" | tr -s '[:space:]')
    output=$(echo -n "$output" | tr -s '[:space:]')

    if [ "$expected" == "$output" ]; then
        echo "TEST ${challenge_index}-${i} SUCCESSFUL"
    else
        echo "TEST ${challenge_index}-${i} FAILED"
        all_good=0
    fi
done

echo
if [ "$all_good" == "1" ]; then
    echo "ALL TESTS PASSED FOR CHALLENGE $challenge_index"
else 
    echo "SOME TEST(S) FAILED FOR CHALLENGE $challenge_index"
fi
