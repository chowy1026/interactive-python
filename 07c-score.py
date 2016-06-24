score = raw_input("Enter Score: ")
sc = float(score)

if sc < 0 or sc > 1:
	print "Value Out of Range"
elif sc >= 0.9 and sc <=1.0:
	print "Grade is", "A"
elif sc >= 0.8:
	print "Grade is", "B"
elif sc >= 0.7:
	print "Grade is", "C"
elif sc >= 0.6:
	print "Grade is", "D"
elif sc < 0.6:
	print "Grade is", "F"
