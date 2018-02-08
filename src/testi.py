from src.testfunction import *
print("Start Tutorial")

array = [0, 1, 2, 3, 4, 5]

for i in array:
    print(array[i], " ", end='')

print("easy array for fertig")

for i in range(0,10):
    print(i, "", end='')
print("easy for fertig")
i=0
while i<10:
    i += 1
    print(i, end='.')
print("easy while fertig")


def stupidfuckingfunction(a,b):
    return a+b


print(stupidfuckingfunction("shit", "fuck"))
print(stupidfuckingfunction(10, 5))

a = 5
b = 5

if b >= a:
    print(b, "ist größer als", a)
else:
    print(a, "ist größer als", b)


inp = input("Enter your Input: ")
if not inp.isdigit():
    print("Dat Shit aint int")
    exit(-1)
print(inp)

testfunctioninotherfile("Endlich")
