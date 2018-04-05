import sys
from NetworkGraph import *

def readMatrixCoveringFile(filename):
	f = open(filename)

	f.close()

# takes in a networkGraph, which vertices are comprised of electrical/optical switches, not endpoints.
# Each node should indicate whether if it is an optical switch or not
# Communication demand matrix must be n-by-n
def routeOpticalDomain(networkGraph, communicationDemand):
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
					maxi = i
					maxj = j


	return

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
	opticalSwitchOffset = 2 * nElecSwitches
	# now make all the optical switches and their ports
	for opticalID in opticalSwitchSet.keys():
		portCnt = 0
		realOpticalSwitchIDinGraph = (opticalSwitchOffset + opticalID) * radix
		inportNodes = {}
		outportNodes = {}
		for i, j in opticalSwitchSet[opticalID]:
			
			srcNode = networkGraph.getNodeByName("src%d" % i)
			dstNode = networkGraph.getNodeByName("dst%d" % j)
			inportNode = NetworkNode(realOpticalSwitchIDinGraph)
			srcNode.addNeighbor()
			portCnt += 1

	# optical switches start from id = nElecSwitches
	

	return networkGraph


# Performs DFS on graph to find all paths from src to dst in graph within distLimit
def route(src, dst, distLimit, graph):
	# perform dfs on graph
	graphSize = graph.numVertices
	stack = []
	paths = []
	distance = [sys.maxsize] * graphSize
	visited = [False] * graphSize
	distance[src.getID()] = 0
	parent = [None] * graphSize
	stack.append(src)
	while len(stack) > 0:
		currNode = stack.pop()
		neighbors = currNode.getNeighborsList()
		for neighbor in neighbors:
			
			if distance[neighbor.getID()] > (distance[currNode.getID()] + 1):
				distance[neighbor.getID()] = (distance[currNode.getID()] + 1)
				parent[neighbor.getID()] = currNode

			# check if our neighbor is the destination node
			if neighbor is dst:
				if (distance[currNode.getID()] + 1) <= distLimit:
					path = []
					tmpCurrNode = currNode
					tmpParent = parent[currNode.getID()]
					path.append()
					while tmpParent is not src:
						path.append(tmpParent)
						tmpCurrNode = tmpParent
						tmpParent = parent[tmpCurrNode.getID()]
					path.append(src)				
					path.reverse() # reverse
					paths.append(path)
			else:
				if not visited[neighbor.getID()]:
					stack.append(neighbor)
					parent[neighbor.getID()] = currNode
		visited[currNode.getID()] = True
	return paths