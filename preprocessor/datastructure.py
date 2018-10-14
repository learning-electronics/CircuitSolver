#Circuit class assumes that there is always a alternative branch when removing dummy branches

#A Circuit contains a list of Branch and the Branch count.
#A Branch contains a list of two nodes and a Component.
#A Component contains a name, value, impedance (if freq >0Hz), type and an optional dependent Component

import math

class Circuit:
	def __init__(self):
		self.nodeCnt=0 
		self.branches=list()

	def __repr__(self):
		st="Circuit with "+str(self.nodeCnt)+" nodes.\n"
		for b in self.branches:
			st+="	"+str(b).replace("\n","\n	")+"\n\n"
		return st

	#Refreshes the value of self.nodeCnt
	def updNodeCnt(self):
		_mp=set()
		for _br in self.branches:
			_gn=_br.getNodes()
			_mp.add(_gn[0])
			_mp.add(_gn[1])
		self.nodeCnt=len(_mp)
		return self.nodeCnt

	#Adds the Branch 'br' to the Branch list
	def addBranch(self,br):
		#FIXME assert already in?
		self.branches.append(br)

	#Get the Branch list with component name 'cname'
	def getBranchCompName(self,cname):
		l=list(filter(lambda x: x.getComponent().getName()==cname,self.branches))

		assert len(l)<2,"One component is in two branches!"

		return l[0] if len(l)==1 else None
	
	#Get the Branch list with nodes (start end) 'nds'
	def getBranchesNodes(self,nds):
		return list(filter(lambda x: (x.node1==nds[0] and x.node2==nds[1]) or (x.node1==nds[1] and x.node2==nds[0]),self.branches))

	#Get the Branch list that connect to node 'nd'
	def getBranchesNode(self,nd):
		return list(filter(lambda x: x.node1==nd or x.node2==nd,self.branches)) 

	#Get the Branch list that contain a tension source (dependent or not)
	def getBranchesWithVS(self):
		return list(filter(lambda x: x.comp.ctype == 'V' or x.comp.ctype == 'VCVS' or x.comp.ctype == 'CCVS', self.branches))

	#Get the Branch list whose Component depends on another Component
	def getBranchesWithDep(self):
		return list(filter(lambda x: x.comp.ctype == 'VCCS' or x.comp.ctype == 'CCCS' or x.comp.ctype == 'VCVS' or x.comp.ctype == 'CCVS', self.branches))

	#Renames the node number 'nold' to 'nnew' on all branches
	def renameNode(self,nnew,nold):
		for _br in self.branches:
			_nds=list(_br.getNodes())
			if _nds[0]==nold:
				_nds[0]=nnew
			elif _nds[1]==nold:
				_nds[1]=nnew
			_br.setNodes(tuple(_nds))

	#Moves Dependency from one Branch 'brold' to another 'brnew'
	def changedep(self,brnew,brold):
		for _br in self.branches:
			if _br.getComponent().dependent!=None and _br.getComponent().dependent.getNodes()==brold.getNodes():
				_br.getComponent().dependent=brnew

	#Returns the best alternative branch to read the current
	def smartAltBranch(self,nds):
		
		for target in ['I','R','V']:

			#First search for one direction, then the other one
			for startnode in range(2):
				_brs=self.getBranchesNode(nds[startnode])
				if(len(_brs)!=2):
					continue

				if _brs[0].getNodes()==nds:
					lastbr=_brs[0]
					checkthisbr=_brs[1]
				else:
					checkthisbr=_brs[0]
					lastbr=_brs[1]


				while True:
					if checkthisbr.getNodes()==nds:
						break
		
					if checkthisbr.getComponent().ctype==target:
						return checkthisbr 

					for nextnode in range(2):
						found_next_hop=False
						_brs=self.getBranchesNode(checkthisbr.getNodes()[nextnode])
						if(len(_brs)==2):
							if _brs[0].getNodes()!=checkthisbr.getNodes() and _brs[0].getNodes()!=lastbr.getNodes():
								lastbr=checkthisbr
								checkthisbr=_brs[0]
								found_next_hop=True
								break
							elif _brs[1].getNodes()!=checkthisbr.getNodes() and _brs[1].getNodes()!=lastbr.getNodes():
								lastbr=checkthisbr
								checkthisbr=_brs[1]
								found_next_hop=True
								break

					if found_next_hop:
						continue
					else:
						break

		assert False, "No alternative branch"

	#Removes all 0V Voltage sources, 0Ohm Resistors and 0H Inductors used for current measurement
	def removeBadBranches(circ):
		done=False
		while not done: #For every change, force the algorithm to traverse the circuit again
			done=True
			for _br in circ.branches:
				_comp=_br.getComponent()
				if _comp.value==0 and (_comp.ctype=='V' or _comp.ctype=='R' or _comp.ctype=='L'):
					if len(circ.getBranchesNodes(_br.getNodes()))>1: #another components in paralel
						circ.branches.remove(_br) #Simply remove dummy branch
					else: 
						_nds=_br.getNodes()
						_alternative=circ.smartAltBranch(_nds)
						circ.changedep(_alternative,_br)
						if _nds[1]==0: #Rename nodes/branches
							circ.renameNode(_nds[1],_nds[0])
						else:
							circ.renameNode(_nds[0],_nds[1])	
						circ.branches.remove(_br) #Remove branch/component

					done=False
					break
				
					
		
	#Makes nodes number sequencial
	def fixNodes(circ):
		_mp=set()
		#Get all node numbers
		for _br in circ.branches:
			_gn=_br.getNodes()
			_mp.add(_gn[0])
			_mp.add(_gn[1])

		#Remove node 0
		_mp.remove(0)

		#Get list
		_nlst=list(_mp)
		
		#Fix node numbers
		for _br in circ.branches:
			_gn=_br.getNodes()	

			_nnn=[0,0]

			try:
				_nnn[0]=_nlst.index(_gn[0])+1
			except ValueError:
				pass
			
			try:
				_nnn[1]=_nlst.index(_gn[1])+1
			except ValueError:
				pass

			_br.setNodes(tuple(_nnn))

		return circ #redundant return
		
	#Calculates the impedances for all the Components of the circuit on the frequency (in Hz) 'freq'
	def calcImpedances(self,freq):
		for br in self.branches:
			br.comp.calcImpedance(freq)

