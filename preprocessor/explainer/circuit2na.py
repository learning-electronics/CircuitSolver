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

        eqs.append(superNodeVoltageEq(circuit,b))
        tmp=superNodeCurrentEq(circuit,b)
        if tmp!=None:
            eqs.append(tmp)
    for n in range(circuit.nodeCnt):
        if n in nodesDefined:
            continue
        else:
            eqs.append(nodeEq(circuit,n))

    res=eqs2latex(eqs)
    eqs=depEqs(circuit)
    if len(eqs)>0:
        res+=' '+eqs2latex(depEqs(circuit))

    res = res.replace("--", "")
    return res


def stepByStepNA(circuit,mnaVector):


    res = 'Theoretical Definitions:\n\n' \
          'Node: an electrical point that connects two or more basic circuit elements.\n' \
          'Nodal voltage: the voltage in a given node referenced to the ground node.\n\n\n'

    res+= 'Introduction to Nodal Analysis: \n\n' \
          'The nodal analysis method consists in writing an equation for each node in a circuit (except the reference' \
          ' node, ground node).\n' \
          'This means that the number of equations in the main system will be the same as the number of nodal ' \
          'voltages and they are the only independent variables. We must consequently define every current/voltage in' \
          ' function of the nodal voltages.\n'

    res+='In a node the sum of all the currents exiting it is null, thus, for the simpler case, all we have to do is ' \
         'to sum all the currents (in function of the nodal voltages) and equal them to zero.\n'

    res+='Note that this approach will bring us a problem in some cases, for we can\'t directly tell what is the ' \
         'current going through a voltage source.\n' \
         'In the case of there being a voltage source, we can however directly write an expression that equals the ' \
         'value of the voltage source to de difference of the nodal voltages amongst which nodes the source is ' \
         'connected. If one of the nodes is the reference the system is complete. If not, we have to build a new ' \
         'equation (considering we have to have an equation for each node besides reference). \n' \
         'This new equations consists of the sum of all the currents in the both nodes of the voltage source, in such' \
         ' way that the current going through it disappears from the equation, solving our struggle. This concept is ' \
         'called a supernode, because we are basically considering the whole voltage source as being one big special ' \
         'node, in the sense that we are adding together all the currents in both ends of it.\n\n'

    res+= 'Besides the main system equations, we might have auxiliary equations to define the current or voltage ' \
          'values in dependent power sources. It\'s easy to conclude that the number of auxiliary equations is equal ' \
          'to the number of dependent power sources.\n\n\n'

    res+= 'Circuit Explanation:\n\n'

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
                res+= '$$'+superNodeVoltageEq(circuit,brVS_n[0])+'$$\n\n'

            else:
                res += 'Node ' + str(n) + ' has a VS that is between two nodes, so we need to form a Super Node and have two equations, as mentioned previously.\n'
                res+='The Super Node\'s voltage equation:\n'
                res+='$$'+superNodeVoltageEq(brVS_n[0])+'$$\n'
                res += 'And the Super Node\'s current equation:\n'
                res += '$$'+superNodeCurrentEq(brVS_n[0]) + '$$\n\n'
                nodesDefined.add(brVS_n[0].node1==0)
                nodesDefined.add(brVS_n[0].node2==0)

        else:
            res += 'Node ' + str(n) + ' has no VS\'s connected to it, so we can evaluate directly the currents going through each branch, sum and equal them to zero:\n'
            res += '$$'+nodeEq(circuit,n)+'$$\n\n'


    if nC>0:
        res+= 'Now we have to define the auxiliary equations, which is done as follows:\n'
        res+= '$$'+eqs2latex(depEqs(circuit))+'$$\n\n'
    else:
        res+='We have no dependent power sources, so we have obtained all the necessary equations.\n\n'

    res+='We have now our fully defined system of equations as follows: \n'
    res+='$$'+circuit2na(circuit)+'$$\n\n'
    res+='After solving this system we obtain the following nodal voltages:\n'
    res+='$$'+eqs2latex(mnaVector2eqs(mnaVector,circuit.nodeCnt))+'$$\n\n'

    return res


def stepByStepExercise(circuit,elem,typeOfExercise,mnaVector):
    branch=circuit.getBranchCompName(elem)
    if typeOfExercise=='V':
        return stepByStepVoltage(circuit,branch,mnaVector)
    elif typeOfExercise=='I':
        return stepByStepCurrent(circuit,branch,mnaVector)
    else:
        return stepByStepPower(circuit,branch,mnaVector)


