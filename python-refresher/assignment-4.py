"""
Assignment 4: If Statements
"""

import random

grade = random.randint(0, 100)

if grade >= 90:
    print("A")
elif grade >= 80:
    print("B")
elif grade >= 70:
    print("C")
elif grade >= 60:
    print("D")
else:
    print("F")
