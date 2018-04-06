import sys
import math
from NetworkGraph import *

def readMatrixCoveringFile(filename):
	coverMatrix = []
	f = open(filename)

	f.close()
	return coverMatrix

def readCommunicationDemandMatrix(filename):
	f = open(filename, 'r')
	matrix = []
	matrixSize = 0
	lines = f.readlines()
	firstRow = True
	for line in lines:
		if firstRow:
			firstRow = False
			matrixSize = int(line)
		else:
			line = line.split()
			matrix.append(line.split()) 
	f.close()
	return matrix

	
# Finds the maximum entry, row and column of the maximum in the matrix
def findMaxInMatrix(matrix):
	maxTmp = -1
	i = 0
	j = 0
	maxi = 0
	maxj = 0
	for line in matrix:
		for entry in line:
			if maxTmp < entry:
				maxTmp = entry
				maxi = i
				maxj = j
			j += 1
		i += 1
	return maxTmp, maxi, maxj



# takes in a networkGraph, which vertices are comprised of electrical/optical switches, not endpoints.
# Each node should indicate whether if it is an optical switch or not
# Communication demand matrix must be n-by-n
def urgencyFactorBasedRouting(networkGraph, communicationDemand):
	matrixSize = len(communicationDemand)
	urgencyFactorMatrix = [0] * matrixSize
	stop = False
	while not stop:
		maxUrgency = -1
		maxi = 0
		maxj = 0
		for i in range(matrixSize):
			for j in range(matrixSize):
				if urgencyMatrix[i][j] > maxUrgency:
					# maxi = i
					# maxj = j
	return

# fcfs means first-come-first-serve
def fcfsBasedRouting(networkGraph, communicationDemand):
	matrixSize = len(communicationDemand)
	flowSatisfied = [0] * matrixSize
	for i in range(matrixSize):
		flowSatisfied[i] = [0] * matrixSize
		srcNode = networkGraph.getNodeByName("src%d" % i)
		for j in range(matrixSize):
			dstNode = networkGraph.getNodeByName("dst%d" % j)
			cannotSatisfy = False
			while not cannotSatisfy and flowSatisfied[i][j] < communicationDemand[i][j]:
				paths = route(srcNode, dstNode, 3, networkGraph)
				if len(paths) > 0:
					offset = 0
					for pathNode in paths[0]:
						if pathNode.getName()[:2] == "os":
							outport = paths[0][offset + 1]
							assert(pathNode.deleteEdge(outport))
							break
						offset += 1
					flowSatisfied[i][j] += 1
				else:
					cannotSatisfy = True
	sum1 = 0
	sum2 = 0
	for i in range(matrixSize):
		for j in range(matrixSize):
			sum1 += flowSatisfied[i][j]
			sum2 += communicationDemand[i][j]
	return float(sum1)/float(sum2)


