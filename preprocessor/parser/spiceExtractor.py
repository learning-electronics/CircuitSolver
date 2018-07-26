from spiceParser import spiceParser
from spiceListener import spiceListener

import sys
sys.path+=['../']

from datastructure import Circuit,Branch,Component

class spiceExtractor(spiceListener):

	def __init__(self,cir):
		self.circ=cir

	# Enter a parse tree produced by spiceParser#netlist.
	def enterNetlist(self, ctx:spiceParser.NetlistContext):
		pass

	# Exit a parse tree produced by spiceParser#netlist.
	def exitNetlist(self, ctx:spiceParser.NetlistContext):
		#Fix dependencies
		for br in self.circ.branches:
			if br.getComponent().dependent!=None:
				if len(br.getComponent().dependent.getNodes())<1:
					assert False,"Inconsistent Netlist, at least one dependency is not met"
				br.getComponent().dependent=self.circ.getBranchesNodes(br.getComponent().dependent.getNodes())[0]

	# Enter a parse tree produced by spiceParser#title.
	def enterTitle(self, ctx:spiceParser.TitleContext):
		pass

	# Exit a parse tree produced by spiceParser#title.
	def exitTitle(self, ctx:spiceParser.TitleContext):
		pass


	# Enter a parse tree produced by spiceParser#element.
	def enterElement(self, ctx:spiceParser.ElementContext):
		pass

	# Exit a parse tree produced by spiceParser#element.
	def exitElement(self, ctx:spiceParser.ElementContext):

		#Check dependencies:
		if ctx.sn!=None: #nodes dependency (tension)
			_gb=self.circ.getBranchesNodes((int(ctx.sn.n1.text),int(ctx.sn.n2.text)))	
			assert len(_gb)>0,"Branch ("+ctx.sn.n1.text+","+ctx.sn.n2.text+") does not exist"

			_dep=Branch(int(ctx.sn.n1.text),int(ctx.sn.n2.text),None)
		elif ctx.cd!=None: #component dependency (current)
			_tmp=self.circ.getBranchCompName(ctx.cd.text)
			assert _tmp!=None,"Component "+ctx.cd.text+" does not exist"
			_dep=Branch(_tmp.getNodes()[0],_tmp.getNodes()[1],None)

		else:
			_dep=None

		_val=list()
		if ctx.value!=None:
			for _i in ctx.value.text:
				if str(_i).isdigit() or _i=='.':
					_val.append(_i)
				else:
					break 
			_val="".join(_val)
		else:
			_val=0

		_scale=ctx.value.text.split(_val)[1] if ctx.value!=None else ""

		_val=float(_val)

		if ctx.name.text[0]=='E':
			_comp='VCVS'
		elif ctx.name.text[0]=='F':
			_comp='CCCS'
		elif ctx.name.text[0]=='G':
			_comp='VCCS'
		elif ctx.name.text[0]=='H':
			_comp='CCVS'
		else:
			_comp=ctx.name.text[0]

		#Create a Component
		_c=Component(ctx.name.text,Component.convertSI(_val,_scale),_comp,_dep) #Check ctype, value, scale

		#Place inside branch
		_b=Branch(int(ctx.nodes(0).n1.text),int(ctx.nodes(0).n2.text),_c)

		#Add branch to circuit
		self.circ.addBranch(_b)


	# Enter a parse tree produced by spiceParser#nodes.
	def enterNodes(self, ctx:spiceParser.NodesContext):
		pass

	# Exit a parse tree produced by spiceParser#nodes.
	def exitNodes(self, ctx:spiceParser.NodesContext):
		pass


