import sys
from antlr4 import *
from spiceLexer import spiceLexer
from spiceParser import spiceParser
from spiceExtractor import spiceExtractor

import sys
sys.path+=['../']

from datastructure import Circuit,Branch,Component
 
def run_parser(file_to_parse):

	#Init lexer/parser

	input = FileStream(file_to_parse)
	lexer = spiceLexer(input)
	stream = CommonTokenStream(lexer)
	parser = spiceParser(stream)
	tree = parser.netlist()

	#FIXME GET SYNTAX ERRORS??

	#Init Walker+Listener and invocate walker

	walker=ParseTreeWalker()

	raw_circuit=Circuit()
	extractor=spiceExtractor(raw_circuit)
	walker.walk(extractor,tree)

	#Raw circuit structure populated

	Circuit.removeBadBranches(raw_circuit)
	Circuit.fixNodes(raw_circuit)
	raw_circuit.updNodeCnt()
	
	#print(raw_circuit)
	return raw_circuit
