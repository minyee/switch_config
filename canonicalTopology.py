# Forms the canonical topology, which is when G = r on a Flexfly
def generateCanonicalTopology(groups):
	matrix = [0] * groups
	numSwitches = groups - 1
	for i in range(groups):
		matrix[i] = [0] * groups
		for j in range(groups):
			switchCovers = []
			for k in range(numSwitches):
				switchCovers.append(k)
			matrix[i][j] = switchCovers
	return matrix

# Generates the uniform demand matrix
def generateUniformDemandMatrix(groups):
	matrix = [0] * groups
	for i in range(groups):
		row = [1] * groups
		row[i] = 0
		matrix[i] = row
	return matrix