"""
Assignment 3: Lists
"""

zoo = ["Lion", "Monkey", "Tiger", "Elephant", "Zebra"]

zoo.pop(2)

zoo.append("Giraffe")

zoo.pop(0)

print(*(animal for animal in zoo))

print(zoo[:3])
