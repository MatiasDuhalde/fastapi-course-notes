"""
Assignment 6: Dictionaries
"""

my_vehicle = {
    "model": "Ford",
    "make": "Explorer",
    "year": 2018,
    "mileage": 40000
}

for key, value in my_vehicle.items():
    print(value)

vehicle_2 = my_vehicle.copy()

vehicle_2['number_of_tires'] = 4
del vehicle_2['mileage']

for key in vehicle_2:
    print(key)
