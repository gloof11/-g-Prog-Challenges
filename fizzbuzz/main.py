#!/usr/bin/python3

import sys
import numpy as np

# User input
text = sys.argv[1]

for number in sorted(np.unique(text.split(","))):
    # If the number is divisible by 3, print the number FIZZ
    # If the number is divisible by 5, print the number BUZZ

    # Do error checking incase user inputs a non integer
    try:
        if(int(number) % 3 == 0):
            print(str(number) + " Fizz!")
        elif(int(number) % 5 == 0):
            print(str(number) + " Buzz!")
        else:
            print(number)
    except TypeError:
        print("Please input an integer!")