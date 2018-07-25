import sys
sys.path+=['../']
from datastructure import Circuit,Branch,Component

def get_power_elem(circ,mnao,elem):
	return get_tension_elem(circ,mnao,elem)*get_current_elem(circ,mnao,elem)

def get_current_elem(circ,mnao,elem):
	raise NotImplementedError

def get_tension_node(circ,mnao,noden):
	if noden==0:
		return 0
	elif noden>=circ.nodeCnt:
		assert False, 'Non existent node'
	return mnao['x'][noden-1][0]

def get_tension_elem(circ,mnao,elem):
	br=circ.getBranchCompName(elem)
	assert br!=None,'Element '+elem+' does not exist'
	nodes=br.getNodes()
	#print(nodes)
	return get_tension_node(circ,mnao,nodes[0])-get_tension_node(circ,mnao,nodes[1])

def get_solution(circ,mnao,elem,questtype):
	if questtype=='V':
		correct_answer=get_tension_elem(circ,mnao,elem)
	elif questtype=='I':
		correct_answer=get_current_elem(circ,mnao,elem)
	elif questtype=='P':
		correct_answer=get_power_elem(circ,mnao,elem)
	else:
		assert False,'Question type unknown'
	return correct_answer
