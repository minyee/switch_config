import sys
from myGraph import *
# Keep in mind that the creation of nodes do not create the edges and weights



def readMatrix(filename):
	f = open ( filename , 'r')
	l = [ map(int,line.split()) for line in f ]
	#print l
	return l

def formNetwork(MatrixFilename, OutputAdjacencyMatrixFilename):
	linkAllocationMatrix = readMatrix(MatrixFilename)
	#print linkAllocationMatrix
	numGroups = len(linkAllocationMatrix)
	numSwitches = numGroups - 1
	nodeID = 0
	NodesCollection = {}
	NodesCollection["sourceNode"] = Node(nodeID, "sourceNode")
	nodeID += 1
	NodesCollection["sinkNode"] = Node(nodeID, "sourceNode")
	nodeID += 1

	for i in range(numGroups):
		for j in range(numGroups):
			if linkAllocationMatrix[i][j] == 0:
				continue
			srcNodeName = ("src%d->%d" % (i,j))
			srcNewNode = Node(nodeID, srcNodeName)
			nodeID += 1
			NodesCollection[srcNodeName] = srcNewNode
			NodesCollection["sourceNode"].insertNeighbor(srcNewNode, linkAllocationMatrix[i][j])

			dstNodeName = ("dst%d->%d" % (i,j))
			dstNewNode = Node(nodeID, dstNodeName)
			nodeID += 1
			dstNewNode.insertNeighbor(NodesCollection["sinkNode"], linkAllocationMatrix[i][j])
			NodesCollection[dstNodeName] = dstNewNode			#NodesCollection["sourceNode"].insertNeighbor(srcNewNode, linkAllocationMatrix[i][j])			


	for swid in range(numSwitches):
		for inport in range(numGroups):
			inportNode1 = Node(nodeID, "inport%d:switch_%d" % (inport, swid))
			nodeID += 1
			inportNode2 = Node(nodeID, "inport%d!:switch_%d" % (inport, swid))
			nodeID += 1
			NodesCollection["inport%d:switch_%d" % (inport, swid)] = inportNode1
			NodesCollection["inport%d!:switch_%d" % (inport, swid)] = inportNode2
			inportNode1.insertNeighbor(inportNode2, 1) # weight of 1

			outportNode1 = Node(nodeID, "outport%d:switch_%d" % (inport, swid))
			nodeID += 1
			outportNode2 = Node(nodeID, "outport%d!:switch_%d" % (inport, swid))
			nodeID += 1
			NodesCollection["outport%d:switch_%d" % (inport, swid)] = outportNode1
			NodesCollection["outport%d!:switch_%d" % (inport, swid)] = outportNode2
			outportNode2.insertNeighbor(outportNode1, 1) # weight of 1
		# connect all the inports to all the outports in the switch 
		for srcinport in range(numGroups):
			for dstinport in range(numGroups):
				srcportNode = NodesCollection["inport%d!:switch_%d" % (srcinport, swid)]
				dstportNode = NodesCollection["outport%d!:switch_%d" % (dstinport, swid)]
				srcportNode.insertNeighbor(dstportNode, 1)

	# Here finally connect the group Nodes to the switch inport and outport nodes 
	lastUsedPort = [0] * (numSwitches)
	for i in range(numGroups):
		for j in range(numGroups):
			if linkAllocationMatrix[i][j] == 0:
				continue
			srcNode = NodesCollection["src%d->%d" % (i,j)]
			dstNode = NodesCollection["dst%d->%d" % (i,j)]
			for swid in range(numSwitches):
				inportNode = NodesCollection["inport%d:switch_%d" % (i, swid)]
				outportNode = NodesCollection["outport%d:switch_%d" % (i, swid)]
				srcNode.insertNeighbor(inportNode, 1)
				outportNode.insertNeighbor(dstNode, 1)
		#for swid in range
		#lastUsedPort[swid] += 1 

	adjMatrix = [0] * len(NodesCollection)
	#print nodeID
	#print len(NodesCollection)
	for nodeName, node in NodesCollection.items():
		vect = [0] * len(NodesCollection)
		for targetNode, weight in node.outgoingEdges.items():
			vect[targetNode.id] = weight
		adjMatrix[node.id] = vect
	file = open(OutputAdjacencyMatrixFilename, 'wb')
	for i in range(len(NodesCollection)):
		line = ""
		for j in range(len(NodesCollection)):
			line += (str(adjMatrix[i][j]))
			if j < len(NodesCollection) - 1:
				line += ","
		line += "\n"
		file.write(line)
	file.close()
	return

filename = sys.argv[1]
formNetwork("tm.txt", "adjMatrix.txt")

