def chunks(l, n):
    """Yield successive n-siyed chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

x = [1,2,2,2,2,2,3,3,2,3,3,2]
# ([x[i] for i in range(len(x[1:])) if x[i] not in x[i + 1:] ])
y = [x[i:i + 2] for i in range(0, len(x), 2)]
z = [y[i] for i in range(len(y)) if (y[i] not in y[i+1:] and list(reversed(y[i])) not in y[i+1:]) ]
#a = [blah.reverse() for blah in z]
print(z)
#print(a)
print (x)




#a = [1,2]
#A = [[1,2],[3,4]]
#print(a in A)
