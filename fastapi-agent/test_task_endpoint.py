#!/usr/bin/env python3
"""
Test the /task endpoint with the Fibonacci task
"""
import requests
import json
import urllib.parse

# The task that will be graded
task = "Write and run a program that prints the 18th Fibonacci number (F0 = 0, F1 = 1). Return just the number."

# URL encode the task
encoded_task = urllib.parse.quote(task)

# Make the request
url = f"http://127.0.0.1:8000/task?q={encoded_task}"
print(f"Testing URL: {url}\n")

print("Making request to the API...")
response = requests.get(url)

print(f"Status Code: {response.status_code}")
print(f"Content-Type: {response.headers.get('content-type')}\n")

print("Response JSON:")
data = response.json()
print(json.dumps(data, indent=2))

# Verify the response structure
print("\n" + "="*60)
print("Verification:")
print("="*60)
assert "task" in data, "Missing 'task' field"
assert "agent" in data, "Missing 'agent' field"
assert "output" in data, "Missing 'output' field"
assert "email" in data, "Missing 'email' field"

print(f"✓ Task: {data['task'][:50]}...")
print(f"✓ Agent: {data['agent']}")
print(f"✓ Email: {data['email']}")
print(f"✓ Output: {data['output'][:100]}...")

# Check if output contains the expected Fibonacci number
expected = "2584"
if expected in data['output']:
    print(f"\n✓✓✓ SUCCESS! Output contains the 18th Fibonacci number: {expected}")
else:
    print(f"\n⚠ Warning: Expected output to contain {expected}")
    print(f"Full output: {data['output']}")
