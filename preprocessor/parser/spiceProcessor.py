import sys
from antlr4 import *
from spiceLexer import spiceLexer
from spiceParser import spiceParser
from spiceExtractor import spiceExtractor

import sys
sys.path+=['../']

from datastructure import Circuit,Branch,Component
 
#The function run_parser receives the filepath to a SPICE formated circuit,
#parses it, filters malformations and fills in the datastructure
def run_parser(file_to_parse):

	#Init lexer/parser
	input = FileStream(file_to_parse)
	lexer = spiceLexer(input)
	stream = CommonTokenStream(lexer)
	parser = spiceParser(stream)
	tree = parser.netlist()

	#Raise an exception if the SPICE file is not completely accepted
	if parser.getNumberOfSyntaxErrors() != 0:
		raise Exception('The given SPICE file contains syntactic errors.')

	#Init Walker+Listener and invocate walker
	walker=ParseTreeWalker()

	raw_circuit=Circuit()
	extractor=spiceExtractor(raw_circuit)
	walker.walk(extractor,tree)

	#Raw circuit structure populated

	#Fix malformations and bad practices 
	Circuit.removeBadBranches(raw_circuit)
	Circuit.fixNodes(raw_circuit)
	raw_circuit.updNodeCnt()
	
	return raw_circuit
