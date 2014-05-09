from Queue import Queue
import ast
import array
import copy

class HeightHelper:

	partition = [[]]

	def __init__(self, root):
		#self.heights = dict()
		self.heights = list()
		self.seen = dict()
		self.getHeight(root)

	def getHeight(self, node):
		if node in self.seen:
			#print 'AAAAAHHHHH'
			return self.seen[node]
			#return self.heights[node]

		maximum = 0
		if isinstance(node, array.array):
			for l in range(len(node)):
				test = self.getHeight(node[l])
				if test > maximum:
					maximum = test 
		else:
			count = 0
			for v in ast.iter_child_nodes(node):
				count += 1
				test = self.getHeight(v)
				if test > maximum:
					maximum = test 

			#if count == 0:
			#	print "LEAF: " + str(node)

		#self.heights[node] = maximum + 1
		height = maximum + 1
		self.heights.append((node, height))
		self.seen[node] = height

		if len(HeightHelper.partition) >= height:
			HeightHelper.partition[height -1].append(node)
		else:
			temp = [node]
			HeightHelper.partition.insert(height - 1, temp)

		return height

	def countEntries(self):
		return len(self.heights)

	def getNodeMap(self):
		return self.heights

	def getPartition(self):
		return HeightHelper.partition


def bucketSortArrayOfLists(A, alpha, ind):
	buckets = [list() for _ in range(alpha + 1)]

	for i in range(len(A)):
		if len(A[i][1]) > ind:
			c = A[i][1][ind]
		else:
			c = alpha

		buck = buckets[c]
		buck.append(A[i])

	result = list()
	for j in range(len(buckets)):
		buck = buckets[j]
		if len(buck) > 0:

			# See if bucket contains only completely identical lists
			compare = buck[0]
			same = True
			for k in range(len(buck)):
				same = same and buck[k][1] == compare[1]

			if not same:
				buck = bucketSortArrayOfLists(buck, alpha, ind + 1)

		for n in range(len(buck)):
			result.append(buck[n])

	return result

def bucketSortArrayOfListsIterative(A, alpha):
	result = copy.copy(A)
	outstanding = Queue()
	outstanding.put((0, len(result) - 1, 0))

	while not outstanding.empty():
		buckets = [list() for _ in range(alpha + 1)]
		pop = outstanding.get()

		i = pop[0]
		while i <= pop[1]:

			if len(result[i][1]) > pop[2]:
				c = result[i][1][pop[2]]
			else:
				c = alpha

			buck = buckets[c]
			buck.append(result[i])

			i += 1


		fing = pop[0]
		for j in range(len(buckets)):
			buck = buckets[j]
			#print buck
			if len(buck) > 0:
				#See if bucket contains only completely identical lists
				compare = buck[0]
				same = True
				for k in range(len(buck)):
					same = same and buck[k][1] == compare[1]

				if not same:
					#We must check for different sized lists or we end
					#up in an infinite loop

					samelen = True
					alen = len(buck[0][1])
					maxlen = 0
					for n in range(len(buck)):
						samelen = samelen and alen == len(buck[n][1])
						maxlen = max(maxlen, len(buck[n][1]))

					if samelen:
						outstanding.put((fing, fing + len(buck) - 1, pop[2] + 1))
					else:
						#Partition into buckets based on size
						numbucks = [list() for _ in range(maxlen)]

						for v in buck:
							numbucks[len(v[1]) - 1].append(v)

						f2 = fing
						for b in numbucks:

							if len(b) > 0:
								sameb = True
								compareb = b[0]

								for m in range(len(b)):
									sameb = sameb and b[m][1] == compareb[1]

								if not same:
									if not (f2 == pop[0] and f2 + len(b) - 1 == pop[1]):
										outstanding.put((f2, f2 + len(b) - 1, pop[2] + 1)) #should this be pop[2] + 1?
									f2 += len(b)

				for n in range(len(buck)):
					result[fing] = buck[n]
					fing += 1

	return result

def test():
	tester = [(0, [4, 8, 6]), (1, [4, 7, 6]), (2, [7, 7, 7]), (3, [7, 7]),
	 (4, [7, 7, 7, 7]), (5, [5]), (6, [2, 3])]
	result = bucketSortArrayOfListsIterative(tester, 8)
	print result
