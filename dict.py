dict1={
    "id":"20203948",
    "name":"Leela Kumar"
}

print(dict1)
print(type(dict1))
print(dict1["id"])
print(dict1.keys()) #keys() gives al the values
print(dict1.values()) # values() gives all the values
print(dict1.items()) #items() all the keys and values

dict1["name"]="Malli"
print(dict1)
dict1.update({"name":"Leela"})
print(dict1)
dict1.pop("id")
print(dict1)

dict2={
    "child1":{
        "name":"mallikarjun"
    },
    "child2":{
        "name":"leelavathi"
    }
}

print(dict2)

child3={
    "name":"lilli",
    "ocptn":"studying"
}
child4={
    "name":"lillii",
    "ocptn":"studying1"
}


dict3={
    "child3": child3,
    "child4": child4,
}

print(dict3)