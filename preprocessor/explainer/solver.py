from explainer import *

#This method returns the absolute value of the voltage in a branch
# @branch: branch whose voltage is wanted
# @beginningNode: the voltage will be given by V_begginingNode-V_endingNode
# @mnaVector: vector of nodal voltages given by the MNA algorithm
def voltageInBranch_value(branch,beginningNode,mnaVector):
	if branch.node1==beginningNode:
		endingNode=branch.node2
	else:
		endingNode=branch.node1
	if endingNode!=0 and beginningNode!=0:
		return mnaVector[beginningNode-1]-mnaVector[endingNode-1]
	elif beginningNode==0:
		return -mnaVector[endingNode-1]
	else:
		print(mnaVector)
		return mnaVector[beginningNode-1]

#This method returns the absolute value of the current in a branch 
# @circuit: the circuit 
# @branch: branch whose current is wanted 
# @beginningNode: the current flowing from the beginning to the ending node 
# @mnaVector: vector of nodal voltages given by the MNA algorithm 
def currentInBranch_value(circuit,branch,beginningNode,mnaVector): 
	if branch.comp.ctype=='R' or branch.comp.ctype=='C' or branch.comp.ctype=='L': #FIXME quick  fix
		return currentInResistor_value(branch,beginningNode,mnaVector) 
	elif branch.comp.ctype=='I' or branch.comp.ctype=='CCCS' or branch.comp.ctype=='VCCS': 
		return currentInCS_value(circuit,branch,beginningNode,mnaVector) 
	return currentInVS_value(circuit,branch,beginningNode,mnaVector) 
 

#Auxiliary method for the current in branch 
def currentInVS_value(circuit, branch, beginningNode,mnaVector): 
	if branch.node1==beginningNode: 
		endingNode=branch.node2 
	else: 
		endingNode=branch.node1 
 
	nds_beg,brs_beg = nonVSbranchesConnectedToBranchThroughNode(circuit, branch, beginningNode) 
	nds_end,brs_end = nonVSbranchesConnectedToBranchThroughNode(circuit, branch, endingNode) 
 
	if brs_beg==None and brs_end==None: 
		return 'ERROR: IMPOSSIBILITY TO EVALUATE CURRENT IN BRANCH '+str(branch.getNodes()) 
	if brs_beg==None or (brs_beg!=None and brs_end!=None and len(brs_end)>len(brs_beg)): 
		nds=nds_end 
		brs=brs_end 
		invert=False 
	else: 
		nds = nds_beg 
		brs = brs_beg 
		invert=True 
 
	res=0 
	for i in range(len(brs)): 
		res += currentInBranch_value(circuit, brs[i], nds[i],mnaVector) 
	if invert: 
		res *= -1 
	return res 
 

#Auxiliary method for the current in branch 
def currentInCS_value(circuit,branch, beginningNode,mnaVector): 
	if branch.comp.ctype=='I': 
		val=branch.comp.value 
	elif branch.comp.ctype=='CCCS': 
		val=branch.comp.value*currentInBranch_value(circuit,branch.comp.dependent,branch.comp.dependent.node1,mnaVector) 
	else:#vccs 
		val=branch.comp.value*voltageInBranch_value(branch.comp.dependent,branch.comp.dependent.node1,mnaVector) 
	if branch.node1 == beginningNode: 
		return val 

#Auxiliary method for the current in branch 
def currentInResistor_value(branch,beginningNode,mnaVector): 
	resistor=branch.comp.impedance 
	return voltageInBranch_value(branch,beginningNode,mnaVector)/resistor 

#This method returns the absolute value of the power in a branch 
# @circuit: the circuit 
# @branch: branch whose power is wanted 
# @mnaVector: vector of nodal voltages given by the MNA algorithm 
def powerInBranch_value(circuit,branch,mnaVector): 
	if branch.comp.ctype=='R' or branch.comp.ctype=='C' or branch.comp.ctype=='L': #FIXME quick  fix 
		return powerInResistor_value(branch,mnaVector) 
	elif branch.comp.ctype=='I' or branch.comp.ctype=='CCCS' or branch.comp.ctype=='VCCS': 
		return powerInCS_value(branch,mnaVector) 
	return powerInVS_value(circuit,branch,mnaVector) 

#Auxiliary method for the power in branch
def powerInResistor_value(branch,mnaVector):
	resistor=branch.comp.impedance
	return voltageInBranch_value(branch,branch.node1,mnaVector)**2/resistor

#Auxiliary method for the power in branch
def powerInVS_value(circuit,branch,mnaVector):
	n1=branch.node1
	n2=branch.node2
	if n1!=0:
		beginningNode=n1
	else:
		beginningNode=n2
	ct=branch.comp.ctype
	if ct=='V':
		val=branch.comp.value
	elif ct=='CCVS':
		val=branch.comp.value*currentInBranch_value(circuit,branch.comp.dependent,branch.comp.dependent.node1,mnaVector)
	else: #'VCVS'
		val=branch.comp.value*voltageInBranch_value(branch.comp.dependent,branch.comp.dependent.node1,mnaVector)
	return abs(val*currentInVS_value(circuit,branch,beginningNode,mnaVector))


#Auxiliary method for the power in branch
def powerInCS_value(circuit,branch,mnaVector):
	n1 = branch.node1
	val=currentInBranch_value(circuit,branch,n1,mnaVector)
	return abs(val*voltageInBranch_value(branch,n1,mnaVector))


#This method returns a list of branches connected to another branch but that don't have any VS connected to it.
#The method is used to calculate the current going through a VS
def nonVSbranchesConnectedToBranchThroughNode(circuit,branch,node):
    if node==0:
        return None,None
    #this method returns a set of branches that are connected to @branch through @node but that aren't VS branches, so
    # that we can calculate the current in a branch with a VS
    brs=circuit.getBranchesNode(node)
    brs.remove(branch)
    beginningNodes=list()
    for i in range(len(brs)):
        beginningNodes.append(node)
    for br in brs:
        if br.comp.ctype=='V' or br.comp.ctype=='CCVS' or br.comp.ctype=='VCVS':
            beginningNodes.pop(brs.index(br))
            brs.remove(br)
            if br.node1==node:
                n=br.node2
            else:
                n=br.node1
            if n==0:
                return None,None
            (begN2,brs2)=nonVSbranchesConnectedToBranchThroughNode(circuit,br,n)
            if brs2==None:
                return None, None
            to_remove=set()
            for br2 in brs2:
                if br2 in brs:
                    beginningNodes.pop(brs.index(br2))
                    begN2.pop(brs2.index(br2))
                    to_remove.add(br2)
                else:
                    brs.append(br2)
            for bb in to_remove:
                brs.remove(bb)
            for nd in begN2:
                beginningNodes.append(nd)
    return (beginningNodes,brs)
