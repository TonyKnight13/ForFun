a = dict()
a['a'] = [1,2,3]

b = a.copy()
b['a'] = [5,6]
c = a.copy()
d = b.copy()

print(a)
print(b)
print(c)
print(d)