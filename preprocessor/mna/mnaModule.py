import numpy
## Third Version of Modified Nodal Analysis Algorithm Implementation
##
#Major changes: now current dependencies are no longer made from currents in
#voltage sources

#------------------------------------
#IMPORTANT ASSUMPTIONS ON THIS VERSION:
#-each branch only has one component
#-the nodes are consecutive starting on 0
#-current dependencies are made on branches containing a resistor or a
#independent current source
#------------------------------------ 

# Args in:
#   circuit - it's an object of the Circuit class, which has all necessary 
# information about the circuit on which we will operate 
#
# Returns:
#   x - vector containing the voltages in each given node followed by the 
# currents in each of the voltage sources in their order of appearance in
# the branches vector, current dependencies and voltage dependencies

 
#function [ CF,x,I, N,M,P,Q,R] = mnaV3( circuit )

def mna(circuit):

	## Definition of the system's dimensions
	# In this part we define the system dimensions, based on the number of
	# nodes, voltage sources, currents and voltages that control dependent
	# sources.

	#Obtaining the list of  branches of the circuit:
	branches=circuit.branches

	#Obtaining the number of nodes (except GND), N:
	N=circuit.nodeCnt-1


	#Obtaining the number of currents in voltage sources (independent or 
	#dependent ones), P: 
	P=0
	for b in branches:
		if b.comp.ctype=='V' or b.comp.ctype=='VCVS' or b.comp.ctype=='CCVS': 
			P=P+1

	#Obtaining the number of currents that control dependent sources, Q:
	Q=0
	for b in branches:
		if b.comp.ctype=='CCVS' or b.comp.ctype=='CCCS': 
			Q=Q+1

	#Obtaining the number of voltages that control dependent sources, R:
	R=0
	for b in branches:
		if b.comp.ctype=='VCVS' or b.comp.ctype=='VCCS': 
			R=R+1

	#Finally, obtaining the number of variables of the system disconsidering 
	#the nodal voltages, M:
	M=P+Q+R 


	## Construction of the GR matrix
	# GR(N,N) is the conductance matrix: 
	#GR=zeros(N,N)
	GR=numpy.zeros((N,N))

	#Filling GR positions in the diagonal: 
	for i in range(N):
		for b in branches:
			if (b.node1==(i+1) or b.node2==(i+1)) and b.comp.ctype=='R':
				GR[i][i]=GR[i][i]+1/b.comp.value

	#Filling GR positions amongst nodes:
	for b in branches:
		Begin=b.node1
		End=b.node2
		if Begin!=0 and End!=0 and b.comp.ctype=='R':
			"""ALTERACAO NO MNA"""
			GR[Begin-1][End-1]=GR[Begin-1][End-1]-1/b.comp.value
			GR[End-1][Begin-1]=GR[End-1][Begin-1]-1/b.comp.value

	## Construction of the B matrix
	# B is a matrix that defines the currents through voltage sources and in
	# (voltage or current) dependent current sources 

	#B=zeros(N,M);
	B=numpy.zeros((N,M))


	#First we fill matrix B with the currents on the independent voltage
	#sources
	idx=0  #this index represents the column of matrix B in which we are working, 
			#that corresponds to the line idx+N of the variables column
	for b in branches:
		if b.comp.ctype=='V' or b.comp.ctype=='VCVS' or b.comp.ctype=='CCVS':
			Begin=b.node1
			End=b.node2
			if Begin!=0:
				B[Begin-1][idx]=1
			if End!=0:
				B[End-1][idx]=-1
			idx=idx+1

	#FIXME: shouldnt put idx = 0 here?
	#Now we add to the matrix B more parameters related to current dependent 
	#current sources
	for b in branches:
		if b.comp.ctype=='CCCS':
			Begin=b.node1
			End=b.node2
			if Begin!=0:
				B[Begin-1][idx]=b.comp.value
			if End!=0:
				B[End-1][idx]=-b.comp.value
			idx=idx+1
		
		if b.comp.ctype=='CCVS':
			idx=idx+1

	#Now we add to the matrix B more parameters related to voltage dependent
	#current sources
	for b in branches:
		if b.comp.ctype=='VCCS':
			Begin=b.node1
			End=b.node2
			if Begin!=0:
				B[Begin-1][idx]=b.comp.value
			if End!=0:
				B[End-1][idx]=-b.comp.value
			idx=idx+1
		
		if b.comp.ctype=='VCVS':
			idx=idx+1


	## Construction of the C matrix
	# C is a matrix that defines amongst which nodes are the currents and
	# voltages related to dependent sources

	#C=zeros(M,N);
	C=numpy.zeros((M,N))

	#first we fill matrix C with the currents on the voltage sources, this will
	#serve to define the voltage on the branches with VSs

	idx=0  #this index represents the line of matrix C in which we are working, 
			#that corresponds to the line idx+N of the variables column

			
	for b in branches:
		if b.comp.ctype=='V' or b.comp.ctype=='VCVS' or b.comp.ctype=='CCVS':
			Begin=b.node1
			End=b.node2
			if Begin!=0:
				C[idx][Begin-1]=1
			if End!=0:
				C[idx][End-1]=-1
			idx=idx+1

	#Now we indicate amongst which nodes are the currents in the dependencies
	#we skip the idxs corresponding to the current dependencies that are not
	#dependencies based on currents in resistors.


	for b in branches:
		if b.comp.ctype=='CCVS' or b.comp.ctype=='CCCS': 
			if b.comp.dependent.comp.ctype=='R':
				Begin=b.comp.dependent.node1
				End=b.comp.dependent.node2
				if Begin!=0:
					C[idx][Begin-1]=1
				if End!=0:
					C[idx][End-1]=-1
			idx=idx+1

	#Finally we complete the B matrix with the information that says in which
	#nodes is the voltage sampled for the voltage dependencies
	for b in branches:
		if b.comp.ctype=='VCVS' or b.comp.ctype=='VCCS': 
			Begin=b.comp.dependent.node1
			End=b.comp.dependent.node2
			if Begin!=0:
				C[idx][Begin-1]=1
			if End!=0:
				C[idx][End-1]=-1
			idx=idx+1



	## Construction of the D matrix
	# D is a matrix relative to voltage sources and to the dependencies of 
	# the various sources:
	#D=zeros(M,M);
	D=numpy.zeros((M,M))

	idx=0  #this index represents the line of matrix D in which we are working, 
			#that corresponds to the line idx+N of the variables column

	#Firstly we set a line of zeros (skip the idx) for the lines that correspond 
	#currents on independent voltage sources:

	for b in branches:
		if b.comp.ctype=='V':
			idx=idx+1
		elif b.comp.ctype=='VCVS':
			idx2=P+Q
			
			for bb in branches:
				if bb.comp.ctype=='VCVS' or bb.comp.ctype=='VCCS': 
					if bb.comp.name==b.comp.name:
						break
					idx2=idx2+1
			
			D[idx][idx2]=-b.comp.value
			idx=idx+1
		elif b.comp.ctype=='CCVS':
			idx2=P
			
			for bb in branches:
				if bb.comp.ctype=='CCVS' or bb.comp.ctype=='CCCS': 
					if bb.comp.name==b.comp.name:
						break
					idx2=idx2+1
			
			
			D[idx][idx2]=-b.comp.value
			idx=idx+1

	#Fill on matrix D the current dependencies, if it is due to a R, we add in
	#the line of the order of that current the value -R, if it is dua to a
	#independent current source, we add the value 1:
	for b in branches:
		if b.comp.ctype=='CCVS' or b.comp.ctype=='CCCS': 
			if b.comp.dependent.comp.ctype=='R':
				D[idx][idx]=-b.comp.dependent.comp.value
			else:
				D[idx][idx]=1
			idx=idx+1	


	for b in branches:
		if b.comp.ctype=='VCVS' or b.comp.ctype=='VCCS':
			D[idx][idx]=-1
			idx=idx+1

	## Assembly of all matrices into the coefficients matrix - CF
	# CF is the final coefficient matrix, formed by GR,B,C,D in the following
	# way:
	#CF=[GR B;C D]
	CF=numpy.concatenate((numpy.concatenate((GR,B),axis=1),numpy.concatenate((C,D),axis=1)),axis=0)

	## Construction of the I matrix
	# I is the matrix of the independent terms
	#I=zeros(M+N,1);
	I=numpy.zeros((M+N,1))

	idx=N
	for b in branches:
		if b.comp.ctype=='V':
			I[idx]=b.comp.value
			idx=idx+1
		if b.comp.ctype=='VCVS' or b.comp.ctype=='CCVS':
			idx=idx+1
		if b.comp.ctype=='I':
			if b.node1>0:
				I[b.node1-1]=-b.comp.value
			if b.node2>0:
				I[b.node2-1]=b.comp.value

	idx=N+P
	for b in branches:
		if b.comp.ctype=='CCVS' or b.comp.ctype=='CCCS': 
			if b.comp.dependent.comp.ctype=='I':
				I[idx]=b.comp.dependent.comp.value
			idx=idx+1 

	## Obtaining the result

	#CF*x=I <=> x=CF^-1 * I
	#x=CF\I;


	info={}
	info['CF'] = CF
	info['x'] = numpy.array(numpy.matmul(numpy.linalg.inv(CF), I))
	info['I'] = I
	info['N'] = N
	info['M'] = M
	info['P'] = P
	info['Q'] = Q
	info['R'] = R

	return info
