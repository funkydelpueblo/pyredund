'''
TREE TRAVERSAL FOR REPEAT FINDING
from Flouri et. al

1. Partition nodes by height.
2. Assign a unique identifier to each label in alphabet.
3. For each height level starting from 0 (the leaves).
	i) 	For each node v of the current height level construct a string 
		containing the identifier of the label of v and the identifiers
		of the subtrees that are attached to v.
	ii) For each such string, sort the identifiers within the string.
	iii) Lexicographically sort the strings (for the current height level).
	iv) Find non-overlapping subtree repeats as identical adjecent
		strings in the lexicographically sorted sequence of strings.
	v) 	Assign unique identifiers to each set of repeating subtrees 
		(equivalence class).
'''
import ast
import astpp
from Queue import PriorityQueue, Queue
import collections
import array
import helper
from helper import HeightHelper
import unparse
import filecollector
import copy
import time

''' 0. Load File '''

folderorfile = raw_input("File (F) or Directory (D)?")

if folderorfile == "D":
	dirname = raw_input("Enter input directory: ")
	timestart = time.time() # used for timing execution
	text = filecollector.master_ast(dirname)
else:
	filename = raw_input("Enter input file: ")
	timestart = time.time() # used for timing execution
	reader = open(filename, 'r')
	text = ast.parse(reader.read())
	#print astpp.dump(text)
	reader.close()

ast.fix_missing_locations(text)


''' 1. Partition Nodes By Height '''
print "1. Partition by Height."

parents = dict() #dictionary that lets us get a node's parent
heightmap = dict() #dictionary that lets us get a node's height

partition = [[]]
queue = PriorityQueue()
queue.put((1, text))
while not queue.empty():
	pop = queue.get()
	node = pop[1]
	height = pop[0]

	heightmap[node] = height

	if isinstance(node, array.array):
		for i in range(len(node)):
			queue.put((height + 1, node[i]))
			parents[node[i]] = parent[node]

	else:
		for j in ast.iter_child_nodes(node):
			queue.put((height +1, j))
			parents[j] = node

	#if len(partition) >= height:
	#	partition[height -1].append(node)
	#else:
	#	temp = [node]
	#	partition.insert(height - 1, temp)

heights = HeightHelper(text)
#print "HeightHelper: " + str(heights.countEntries())
partition = heights.getPartition()

''' 2. Assign a unique identifier to each label in alphabet. '''
print "2. Assign identifiers to alphabet"

alphaset = set()
nodecount = 0

for i in range(len(partition)):
	for j in range(len(partition[i])):
		alphaset.add(type(partition[i][j]))
		nodecount += 1

print "Running algorithm on AST of " + str(nodecount) + " nodes."

count = 0
mapping = dict()
for elem in alphaset:
	mapping[elem] = count
	count+=1

alphasize = count

K = dict()	# stores identifier for a specific subtree
allRepeats = list() # stores all repeat instances
reps = 0

print str(len(partition)) + " levels"

''' 3. For each height level starting from 0 (the leaves)... '''
print "3. For each height level, find repeats."

### FEEDBACK STUFF
totallevels = len(partition)
tenthlevels = int(totallevels / 10) + 1
levcounter = 0

