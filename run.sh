#!/bin/bash

# Run your app in the background
streamlit run app.py &
p1_pid=$!
sleep 20
python -m unittest discover -s test_cases
p2_pid=$!

# Kill streamlit process
kill $p1_pid

# Optionally exit true to prevent travis seeing this as an error
# exit 0