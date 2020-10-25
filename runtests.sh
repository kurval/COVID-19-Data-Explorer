#!/bin/bash

# Run your app in the background
streamlit run app.py &
p1_pid=$!
sleep 20
python -m unittest discover -s test_cases
ret=$?

# Kill streamlit process
kill $p1_pid

exit ret