def stepByStepVoltage(circuit,branch,mnaVector):
    res='After having solved the NA system we already have the voltages for each node, so to obtain the voltage in a' \
        ' component it\'s very straight-forward, all we have to do is obtain the difference between the voltages in ' \
        'each end of the component:\n'
    n1=branch.node1
    n2=branch.node2
    if n1!=0 and n2!=0:
        res += '$$V_{'+branch.comp.name+'} = V_{'+str(n1)+'} - V_{'+str(n2)+'} = '
        val=mnaVector[n1-1][0]-mnaVector[n2-1][0]
    elif n2==0:
        res += '$$V_{'+branch.comp.name+'} = V_{'+str(n1)+'} = '
        val = mnaVector[n1 - 1][0]
    else:
        res += '$$V_{' + branch.comp.name + '} = -V_{' + str(n2) + '} = '
        val = -mnaVector[n2 - 1][0]
    res += str(val) + 'V$$\n'

    return (val,res)


def stepByStepCurrent(circuit,branch,mnaVector):
    res='The way to obtain a current in a component depends on the type of component in question.\n'

    ct=branch.comp.ctype

    if ct=='R':
        res+='In a resistor, as we know, we can obtain the current in it from the nodal voltages and its value:\n'
        res+='$$I_{'+branch.comp.name+'} = '+currentInResistor(branch,branch.node1)+' = '
        val=currentInResistor_value(branch,branch.node1,mnaVector)
    elif ct=='V' or ct=='VCVS' or ct=='CCVS':
        res+='In a voltage source, the only way to obtain the current going through it is to sum all the  currents ' \
             'going through one of its nodes:\n'
        if branch.node1!=0:
            n=branch.node1
        else:
            n=branch.node2
        res += '$$I_{' + branch.comp.name + '} = ' + currentInVS(circuit,branch,n) + ' = '
        val = currentInVS_value(circuit,branch,n, mnaVector)
    else: # ct==CS:
        res += 'In a current source, the current is defined by the current value, obviously:\n'
        res += '$$I_{' + branch.comp.name + '} = ' + currentInCS(circuit,branch, branch.node1) + ' = '
        val = currentInCS_value(circuit,branch,branch.node1, mnaVector)

    res += str(val) + 'A$$\n'
    return (val,res)


def stepByStepPower(circuit,branch,mnaVector):
    res = 'To obtain the power in a component we have to obtain the product of the current times the voltage in it.\n'

    ct = branch.comp.ctype

    if ct=='R':
        res+='As the component in question is a resistor, knowing that its current can be expressed as:\n'
        res+='$$'+currentInResistor(branch,branch.node1)+'$$\n'
        res+='We can simplify its poweer expression and obtain the following value:\n'
        res+='$$'+powerInResistor(branch)+' = '
        val=powerInResistor_value(branch,mnaVector)
    elif ct=='I' or ct=='CCCS' or ct=='VCCS':
        res+='The Nodal Analysis method already gives us the voltage in the current source, so all we have to do is ' \
             'obtain the current and then multiply.\n'
        (val,tmp)=stepByStepCurrent(circuit,branch,mnaVector)
        res+=tmp
        res+='$$'+powerInCS(circuit,branch)+' = '
        val=powerInCS_value(circuit,branch,mnaVector)
    else: #'VS'
        res += 'The Nodal Analysis method already gives us the voltage in the voltage source, so all we have to do is ' \
               'obtain the current and then multiply.\n'
        (val, tmp) = stepByStepCurrent(circuit, branch, mnaVector)
        res += tmp
        res += '$$' + powerInVS(circuit,branch) + ' = '
        val = powerInVS_value(circuit,branch, mnaVector)

    res += str(val) + 'W$$\n'
    return (val,res)

def eqs2latex(eqs):
    res='\\left \\{ \\begin{matrix} '
    first=True
    for eq in eqs:
        if not first:
            res += ' \\\\ '
        first = False
        res += eq
    res += ' \\end{matrix}\\right.'
    return res


def mnaVector2eqs(mnaVector,nc):
    eqs=[]
    for n in range(nc):
        eqs.append('V_{'+str(n+1)+'} = '+str(mnaVector[n][0]))
    return eqs


