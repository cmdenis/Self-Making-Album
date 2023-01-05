a = [1, 2, 3, 4, 5]
b = ['a', 'b', 'c', 'd', 'e']

c = dict(zip(b, a))

print(c["a"])

print()

for i in c:
    print(i)

b = ['k', 'b', 'c', 'd', 'e']


for i in c:
    print(i)