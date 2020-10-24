#!/bin/bash

# Run your app in the background
streamlit run app.py >/dev/null &

p1_pid=$!
sleep 20
python -m unittest discover -s test_cases
p2_pid=$!

# Kill streamlit process
kill $p1_pid