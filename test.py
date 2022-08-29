from operator import add
import numpy as np
def square(n):
    print("Test")



my_list = [1,2,3,4,5,6,7,0]

sortedPicks = sorted(range(len(my_list)), key=lambda k: my_list[k])
print(sortedPicks)