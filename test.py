from operator import add
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



7 * 6


| | | | | | | |
 _ _ _ _      
       _ _ _ _ 

       7-4 = 3