#!/usr/bin/env python3
"""
Test script to verify the 18th Fibonacci number
F0 = 0, F1 = 1
"""

def fibonacci(n):
    """Calculate the nth Fibonacci number"""
    if n == 0:
        return 0
    elif n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Test the 18th Fibonacci number
result = fibonacci(18)
print(f"The 18th Fibonacci number is: {result}")

# Verify with the sequence
print("\nFibonacci sequence (0-18):")
for i in range(19):
    print(f"F{i} = {fibonacci(i)}")
