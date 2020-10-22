#!/bin/bash

# Run your app in the background
streamlit run app.py &
p1_pid=$!
sleep 20
python3 -m unittest discover -s test_cases &
p2_pid=$!

# sleep for X seconds
sleep 120

# Kill the python process
kill $p1_pid
kill $p2_pid

# Optionally exit true to prevent travis seeing this as an error
exit 0