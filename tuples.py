tuple1=('apple','banana','orange')
# print(tuple1[2])
# tuple1[2]="grape"
# print(tuple1)         #tuple is immutable i.e., we can't change the values of tuple
tuple2=('apple')
print(type(tuple1))
tuple3=('apple',)
print(type(tuple2))
print(tuple1[:2])   # it will consider intial index as 0 here
print(tuple1[0:])   # it will print all the index values till end

#to mutable the tuble
mytuple = list(tuple1)
print(mytuple)
mytuple[1]="xyz"
print(mytuple)
tuple1=tuple(mytuple)
print(tuple1)
for i in tuple1:
    print(i)
for i in range(0,3):
    print(tuple1[i])
for i in range(0,len(tuple1)):
    print(tuple1)

tuple4=tuple1*2
print(tuple4)
a=tuple4.count("apple")
print(a)
c=tuple1.index('apple')
print(c)
