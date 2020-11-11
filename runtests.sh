#!/bin/bash

# Run streamlit app in the background
streamlit run app.py &
p1_pid=$!

# Giving some time to import data
sleep 20

# Running tests with Firefox and Chrome
echo Running tests on Firefox
python tests.py firefox
ret1=$?

echo Running tests on Chrome
python tests.py chrome
ret2=$?

# Check if tests fails or passes
if [ $ret1 != 0 ] || [ $ret2 != 0 ]
then
    ret=1
else
    ret=0
fi

# Kill streamlit process
kill $p1_pid

exit $ret