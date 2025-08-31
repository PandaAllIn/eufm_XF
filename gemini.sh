#!/bin/bash

# A simple shell script to interact with the Google Gemini API using curl.

# Your API key
API_KEY="AIzaSyBMXkjP7uOjm1bPl5a2l-lABE1sqmvjBwA"

# The model to use
MODEL="gemini-1.5-pro-latest"

# The prompt is the first argument to the script
PROMPT="$1"

# The API endpoint
API_URL="https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${API_KEY}"

# The curl command
curl -s -H 'Content-Type: application/json' -d "{\"contents\":[{\"parts\":[{\"text\":\"${PROMPT}\"}]}]}" "${API_URL}"
