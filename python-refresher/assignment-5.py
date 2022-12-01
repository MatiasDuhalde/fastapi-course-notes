"""
Assignment 5: Loops
"""

my_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

for _ in range(3):
    i = 0
    while i < len(my_list):
        if my_list[i] == "Monday":
            i += 1
            continue
        print(my_list[i])
        i += 1
