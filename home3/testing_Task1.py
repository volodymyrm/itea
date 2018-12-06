import os


with open('inverse.txt', 'w') as file:
    file.write('123 abc')

os.system("python Task1.py inverse.txt")

with open('inverse.txt', 'r') as file:
    result = file.read()
print('Test inverse: ', result == 'cba 321' )