for i in range(len(partition)):
	### FEEDBACK FOR LONG FILES

	if(len(partition) > 75000):
		levcounter += 1
		if levcounter % tenthlevels == 0:
			print "Working..." + str(int((float(float(levcounter) / float(totallevels)) * 100)))+ "%"

	#j = len(partition) - i - 1 #we need to reverse the ordering
	j = i

	''' i) 	For each node v of the current height level construct a string 
		containing the identifier of the label of v and the identifiers
		of the subtrees that are attached to v. '''

	heightalpha = set()
	strings = list()
	for v in range(len(partition[j])):
		node = partition[j][v]

		SV = list()
		SV.append(mapping[type(node)])

		heightalpha.add(mapping[type(node)]) #for remapping

		for c in ast.iter_child_nodes(node):
			SV.append(K[c])
			heightalpha.add(K[c]) #for remapping

		strings.append((node, SV))

	''' i.5) 	Remap the alphabet size to only the identifiers present at this level.
				This is a HUGE optimization and achieves a linear-time bucket sort.'''
	#print str(len(heightalpha)) + " vs " + str(alphasize + reps)
	countlevel = 0
	heightmapping = dict()
	for elem in heightalpha:

		heightmapping[elem] = countlevel
		countlevel += 1

	newstrings = list()
	for entry in strings:
		string = entry[1]
		newstring = list()

		for char in string:
			newchar = heightmapping[char]
			newstring.append(newchar)

		newstrings.append((entry[0], newstring))


	''' ii) For each such string, sort the identifiers within the string.''' 
	remapped = list()
	for entry in newstrings:
		string = entry[1]

		stringchars = list()
		for n in range(len(string)):
			stringchars.append(string[n])

		stringchars = sorted(stringchars)
		stringmap = dict()
		stringfing = 0
		for stringid in stringchars:
			stringmap[stringid] = stringfing
			stringfing += 1

		remap = list()
		'Bucket sort'

		buckets = [list() for _ in range( len(stringchars) + 1)]

		for i in range(len(string)):
			c = string[i]
			buck = buckets[stringmap[c]]
			buck.append(c)

		'reconstruct'
		for j in range(len(buckets)):
			for k in range(len(buckets[j])):
				remap.append(buckets[j][k])

		#remap = sorted(string)

		remapped.append((entry[0], remap))

	''' iii) Lexicographically sort the strings (for the current height level). '''
	lexisort = helper.bucketSortArrayOfListsIterative(remapped, len(heightalpha))

	'''	iv) Find non-overlapping subtree repeats as identical adjecent
		strings in the lexicographically sorted sequence of strings.
		v) 	Assign unique identifiers to each set of repeating subtrees 
		(equivalence class).'''

	reps += 1
	repeat = list()
	repeat.append(lexisort[0])
	#print "== class =="
	#print lexisort[0]
	K[lexisort[0][0]] = reps + count

	for n in range(len(lexisort) - 1):
		p = n + 1
		if lexisort[p][1] == lexisort[p - 1][1]:
			repeat.append(lexisort[p])
		else:
			reps += 1
			allRepeats.append(repeat)

			repeat = list()
			repeat.append(lexisort[p])
			#print "== class =="
		#print lexisort[p]

		#boundary case
		if p == len(lexisort) - 1:
			allRepeats.append(repeat)


		K[lexisort[p][0]] = reps + count

#for repeat in allRepeats:
#	print "~~~~~~~~~~~~~~~~~~"
#	print repeat

'''4. Remove non-maximal instances'''

banned = set()
trueRepeats = list()
for repeat in allRepeats:

	if len(repeat) > 1:
		for inst in repeat:
			node = inst[0]
			for j in ast.iter_child_nodes(node):
				banned.add(j)

for repeat in allRepeats:
	temp = list()
	for inst in repeat:
		if not inst[0] in banned:
			temp.append(inst)

	if len(temp) > 1:
		trueRepeats.append(temp)

''' 5. Final output '''
print "5. Enumerate instances."

''' i) Sort by complexity of node, i.e. total number of child nodes'''
complexsort = dict()
for repeat in trueRepeats:
	complexity = sum( 1 for _ in ast.walk(repeat[0][0])) #find better way to do this?
	if len(repeat) > 1:
		if complexity in complexsort:
			complexsort[complexity].append(repeat)
		else:
			complexsort[complexity] = [repeat]

comps = complexsort.keys()
comps = sorted(comps)

''' ii) Print out one repeat at a time, in decreasing order of complexity'''

total = 0
for entry in comps:
	total += len(complexsort[entry])

timeend = time.time()
timeelapsed = int(timeend - timestart)
elapsedmin = int(timeelapsed / 60)
elapsedsec = timeelapsed % 60

if elapsedsec < 10:
	secstring = "0" + str(elapsedsec)
else:
	secstring = str(elapsedsec)

print "Finished in " + str(elapsedmin) + ":" + secstring

print '********************'
print str(total) + " repeats found"
print '********************'

m = len(comps) - 1
pos = 0
choice = "N"
while m >= 0  and choice != "X":

	end = False
	if pos >= len(complexsort[comps[m]]):
		m -= 1
		pos = 0
		if m < 0:
			end = True

	if not end:
		repeat = complexsort[comps[m]][pos]
		print "----------------"
		print "---- REPEAT ----"
		print "----------------"
		for q in range(len(repeat)):
			node = repeat[q][0]
			parent = parents[node]
			nodestr = str(node)
			ast.fix_missing_locations(node)

			if hasattr(node, 'lineno'):
				print ""
				print "* Instance " + str(q + 1) + " @ line " + str(node.lineno) + " complexity: " + str(comps[m]) #+ " Parent: " + str(parents[node]) + " Node: " +  str(node) #+ " height: " + str(heightmap[node])
				unparse.Unparser(node)
				print ""
			else:
				print "* Instance " + str(q + 1) + ": " + node.__class__.__name__ + " (no line)"

		pos += 1

		if not folderorfile == 'A':
			choice = raw_input("See next repeat? N for next, X for exit.")

print "No more repeats."






	









