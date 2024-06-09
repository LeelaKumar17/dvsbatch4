myset={'apple','banana','orange'} # index is not possible for set type and duplicate value is ignored in set
print(myset) #order is unpredictable in set data type, these are immutable
print(type(myset))
myset.add('grape') #add() is used a add value to the set
print(myset)
tset={'1','2','3'}
myset.update(tset) #update() helps to add or combine two sets
print(myset)
myset.remove('apple')
print(myset)
myset.discard('banana')
print(myset)
myset.clear()
print(myset)
set1={'a','b','c'}
set2={"c","d","b"}
set3=set1.union(set2) #union() cpmbines the sets by ignoring the duplicates
print(set3)
set4=set1.intersection(set2) #intersection() gives common values as output
print(set4)
set5=set1.symmetric_difference(set2) #symmetric_difference() gives non-common values
print(set5)
set6=set1.symmetric_difference_update(set2)
print(set6)