#!/bin/bash

# Run your app in the background
streamlit run app.py &
p1_pid=$!
sleep 20
python -m unittest discover -s test_cases &
p2_pid=$!

# sleep for X seconds
sleep 120

# Kill the python process
kill $p1_pid
kill $p2_pid
