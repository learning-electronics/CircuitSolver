import sys
sys.path.insert(0, '..')
sys.path.insert(0, '../mna')
from datastructure import Circuit,Branch,Component
from mnaModule_AC import mna


c = Circuit()


##CIRCUITO 1
f=5e3#Hz
b1 = Branch(1,0,Component('V1',5.0,'V'))
zC=1.0/(1j*2.0*3.1415*f*200e-9)
b2 = Branch(1,2,Component('C1',zC,'C'))
zL=(1j*2.0*3.1415*f*10e-9)
b3 = Branch(2,0,Component('L1',zL,'L'))
c.addBranch(b1)
c.addBranch(b2)
c.addBranch(b3)
del b1,b2,b3
c.updNodeCnt()

info = mna(c)
CF = info.get('CF')
x = info.get('x')
I = info.get('I')
N = info.get('N')
M = info.get('M')
P = info.get('P')
Q = info.get('Q')
R = info.get('R')






