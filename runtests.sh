#!/bin/bash

# Run streamlit app in the background
streamlit run app.py &
p1_pid=$!

# Giving some time to import data
sleep 20

# Running tests with unittest
python -m unittest discover -s test_cases
ret=$?

# Kill streamlit process
kill $p1_pid

exit $ret