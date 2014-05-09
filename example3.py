class Rectangle:

	def __init__(self, w, h):
		self.width = w
		self.height = h

	def area(self):
		return self.width * self.height

	def perimeter(self):
		return (2 * self.width) + (2 * self.height)

	def position(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return str(self.width) + " x " + str(self.height)

	def printLocation(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"

class Square(Rectangle):
	
	def __init__(self, s):
		self.width = s
		self.height = s


rects = list()
squares = list()

for i in range(10):
	rects.append(Rectangle(i, i + 2))
	squares.append(Square(i))

maxArea = (0, None)
for j in range(len(rects)):
	if rects[j].area() > maxArea[0]:
		maxArea = (rects[j].area(), rects[j])

for k in range(len(squares)):
	if squares[j].area() > maxArea[0]:
		maxArea = (squares[j].area(), squares[j])

allRects = list()
allRects.extend(rects)
allRects.extend(squares)

count = 10
for r in range(len(allRects)):
	count += r
	allRects[r].position(count % (r + 1), count % 5)
	print allRects[r].printLocation()

print "Max area rectangle:"
print str(maxArea[1]) + " Area: " + str(maxArea[0])
