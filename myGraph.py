# For directed graph nodes with edges with integer weights
class Node:
	def __init__(self, id, name):
		self.id = id
		self.name = name
		self.outgoingEdges = {}
		return

	def insertNeighbor(self, neighborNodeID, weight):
		self.outgoingEdges[neighborNodeID] = weight
		return