def generateNetworkTopology(coverMatrix):
	networkGraph = NetworkGraph()
	nElecSwitches = len(coverMatrix)
	
	# Now first generate all the electrical switches (groups in flexfly context)
	for i in range(nElecSwitches):
		networkNodeSrc = NetworkNode(i, False) # not optical switches, hence false
		networkNodeSrc.addName("src%d"%i)
		networkGraph.addNode(networkNodeSrc)
		networkNodeDst = NetworkNode((nElecSwitches + i), False)
		networkNodeDst.addName("dst%d"%i)
		networkGraph.addNode(networkNodeDst)

	# now find how many optical switches are there
	opticalSwitchSet = {}
	for row in range(len(coverMatrix)):
		for col in range(len(coverMatrix)):
			for opticalSwitchID in coverMatrix[row][col]:
				if opticalSwitchID not in opticalSwitchSet.keys():
					opticalSwitchSet[opticalSwitchID] = []
				opticalSwitchSet[opticalSwitchID].append((row,col))
	
	# calculate the offset for optical switches
	opticalSwitchOffset = int(2 * nElecSwitches)
	# now make all the optical switches and their ports
	radix = math.sqrt(len(opticalSwitchSet[0]))
	for opticalID in opticalSwitchSet.keys():
		inportCnt = 0
		outportCnt = 0
		inportToSrcNode = {} # maps input switchid to the inport id of this optical switch
		outportToDstNode = {}
		for i, j in opticalSwitchSet[opticalID]:
			if i not in inportToSrcNode.keys():
				inportToSrcNode[i] = inportCnt
				inportNode = NetworkNode(opticalSwitchOffset + inportCnt, True)
				inportNode.addName("os%d-inport%d" % (opticalID, inportCnt))
				(networkGraph.getNodeByName("src%d"%i)).addNeighbor(inportNode)
				networkGraph.addNode(inportNode)
				inportCnt += 1
			if j not in outportToDstNode.keys():
				outportToDstNode[j] = outportCnt
				outportNode = NetworkNode(opticalSwitchOffset + radix + outportCnt, True)
				outportNode.addName("os%d-outport%d" % (opticalID, outportCnt))
				outportNode.addNeighbor(networkGraph.getNodeByName("dst%d"%j))
				networkGraph.addNode(outportNode)
				outportCnt += 1 
		assert(outportCnt == inportCnt)
		# Finally form all to all connection between the inport nodes and outport nodes within this optical switch
		for inport in range(inportCnt):
			inportNode = networkGraph.getNodeByName("os%d-inport%d" % (opticalID, inport))
			for outport in range(outportCnt):
				outportNode = networkGraph.getNodeByName("os%d-outport%d" % (opticalID, outport))
				inportNode.addNeighbor(outportNode)
		opticalSwitchOffset += (outportCnt + inportCnt)
	return networkGraph


# Performs DFS on graph to find all paths from src to dst in graph within distLimit
def route(src, dst, distLimit, graph):
	# perform dfs on graph
	assert(src is not None and dst is not None)
	graphSize = graph.numVertices()
	stack = []
	paths = []
	distance = [int(sys.maxsize)] * graphSize
	visited = [False] * graphSize
	distance[src.getID()] = 0
	parent = [None] * graphSize
	stack.append(src)
	while len(stack) > 0:
		currNode = stack.pop()
		neighbors = currNode.getNeighborsList()
		visited[currNode.getID()] = True
		for neighbor in neighbors:
			
			if distance[neighbor.getID()] > (distance[currNode.getID()] + 1):
				distance[neighbor.getID()] = (distance[currNode.getID()] + 1)
				

			# check if our neighbor is the destination node
			if neighbor is dst:
				parent[dst.getID()] = currNode
				if (distance[currNode.getID()] + 1) <= distLimit:
					path = []

					tmpCurrNode = currNode
					tmpParent = parent[currNode.getID()]
					path.append(neighbor)
					while tmpCurrNode is not src:
						path.append(tmpCurrNode)
						tmpCurrNode = tmpParent
						tmpParent = parent[tmpCurrNode.getID()]
					path.append(src)				
					path.reverse() # reverse
					paths.append(path)
			else:
				if not visited[neighbor.getID()]:
					parent[neighbor.getID()] = currNode
					stack.append(neighbor)
					#parent[neighbor.getID()] = currNode
		
	return paths

def printTopology(networkGraph):
	for node in networkGraph.nodesCollection:
		print "Current node is: " + node.getName()
		i = 0
		for neighbor in node.getNeighborsList():
			print("neighbor %d" % i)


# The first testing method for this routing function
def test1():
	coverMatrix = [[[0,1],[0,1],[0,1]],[[0,1],[0,1],[0,1]],[[0,1],[0,1],[0,1]]]
	commRequirement = [[0, 1, 1],[1, 0, 1],[1, 1, 0]]
	commRequirement = [[0, 2, 0],[0, 0, 2],[2, 0, 0]]
	graph = generateNetworkTopology(coverMatrix)
	routingYield = fcfsBasedRouting(graph, commRequirement)
	print "The yield for fcfs routing is: %f" % routingYield


print "Entering routeOpticalNetwork code"
test1()
print "Exited Cleanly"