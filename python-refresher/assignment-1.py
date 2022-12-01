"""
Assignment 1: Variables
"""

money = 50
item_price = 15
tax = .03

# Calculate the total price of the item
total_price = item_price + (item_price * tax)
money = money - total_price

print(money)
