import sys
sys.path.insert(0, '..')
sys.path.insert(0, '../mna')
from datastructure import Circuit,Branch,Component
from mnaModule import mna
from circuit2na import circuit2na
from circuit2na import stepByStepNA,stepByStepExercise
c = Circuit()


 ##CIRCUITO 1

b1 = Branch(0,1,Component('I1',10,'I'))
b2 = Branch(0,1,Component('R1',50,'R'))
b3 = Branch(1,2,Component('R2',100,'R'))
b4 = Branch(2,0,Component('V3',2,'VCVS',b2))
b5 = Branch(1,3,Component('R3',150,'R'))
b6 = Branch(0,3,Component('I2',-3,'CCCS',b2))
b7 = Branch(1,4,Component('R4',200,'R'))
b8 = Branch(4,0,Component('V5',5,'V'))
c.addBranch(b1)
c.addBranch(b2)
c.addBranch(b3)
c.addBranch(b4)
c.addBranch(b5)
c.addBranch(b6)
c.addBranch(b7)
c.addBranch(b8)
del b1,b2,b3,b4,b5,b6,b7,b8


"""
### CIRCUITO 2

b1 = Branch(1,0,Component('V1',5,'V'))
b2 = Branch(1,0,Component('R1',5,'R'))
c.addBranch(b1)
c.addBranch(b2)
del b1,b2

"""
"""
### CIRCUITO 3

b1 = Branch(1,0,Component('R1',1000,'R'))
b2 = Branch(1,0,Component('V1',5,'V'))
b3 = Branch(1,2,Component('V2',6,'V'))
b4 = Branch(2,3,Component('V3',8,'V'))
b5 = Branch(2,0,Component('R2',1000,'R'))
b6 = Branch(3,0,Component('R3',1000,'R'))
c.addBranch(b1)
c.addBranch(b2)
c.addBranch(b3)
c.addBranch(b4)
c.addBranch(b5)
c.addBranch(b6)
del b1,b2,b3,b4,b5,b6

"""
c.updNodeCnt()

# cf=np.matrix([[ 0.0417, -0.0100, -0.0067, -0.0050,       0,       0,        0,       0],
#               [-0.0100,  0.0100,       0,       0,  1.0000,       0,        0,       0],
#               [-0.0067,       0,  0.0067,       0,       0,       0,   3.0000,       0],
#               [-0.0050,       0,       0,  0.0050,       0,  1.0000,        0,       0],
#               [      0,  1.0000,       0,       0,       0,       0,        0, -2.0000],
#               [      0,       0,       0,  1.0000,       0,       0,        0,       0],
#               [-1.0000,       0,       0,       0,       0,       0, -50.0000,       0],
#               [-1.0000,       0,       0,       0,       0,       0,        0, -1.0000]])

info = mna(c)
CF = info.get('CF')
x = info.get('x')
I = info.get('I')
N = info.get('N')
M = info.get('M')
P = info.get('P')
Q = info.get('Q')
R = info.get('R')

latt=circuit2na(c)

res=stepByStepNA(c,x)
res+='\n\n Test - Sum of the power in all components must be null:\n'
val=0
for b in c.branches:
    res += '\n\n Power in '+b.comp.name+':\n'
    (tmp1,tmp2)=stepByStepExercise(c,b.comp.name,'P',x)
    if b.comp.ctype=='R':
        val-=tmp1
    else:
        val+=tmp1
    res+=tmp2
res+='Sum='+str(val)+'\n' \
     'PS: this value may not be null due to precision errors, but all the powers are well calculated.\n'