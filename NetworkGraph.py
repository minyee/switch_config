class NetworkNode:
	def __init__(self, idArg, opticalSwitchOrNot):
		self.id = idArg
		self.neighbors = []
		self.opticalSwitch = opticalSwitchOrNot
		self.name = ("node %d" % self.id)
		return
	
	def addName(self, nameArg):
		self.name = nameArg

	def isOpticalSwitch(self):
		return this.opticalSwitch

	def addNeighbor(self, neighborSwitch):
		if neighborSwitch != None and neighborSwitch not in self.neighbors:
			self.neighbors.append(neighborSwitch)
		return

	def getNeighborsList(self):
		return this.neighbors

	def getID(self):
		return self.id

	def getName(self):
		return self.name

	# returns a boolean true if the neighbor is deleted, and false otherwise
	def deleteEdge(self, neighborID):
		index = 0
		for neighbor in self.neighbors:
			if neighbor.getID() == neighborID:
				self.neighbors.pop(index)
				return True
			index += 1
		return False


class NetworkGraph:
	def __init__(self):
		self.nodesCollection = []
		return

	def addNode(self, node):
		found = False
		for graphNode in self.nodesCollection:
			if graphNode is node:
				found = True
				break
		if not found:
			self.nodesCollection.append(node)
		return

	def getNodeByID(self, id):
		for graphNode in self.nodesCollection:
			if node.getID() == node.getID():
				return graphNode
		return None

	def getNodeByName(self, name):
		for graphNode in self.nodesCollection:
			if node.getName() == name:
				return graphNode
		return None

	def numVertices(self):
		return len(self.nodesCollection)