def currentInBranch(circuit,branch,beginningNode):
    if branch.comp.ctype=='R':
        return currentInResistor(branch,beginningNode)
    elif branch.comp.ctype=='I' or branch.comp.ctype=='CCCS' or branch.comp.ctype=='VCCS':
        return currentInCS(branch,beginningNode)
    return currentInVS(circuit,branch,beginningNode)

def currentInBranch_value(circuit,branch,beginningNode,mnaVector):
    if branch.comp.ctype=='R':
        return currentInResistor_value(branch,beginningNode,mnaVector)
    elif branch.comp.ctype=='I' or branch.comp.ctype=='CCCS' or branch.comp.ctype=='VCCS':
        return currentInCS_value(circuit,branch,beginningNode,mnaVector)
    return currentInVS_value(circuit,branch,beginningNode,mnaVector)


def currentInVS(circuit, branch, beginningNode):
    res = ''
    for br in circuit.getBranchesNode(beginningNode):
        if br == branch:
            continue
        else:
            if res != '':
                res += ' + '
            res += currentInBranch(circuit, br, beginningNode)
    return '-1 \\times ('+res+')'


def currentInVS_value(circuit, branch, beginningNode,mnaVector):
    value=0
    for br in circuit.getBranchesNode(beginningNode):
        if br == branch:
            continue
        else:
            value -= currentInBranch_value(circuit, br, beginningNode,mnaVector)
    return value


def currentInCS(circuit,branch, beginningNode):
    if branch.comp.ctype=='I':
        val=str(branch.comp.value)
    elif branch.comp.ctype=='CCCS':
        val=str(branch.comp.value)+' \\times I_{'+branch.comp.dependent.comp.name+'}'
    else:
        val = str(branch.comp.value) + ' \\times V_{' + branch.comp.dependent.comp.name + '}'
    if branch.node1 == beginningNode:
        return val
    return '-' + val


def currentInCS_value(circuit,branch, beginningNode,mnaVector):
    if branch.comp.ctype=='I':
        val=branch.comp.value
    elif branch.comp.ctype=='CCCS':
        val=branch.comp.value*currentInBranch_value(circuit,branch.comp.dependent,branch.comp.dependent.node1,mnaVector)
    else:
        n1=branch.comp.dependent.node1
        n2=branch.comp.dependent.node2
        val=branch.comp.value*(mnaVector[n1-1][0]-mnaVector[n2-1][0])
    if branch.node1 == beginningNode:
        return val
    return -val


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


def currentInResistor_value(branch,beginningNode,mnaVector):
    if branch.node1==beginningNode:
        endingNode=branch.node2
    else:
        endingNode = branch.node1
    resistor=branch.comp.value
    if endingNode!=0 and beginningNode!=0:
        return (mnaVector[beginningNode-1][0]-mnaVector[endingNode-1][0])/resistor
    elif beginningNode==0:
        return -mnaVector[endingNode-1][0]/resistor
    else:
        return mnaVector[beginningNode-1][0]/resistor


def powerInBranch(circuit,branch):
    if branch.comp.ctype=='R':
        return powerInResistor(branch)
    elif branch.comp.ctype=='I' or branch.comp.ctype=='CCCS' or branch.comp.ctype=='VCCS':
        return powerInCS(branch)
    return powerInVS(circuit,branch)


def powerInBranch_value(circuit,branch,mnaVector):
    if branch.comp.ctype=='R':
        return powerInResistor_value(branch,mnaVector)
    elif branch.comp.ctype=='I' or branch.comp.ctype=='CCCS' or branch.comp.ctype=='VCCS':
        return powerInCS_value(branch,mnaVector)
    return powerInVS_value(circuit,branch,mnaVector)


def powerInResistor(branch):
    n1=branch.node1
    n2=branch.node2
    resistor=branch.comp.name
    if n1!=0 and n2!=0:
        return '\\frac{(V_{'+str(n1)+'} - V_{'+str(n2)+'})^{2}}{'+resistor+'}'
    elif n2==0:
        return '\\frac{ - V_{' + str(n1) + '}^{2}}{' + resistor + '}'
    else:
        return '\\frac{V_{' + str(n2) + '}^{2}}{' + resistor + '}'


