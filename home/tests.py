from django.test import TestCase

# Create your tests here.

num = int(input('Enter a number: '))
sum = 0

while num % 2 != 0:
    sum += num
    num = int(input('Enter a numner: '))

if num % 2 == 0:
    sum += num

print(sum)