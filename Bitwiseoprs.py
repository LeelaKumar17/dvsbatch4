#print(bin(2))  #to know the binary value of any number use bin()

a=10
print(bin(a))
b=8
print(bin(b))
print(a & b) #AND if both bits are 1, then 1
print(a | b) #OR if any one of the bits is 1, then 1
print(a ^ b) #XOR if only one of the bit is 1, then 1
print(~a) #NOT inverts all the bits
print(bin(a))
print(a << 2 ) #LEFT SHIFT, removes two bits at extreme left and adds zero value in empty positions at right
print(bin(a))
print(a >> 2) #RIGHT SHIFT, removes two bits at extreme right and adds zero value in empty positions at left