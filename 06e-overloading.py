# overloading



n = 100
numbers = range(2, n)

results = []
while len(numbers) > 0:
	results.append(numbers[0])
	for num in numbers:
		if (num % numbers[0] == 0):
			numbers.remove(num)

print len(results)


fast = 1
slow = 1000
i = 0

while slow > fast:
	slow = 2 * slow * 0.6
	fast = 2 * fast * 0.7
	i += 1
	print i, slow, fast
	
print i, slow, fast, 

