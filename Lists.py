# fruits=["apple","banana","mango"]
# # print(fruits[1])
# # print(fruits[0:2])
# # fruits[1]="grapes"
# # print(fruits)
# fruits[0:2]=["orange","sapota"]
# print(fruits)
# fruits.append("grapes") #use append() to add value at end
# print(fruits)
# fruits.insert(0,"pomegranate") #use insert() to add value at index you want
# print(fruits)
# fruits1=["guava"]
# fruits.extend(fruits1) #extend() helps to combine both the lists
# print(fruits)
# fruits.remove("orange") #remove() helps to remove the value from list
# print(fruits)
# fruits.pop(1) #pop() with index helps to delete or pop that index value
# print(fruits)
# fruits.pop() #if we don't give index, pop() it automatically deletes from last
# print(fruits)
# del fruits[1]
# print(fruits)
# fruits.clear() #clear() empties your list
# print(fruits)

              # loop through the list

mylist = ["apple", "samsung", "Nokia"]
for i in mylist:                                # here 'i' reperesents index of mylist
    print(i)
# for i in range(0,3):
#     print(mylist[i])
# for i in range(0,len(mylist)):
#     print(mylist[i])
list1=[1,2,3,6,5,4]
# list1.sort()                  # sort() helps to arrange the list in ascending order
# print(list1)
# list1.reverse()               # reverse() is used to reverse the order of the list
# print(list1)
# list1.sort(reverse=True)      # This particular line helps to sort the order of the list in descending order
# print(list1)
          # copy lists
# list2=list1.copy()          #copy() helps to copy the list1 to list2
# print(list2)

# list2 = list1               # this type of operation is not encouraged, so dont use. instead use copy()
# print(list2)

# or use this. It gives same output as above
list2=list(list1)
print(list2)

        # join lists
# list3= mylist + list1
# print(list3)
# for i in list1:              #appending list1 values to mylist
#     mylist.append(i)
#     print(mylist)

list1.extend(mylist)
print(list1)