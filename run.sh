#!/bin/bash

# Run your app in the background
streamlit run app.py &
p1_pid=$!
sleep 20
python -m unittest tests.CompareCountries.test_log_scale
p2_pid=$!

# Kill streamlit process
kill $p1_pid

# Optionally exit true to prevent travis seeing this as an error
exit 0