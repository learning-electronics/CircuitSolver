import sys
sys.path.insert(0, '../mna')
from mnaModule import mna

def circuit2na(circuit):
    eqs=list() #list of equations in LaTeX

    brVS=circuit.getBranchesWithVS()
    nodesDefined=set()
    for b in brVS:
        nodesDefined.add(b.node1)
        nodesDefined.add(b.node2)

        eqs.append(superNodeVoltageEq(b))
        tmp=superNodeCurrentEq(circuit,b)
        if tmp!=None:
            eqs.append(tmp)
    for n in range(circuit.nodeCnt):
        if n in nodesDefined:
            continue
        else:
            eqs.append(nodeEq(circuit,n))
    for eq in depEqs(circuit):
        eqs.append(eq)

    res='\\left \\{ \\begin{matrix} '
    for eq in eqs:
        if res != '\\left \\{ \\begin{matrix} ':
            res+= ' \\\\ '
        res+=eq
    res+=' \\end{matrix}\\right.'
    return res

def stepByStep(circuit):

    info=mna(circuit)

    res='The nodal analysis method consists in writing an equation for each node in a circuit (excepte the reference node, ground node).\n'
    res+='In a node the sum of all the currents exiting it is null, thus, for the simpler case, all we have to do is ' \
         'to sum all the currents and equal them to zero.\n'
    res+='Note that this approach will bring us a problem in some cases, for we can\'t directly tell what is the ' \
         'current going through a voltage source (in most cases).\n'
    res+='In these special cases we might have to create a supernode, that is, a node around the voltage source ' \
         'all the currents exiting it still have to sum up  to zero, thus giving us one equation, but we need two, ' \
         'for there are two nodes lost in the process, so the second equation will be the relation between the voltages' \
         ' in each node. This is as complex as the nodal analysis gets, but in some cases you might not have to form a ' \
         'supernode, if the voltage source is connected to the ground node, you can only just directly define the ' \
         'voltage of the node being considered, and move on to the other nodes.'



    res+= 'The number of nodes alongside with the number of dependent power sources already define the number of ' \
          'equations our system will have. Because we have the main equations, that are correspounding to each node ' \
          'except ground and the auxiliary equations, that define the current or voltage in a dependent component.\n'

    nN=circuit.nodeCnt
    nC=len(circuit.getBranchesWithDep())
    res += '\n\nLooking at the circuit we can count ' + str(nN) + ' nodes, which means we\'ll have '+str(nN-1)+' ' \
           'main equations, and '+str(nC)+' dependent components, which means we\'ll have '+str(nC)+' auxiliary equations. \n'

    res += '\n\nStarting to define the main equations:\n\n'

    nodesDefined=set()
    brVS=circuit.getBranchesWithVS()
    for n in range(1,nN):
        if n in nodesDefined:
            continue
        nodesDefined.add(n)
        brVS_n=list(filter(lambda x: x.node1==n or x.node2==n,brVS))
        if len(brVS_n)>1:
            res+= 'ERROR: THIS ALGORITHM DOESN\'T WORK FOR CASES IN WHICH TWO VS ARE CONNECTED TO THE SAME NODE'
            return res
        elif len(brVS_n)>0:
            if brVS_n[0].node1==0 or brVS_n[0].node2==0:
                res+= 'Node '+str(n)+' has a VS that is directly connected to ground, thus, we can just define this node\'s voltage:\n'
                res+= superNodeVoltageEq(brVS_n[0])+'\n\n'

            else:
                res += 'Node ' + str(n) + ' has a VS that is between two nodes, so we need to form a Super Node and have two equations, as mentioned previously.\n'
                res+='The Super Node\'s voltage equation:\n'
                res+=superNodeVoltageEq(brVS_n[0])+'\n'
                res += 'And the Super Node\'s current equation:\n'
                res += superNodeCurrentEq(brVS_n[0]) + '\n\n'
                nodesDefined.add(brVS_n[0].node1==0)
                nodesDefined.add(brVS_n[0].node2==0)

        else:
            res += 'Node ' + str(n) + ' has no VS\'s connected to it, so we can evaluate directly the currents going through each branch, sum and equal them to zero:\n'
            res += nodeEq(circuit,n)+'\n\n'

    if nC>0:
        res+= 'Now we have to define the auxiliary equations, which is done as follows:\n'
        res += '\\left \\{ \\begin{matrix} '
        first=True
        for eq in depEqs(circuit):
            if not first:
                res += ' \\\\ '
            first=False
            res += eq
        res += ' \\end{matrix}\\right.\n\n'

    else:
        res+='We have no dependent power sources, so we have obtained all the necessary equations.\n\n'

    res+='We have now our fully defined system of equations as follows: \n'
    res+=circuit2na(circuit)+'\n'
    return res


def currentInBranch(circuit,branch,beginningNode):
    if branch.comp.ctype=='R':
        return currentInResistor(branch,beginningNode)
    elif branch.comp.ctype=='I' or branch.comp.ctype=='CCCS' or branch.comp.ctype=='VCCS':
        return currentInCS(branch,beginningNode)
    return currentInVS(circuit,branch,beginningNode)