def powerInResistor_value(branch,mnaVector):
    n1=branch.node1
    n2=branch.node2
    resistor=branch.comp.value
    if n1!=0 and n2!=0:
        return (mnaVector[n1-1][0]-mnaVector[n2-1][0])**2/resistor
    elif n2==0:
        return mnaVector[n1-1][0]**2/resistor
    else:
        return mnaVector[n2-1][0]**2/resistor


def powerInVS(circuit,branch):
    if branch.node1!=0:
        beginningNode=branch.node1
    else:
        beginningNode=branch.node2
    ct=branch.comp.ctype
    if ct=='V':
        val=str(branch.comp.value)
    elif ct=='CCVS':
        val=str(branch.comp.value)+' \\times I_{'+branch.comp.dependent.comp.name+'}'
    else: #'VCVS'
        val = str(branch.comp.value) + ' \\times V_{' + branch.comp.dependent.comp.name + '}'
    return '\\left |'+val+' \\times ('+currentInVS(circuit,branch,beginningNode)+') \\right |'


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
        val=branch.comp.value*currentInBranch_value(circuit,branch.comp.dependent.comp.name,branch.comp.dependent.node1,mnaVector)
    else: #'VCVS'
        val=branch.comp.value*stepByStepVoltage(circuit,branch.comp.dependent,mnaVector)[0]
    return abs(val*currentInVS_value(circuit,branch,beginningNode,mnaVector))


def powerInCS(circuit,branch):
    n1 = branch.node1
    n2 = branch.node2
    val=currentInCS(circuit,branch,n1)
    if n1!=0 and n2!=0:
        return '\\left |'+val+' \\times ( V_{' +str(n1)+'} - V_{'+str(n2)+'} ) \\right |'
    elif n2==0:
        return '\\left |'+val+' \\times V_{'+str(n1)+'} \\right |'
    else:
        return '\\left |'+val+' \\times V_{'+str(n2)+'} \\right |'



def powerInCS_value(circuit,branch,mnaVector):
    n1 = branch.node1
    n2 = branch.node2
    val=currentInBranch_value(circuit,branch,n1,mnaVector)
    if n1!=0 and n2!=0:
        return abs(val*(mnaVector[n1-1][0]-mnaVector[n2-1][0]))
    elif n2==0:
        return abs(val*mnaVector[n1-1][0])
    else:
        return abs(val*-mnaVector[n2-1][0])


def superNodeVoltageEq(circuit,branch):
    n1=branch.node1
    n2=branch.node2
    ct=branch.comp.ctype

    if ct=='V':
        val=str(branch.comp.value)
    elif ct=='CCVS':
        val=str(branch.comp.value)+' \\times I_{'+branch.comp.dependent.comp.name+'}'
    else: #'VCVS'
        val = str(branch.comp.value) + ' \\times V_{' + branch.comp.dependent.comp.name + '}'
    if n1==0:
        return 'V_{' + str(n2) + '} = -'+val
    elif n2==0:
        return 'V_{' + str(n1) + '} = ' + val
    return 'V_{' + str(n1) + '} - V_{' + str(n2) + '} = ' + val

def nodeEq(c,node):
    br=c.getBranchesNode(node)

    eq=''
    for b in br:
        if eq!='':
            eq+=' + '
        if b.comp.ctype=='R':
            eq+=currentInResistor(b,node)
        elif b.comp.ctype=='I' or b.comp.ctype=='VCCS' or b.comp.ctype=='CCCS':
            eq += currentInCS(c,b,node)
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
        if b.comp.ctype=='CCVS' or b.comp.ctype=='CCCS':
            eq = 'I_{'+b.comp.dependent.comp.name + '} = '
            if b.comp.dependent.comp.ctype=='R':
                eq+=currentInResistor(b.comp.dependent,b.comp.dependent.node1)
            else:
                eq+=currentInCS(b.comp.dependent,b.comp.dependent.node1)
        elif b.comp.ctype=='VCVS' or b.comp.ctype=='VCCS':
            eq = 'V_{' + b.comp.dependent.comp.name + '} = '
            if b.comp.dependent.node1==0:
                eq += '-V_{' + str(b.comp.dependent.node2) + '}'
            elif b.comp.dependentnode2==0:
                eq += 'V_{' + str(b.comp.dependent.node1) + '}'
            else:
                eq+='(V_{'+str(b.comp.dependent.node1)+'}-V_{'+str(b.comp.dependent.node2)+'})'
        eqs.append(eq)

    return eqs