class Branch:
	def __init__(self,n1,n2,comp):
		self.node1=n1 #int
		self.node2=n2 #int
		self.comp=comp #Component()	

	def __repr__(self):
		st="Branch: Node1: "+str(self.node1)+" Node2: "+str(self.node2)+"\n"+str(self.comp).replace("\n","\n	")
		return st

	#Returns the nodes of this Branch
	def getNodes(self):
		return (self.node1,self.node2)

	#Returns the component of this Branch
	def getComponent(self):
		return self.comp

	#Sets the nodes of this Branch
	def setNodes(self,ns):
		self.node1=ns[0]
		self.node2=ns[1]

class Component:
	def __init__(self,nm,vl,ct,dep=None):
		self.name=nm  #str()
		self.ctype=ct #str()
		self.value=float(vl) #float() # ?
		self.impedance=complex()
		self.dependent=dep #Branch()

	def __repr__(self):
		_dep=str(self.dependent).replace("\n","\n   ")
		return "Component:\nName: "+self.name+"\nType: "+self.ctype+"\nValue: "+str(self.value)+ "\nDependency: "+("\n" if _dep!="None" else "")+ _dep

	#Returns the name of the Component
	def getName(self):
		return self.name

	#Calculates the impedance for the Component on the frequency in Hz 'freq'
	def calcImpedance(self,freq):
		if self.ctype=='R':
			self.impedance=complex(self.value)		
		elif self.ctype=='C':
			if freq!=0:
				self.impedance=1.0/(1j*2.0*math.pi*freq*self.value)
			else:
				self.impedance=complex('Inf')
		elif self.ctype=='L':
			self.impedance=1j*2.0*math.pi*freq*self.value
		else:
			self.impedance=None #Power sources

	#Converts a given value to the International System, given its scale
	def convertSI(value,unit):
		if len(unit)==1 or unit==None or unit=='':
			pass
		elif unit[0]=='F':
			value*=1e-15
		elif unit[0]=='P':
			value*=1e-12
		elif unit[0]=='N':
			value*=1e-9
		elif unit[0]=='U':
			value*=1e-6
		elif unit[0:3]=='MIL':
			value*=25.4e-6
		elif unit[0]=='M' or unit[0]=='C':
			value*=1e-3
		elif unit[0]=='K':
			value*=1e3
		elif unit[0]=='MEG':
			value*=1e6
		elif unit[0]=='G':
			value*=1e9
		elif unit[0]=='T':
			value*=1e12

		return value