def currentInVS(circuit, branch, beginningNode):
    res = ''
    for br in circuit.getBranchesNode(beginningNode):
        if br == branch:
            continue
        else:
            if res != '':
                res += ' + '
            res += currentInBranch(circuit, br, beginningNode)
    return res


def currentInCS(branch, beginningNode):
    if branch.node1 == beginningNode:
        return branch.comp.name
    return '-' + branch.comp.name


def currentInResistor(branch,beginningNode):
    if branch.node1==beginningNode:
        endingNode=branch.node2
    else:
        endingNode = branch.node1
    resistor=branch.comp.name
    if endingNode!=0 and beginningNode!=0:
        return '\\frac{V_{'+str(beginningNode)+'} - V_{'+str(endingNode)+'}}{'+resistor+'}'
    elif beginningNode==0:
        return '\\frac{ - V_{' + str(endingNode) + '}}{' + resistor + '}'
    else:
        return '\\frac{V_{' + str(beginningNode) + '}}{' + resistor + '}'

def powerInBranch(circuit,branch,beginningNode):
    if branch.comp.ctype=='R':
        return powerInResistor(branch)
    elif branch.comp.ctype=='I' or branch.comp.ctype=='CCCS' or branch.comp.ctype=='VCCS':
        return powerInCS(branch)
    return powerInVS(circuit,branch,beginningNode)

def powerInResistor(branch):
    n1=branch.node1
    n2=branch.node2
    resistor=branch.comp.name
    if n1!=0 and n2!=0:
        return '\\frac{(V_{'+str(n1)+'} - V_{'+str(n2)+'})^{2}}{'+resistor+'}'
    elif n2==0:
        return '\\frac{ - V_{' + str(n1) + '}^{2}}{' + resistor + '}'
    else:
        return '\\frac{V_{' + str(n1) + '}^{2}}{' + resistor + '}'


def powerInVS(circuit,branch,beginningNode):
    return '\\left |'+branch.comp.name+' \\times ('+currentInVS(circuit,branch,beginningNode)+') \\right |'


def powerInCS(branch):
    return '\\left |' + branch.comp.name + ' \\times ( V_{'+str(branch.node1)+'} - V_{'+str(branch.node2)+'} ) \\right |'


def superNodeVoltageEq(branch):
    n1=branch.node1
    n2=branch.node2

    if n1==0:
        return 'V_{' + str(n2) + '} = -'+branch.comp.name
    elif n2==0:
        return 'V_{' + str(n1) + '} = ' + branch.comp.name
    return 'V_{' + str(n1) + '} - V_{' + str(n2) + '} = ' + branch.comp.name

def nodeEq(c,node):
    br=c.getBranchesNode(node)

    eq=''
    for b in br:
        if eq!='':
            eq+=' + '
        if b.comp.ctype=='R':
            eq+=currentInResistor(b,node)
        elif b.comp.ctype=='I' or b.comp.ctype=='VCCS' or b.comp.ctype=='CCCS':
            eq += currentInCS(b,node)
    eq+=' = 0'
    return eq

def superNodeCurrentEq(c,branch):
    n1=branch.node1
    n2=branch.node2

    if n1==0 or n2==0:
        return None

    br=c.getBranchesNode(n1)
    br=br.append(c.getBranchesNode(n2))
    br=set(br)
    br.remove(c.getBranchesNodes([n1,n2]))
    eq=''
    for b in br:
        if b.node1==n1 or b.node2==n1:
            n=n1
        else:
            n=n2

        if eq != '':
            eq += ' + '

        if b.comp.ctype=='R':
            eq+=currentInResistor(b,n)
        elif b.comp.ctype=='I' or b.comp.ctype=='VCCS' or b.comp.ctype=='CCCS' :
            eq+=currentInCS(b,n)
    eq += ' = 0'

    return eq

def depEqs(c):
    br=c.getBranchesWithDep()

    eqs=list()

    for b in br:
        eq = b.comp.name + ' = ' + str(b.comp.value) + ' \\times '
        if b.comp.ctype=='CCVS' or b.comp.ctype=='CCCS':
            if b.comp.dependent.comp.ctype=='R':
                eq+=currentInResistor(b.comp.dependent,b.comp.dependent.node1)
            else:
                eq+=currentInCS(b.comp.dependent,b.comp.dependent.node1)
        elif b.comp.ctype=='VCVS' or b.comp.ctype=='VCCS':
            if b.comp.dependent.node1==0:
                eq += '-V_{' + str(b.comp.dependent.node2) + '}'
            elif b.comp.dependentnode2==0:
                eq += 'V_{' + str(b.comp.dependent.node1) + '}'
            else:
                eq+='(V_{'+str(b.comp.dependent.node1)+'}-V_{'+str(b.comp.dependent.node2)+'})'
        eqs.append(eq)

    return eqs

