from os.path import abspath,realpath,relpath,dirname,join
import sys
from sympy import *

#Get project dir
project_path=dirname(realpath(__file__))

sys.path+=[join(project_path,'../')]
from datastructure import Circuit,Branch,Component


sys.path+=[join(project_path,'../parser/')]
from spiceProcessor import run_parser

sys.path+=[join(project_path,'../mna/')]
from mnaModule import mna
from randSol import randomWrongs

circ=run_parser(abspath('example1.cir'))
circ.calcImpedances(0)
print(mna(circ)['x'])



circ.getBranchCompName('R1').getComponent().value*=symbols('x')*20
circ.getBranchCompName('V1').getComponent().value*=symbols('y')
circ.calcImpedances(0)
print(mna(circ)['x'].subs(symbols('x'),1/20).subs(symbols('y'),1))
print('',mna(circ))

