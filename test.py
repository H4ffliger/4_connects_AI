from operator import add
import numpy as np
def square(n):
    print("Test")



my_list = [2,3,4,5,6,7,8,9]
my_list2 = [2,3,4,5,6, 0, 0, 0]
result = map(square, my_list)
list(result)

a = list(map(add, my_list, my_list2))


test_list = [4, 5, 6, 3, 9]
insert_list = [2, 3]
  
test_list.extend(insert_list)

print(test_list)

viewfield = [0]*10

print(np.any(viewfield))

x1 = 0
x2 = 0
x3 = 0
x4 = 0
gameW = 5
for y in range(0, 10000):
    x = np.random.randint(0,gameW-1)
    if(x == 0):
        x1 += 1
    if(x == 1):
        x2 += 1
    if(x == 2):
        x3 += 1
    if(x == 3):
        x4 += 1

print("1: " + str(x1))
print("2: " + str(x2))
print("3: " + str(x3))
print("4: " + str(x4))