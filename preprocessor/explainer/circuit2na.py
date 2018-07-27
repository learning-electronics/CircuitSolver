def circuit2na(circuit):
    eqs=list() #list of equations in LaTeX

    brVS=circuit.getBranchesWithVS()

    brVSgroups=list() #list of groups of VS that are connected to the same nodes, to build supernodes
    nodesDefined=set() #modes already defined on the supernodes equations
    idxAdded=set() #index of the list brVS that has already been added to the groups

    for i in range(len(brVS)):
        if i in idxAdded:
            continue

        brVSgroups.append(set())
        brVSgroups[-1].add(brVS[i])
        idxAdded.add(i)
        # TODO: MAKE SURE THIS DOESNT ONLY WORK IN ONE LEVEL , MEANING IT WILL NOT RETURN TWO VOLTAGE SOURCES THAT ARE CONNECTED THROUGH A THIRD
        for j in range(i + 1, len(brVS)):
            for br in brVSgroups[-1]:
                to_add = None
                if br.node1 == brVS[j].node1 != 0 or br.node2 == brVS[j].node2 != 0 or br.node2 == brVS[j].node1 != 0 or \
                        br.node1 == brVS[j].node2 != 0:
                    to_add = j
                    continue
            if to_add != None:
                brVSgroups[-1].add(brVS[to_add])
                idxAdded.add(to_add)

    for bGroups in brVSgroups:
        for b in bGroups:
            nodesDefined.add(b.node1)
            nodesDefined.add(b.node2)
        for eq in superNodeVoltageEq(circuit,bGroups):
            eqs.append(eq)
        tmp=superNodeCurrentEq(circuit,bGroups)
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


    res = '<p>Theoretical Definitions:\n\n</p>' \
          '<p>Node: an electrical point that connects two or more basic circuit elements.\n</p>' \
          '<p>Nodal voltage: the voltage in a given node referenced to the ground node.\n\n\n</p>'

    res+= '<p>Introduction to Nodal Analysis: \n\n</p>' \
          '<p>The nodal analysis method consists in writing an equation for each node in a circuit (except the reference' \
          ' node, ground node).\n</p>' \
          '<p>This means that the number of equations in the main system will be the same as the number of nodal ' \
          'voltages and they are the only independent variables. We must consequently define every current/voltage in' \
          ' function of the nodal voltages.\n</p>'

    res+='<p>In a node the sum of all the currents exiting it is null, thus, for the simpler case, all we have to do is ' \
         'to sum all the currents (in function of the nodal voltages) and equal them to zero.\n</p>'

    res+='<p>Note that this approach will bring us a problem in some cases, for we can\'t directly tell what is the ' \
         'current going through a voltage source.\n</p>' \
         '<p>In the case of there being a voltage source, we can however directly write an expression that equals the ' \
         'value of the voltage source to de difference of the nodal voltages amongst which nodes the source is ' \
         'connected. If one of the nodes is the reference the system is complete. If not, we have to build a new ' \
         'equation (considering we have to have an equation for each node besides reference). \n</p>' \
         '<p>This new equations consists of the sum of all the currents in the both nodes of the voltage source, in such' \
         ' way that the current going through it disappears from the equation, solving our struggle. This concept is ' \
         'called a supernode, because we are basically considering the whole voltage source as being one big special ' \
         'node, in the sense that we are adding together all the currents in both ends of it.\n\n</p>'

    res+= '<p>Besides the main system equations, we might have auxiliary equations to define the current or voltage ' \
          'values in dependent power sources. It\'s easy to conclude that the number of auxiliary equations is equal ' \
          'to the number of dependent power sources.\n\n\n</p>'

    res+= '<p>Circuit Explanation:\n\n</p>'

    nN=circuit.nodeCnt
    nC=len(circuit.getBranchesWithDep())
    res += '\n\n<p>Looking at the circuit we can count ' + str(nN) + ' nodes, which means we\'ll have '+str(nN-1)+' ' \
           'main equations, and '+str(nC)+' dependent components, which means we\'ll have '+str(nC)+' auxiliary equations. \n</p>'

    res += '\n\n<p>Starting to define the main equations:\n\n</p>'

    brVS = circuit.getBranchesWithVS()

    brVSgroups = list()  # list of groups of VS that are connected to the same nodes, to build supernodes
    nodesDefined = set()  # modes already defined on the supernodes equations
    idxAdded = set()  # index of the list brVS that has already been added to the groups

    for i in range(len(brVS)):
        if i in idxAdded:
            continue

        brVSgroups.append(set())
        brVSgroups[-1].add(brVS[i])
        idxAdded.add(i)
        # TODO: MAKE SURE THIS DOESNT ONLY WORK IN ONE LEVEL , MEANING IT WILL NOT RETURN TWO VOLTAGE SOURCES THAT ARE CONNECTED THROUGH A THIRD
        for j in range(i + 1, len(brVS)):
            for br in brVSgroups[-1]:
                to_add = None
                if br.node1 == brVS[j].node1 != 0 or br.node2 == brVS[j].node2 != 0 or br.node2 == brVS[j].node1 != 0 or \
                        br.node1 == brVS[j].node2 != 0:
                    to_add = j
                    continue
            if to_add != None:
                brVSgroups[-1].add(brVS[to_add])
                idxAdded.add(to_add)
    for bGroups in brVSgroups:
        nodesInGroup = set()
        for b in bGroups:
            nodesInGroup.add(b.node1)
            nodesInGroup.add(b.node2)

        if len(nodesInGroup) == 2 and 0 in nodesInGroup:
            nodesInGroup=list(nodesInGroup)
            if nodesInGroup[0]==0:
                n=nodesInGroup[1]
            else:
                n=nodesInGroup[0]
            res += '<p>Node ' + str(n) + ' has a VS that is directly connected to ground, thus, we can just define this node\'s voltage:\n</p>'
            res += '$$'
            for eq in superNodeVoltageEq(circuit, bGroups):
                res += eq
            res += '$$\n\n'
        else:
            res += '<p>Nodes '
            for n in nodesInGroup:
                if n != 0:
                    res += str(n) + ' '
            res += 'constitute a supernode, thus we have a voltage equation that relates the nodal voltages ' \
                   'and the voltage value for each branch:\n</p>'
            res += '$$' + eqs2latex(superNodeVoltageEq(circuit, bGroups)) + '$$\n'
            if 0 in nodesInGroup:
                res += '<p>As one of the VS\'s is connected to ground, the equations above are enough to define the ' \
                       'supernode.\n\n</p>'
            else:
                res += '<p>As none of the VS\'s is connected to ground we must also create a current equation for the ' \
                       'supernode:\n</p>'
                res += '$$' + superNodeCurrentEq(circuit,bGroups) + '$$\n\n'
        nodesDefined = nodesDefined.union(nodesInGroup)

    for n in range(circuit.nodeCnt):
        if n in nodesDefined:
            continue
        else:
            res += '<p>Node ' + str(
                n) + ' has no VS\'s connected to it, so we can evaluate directly the currents going through each branch, sum and equal them to zero:\n</p>'
            res += '$$' + nodeEq(circuit, n) + '$$\n\n'

    if nC>0:
        res+= '<p>Now we have to define the auxiliary equations, which is done as follows:\n</p>'
        res+= '$$'+eqs2latex(depEqs(circuit))+'$$\n\n'
    else:
        res+='<p>We have no dependent power sources, so we have obtained all the necessary equations.\n\n</p>'

    res+='<p>We have now our fully defined system of equations as follows: \n</p>'
    res+='$$'+circuit2na(circuit)+'$$\n\n'
    res+='<p>After solving this system we obtain the following nodal voltages:\n</p>'
    res+='$$'+eqs2latex(mnaVector2eqs(mnaVector,circuit.nodeCnt))+'$$\n\n'
    res = res.replace("--", "")

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
    res='<p>After having solved the NA system we already have the voltages for each node, so to obtain the voltage in a' \
        ' component it\'s very straight-forward, all we have to do is obtain the difference between the voltages in ' \
        'each end of the component:\n</p>'
    res += '$$V_{'+branch.comp.name+'} = '+voltageInBranch(branch,branch.node1)+' = '
    val=voltageInBranch_value(branch,branch.node1,mnaVector)
    res += str(val) + 'V$$\n'
    return (val,res)


def stepByStepCurrent(circuit,branch,mnaVector):
    res='<p>The way to obtain a current in a component depends on the type of component in question.\n</p>'

    ct=branch.comp.ctype

    if ct=='R':
        res+='<p>In a resistor, as we know, we can obtain the current in it from the nodal voltages and its value:\n</p>'
        res+='$$I_{'+branch.comp.name+'} = '+currentInResistor(branch,branch.node1)+' = '
        val=currentInResistor_value(branch,branch.node1,mnaVector)
    elif ct=='V' or ct=='VCVS' or ct=='CCVS':
        res+='<p>In a voltage source, the only way to obtain the current going through it is to sum all the  currents ' \
             'going through one of its nodes:\n</p>'
        if branch.node1!=0:
            n=branch.node1
        else:
            n=branch.node2
        res += '$$I_{' + branch.comp.name + '} = ' + currentInVS(circuit,branch,n) + ' = '
        val = currentInVS_value(circuit,branch,n, mnaVector)
    else: # ct==CS:
        res += '<p>In a current source, the current is defined by the current value, obviously:\n</p>'
        res += '$$I_{' + branch.comp.name + '} = ' + currentInCS(circuit,branch, branch.node1) + ' = '
        val = currentInCS_value(circuit,branch,branch.node1, mnaVector)

    res += str(val) + 'A$$\n'
    return (val,res)


def stepByStepPower(circuit,branch,mnaVector):
    res = '<p>To obtain the power in a component we have to obtain the product of the current times the voltage in it.\n</p>'

    ct = branch.comp.ctype

    if ct=='R':
        res+='<p>As the component in question is a resistor, knowing that its current can be expressed as:\n</p>'
        res+='$$'+currentInResistor(branch,branch.node1)+'$$\n'
        res+='<p>We can simplify its poweer expression and obtain the following value:\n</p>'
        res+='$$'+powerInResistor(branch)+' = '
        val=powerInResistor_value(branch,mnaVector)
    elif ct=='I' or ct=='CCCS' or ct=='VCCS':
        res+='<p>The Nodal Analysis method already gives us the voltage in the current source, so all we have to do is ' \
             'obtain the current and then multiply.\n</p>'
        (val,tmp)=stepByStepCurrent(circuit,branch,mnaVector)
        res+=tmp
        res+='$$'+powerInCS(circuit,branch)+' = '
        val=powerInCS_value(circuit,branch,mnaVector)
    else: #'VS'
        res += '<p>The Nodal Analysis method already gives us the voltage in the voltage source, so all we have to do is ' \
               'obtain the current and then multiply.\n</p>'
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
    for n in range(nc-1):
        eqs.append('V_{'+str(n+1)+'} = '+str(mnaVector[n][0])+'V')
    return eqs

def voltageInBranch(branch,beginningNode):
    if branch.node1==beginningNode:
        endingNode=branch.node2
    else:
        endingNode=branch.node1
    if endingNode!=0 and beginningNode!=0:
        return 'V_{'+str(beginningNode)+'} - V_{'+str(endingNode)+'}'
    elif beginningNode==0:
        return '-V_{' + str(endingNode) + '}'
    else:
        return 'V_{' + str(beginningNode) + '}'


def voltageInBranch_value(branch,beginningNode,mnaVector):
    if branch.node1==beginningNode:
        endingNode=branch.node2
    else:
        endingNode=branch.node1
    if endingNode!=0 and beginningNode!=0:
        return mnaVector[beginningNode-1][0]-mnaVector[endingNode-1][0]
    elif beginningNode==0:
        return -mnaVector[endingNode-1][0]
    else:
        return mnaVector[beginningNode-1][0]


def currentInBranch(circuit,branch,beginningNode):
    if branch.comp.ctype=='R':
        return currentInResistor(branch,beginningNode)
    elif branch.comp.ctype=='I' or branch.comp.ctype=='CCCS' or branch.comp.ctype=='VCCS':
        return currentInCS(circuit,branch,beginningNode)
    return currentInVS(circuit,branch,beginningNode)

def currentInBranch_value(circuit,branch,beginningNode,mnaVector):
    if branch.comp.ctype=='R':
        return currentInResistor_value(branch,beginningNode,mnaVector)
    elif branch.comp.ctype=='I' or branch.comp.ctype=='CCCS' or branch.comp.ctype=='VCCS':
        return currentInCS_value(circuit,branch,beginningNode,mnaVector)
    return currentInVS_value(circuit,branch,beginningNode,mnaVector)


def currentInVS(circuit, branch, beginningNode):
    if branch.node1==beginningNode:
        endingNode=branch.node2
    else:
        endingNode=branch.node1

    nds_beg,brs_beg = nonVSbranchesConnectedToBranchThroughNode(circuit, branch, beginningNode)
    nds_end,brs_end = nonVSbranchesConnectedToBranchThroughNode(circuit, branch, endingNode)

    if brs_beg==None and brs_end==None:
        return 'ERROR: IMPOSSIBILITY TO EVALUATE CURRENT IN BRANCH '+str(branch.getNodes())
    if brs_beg==None or (brs_beg!=None and brs_end!=None and len(brs_end)>len(brs_beg)):
        nds=nds_end
        brs=brs_end
        res = '('
    else:
        nds = nds_beg
        brs = brs_beg
        res = '-('

    first=True
    for i in range(len(brs)):
        if not first:
            res += ' + '
        first=False
        res += currentInBranch(circuit, brs[i], nds[i])
    return res+')'


def currentInVS_value(circuit, branch, beginningNode,mnaVector):
    if branch.node1==beginningNode:
        endingNode=branch.node2
    else:
        endingNode=branch.node1

    nds_beg,brs_beg = nonVSbranchesConnectedToBranchThroughNode(circuit, branch, beginningNode)
    nds_end,brs_end = nonVSbranchesConnectedToBranchThroughNode(circuit, branch, endingNode)

    if brs_beg==None and brs_end==None:
        return 'ERROR: IMPOSSIBILITY TO EVALUATE CURRENT IN BRANCH '+str(branch.getNodes())
    if brs_beg==None or (brs_beg!=None and brs_end!=None and len(brs_end)>len(brs_beg)):
        nds=nds_end
        brs=brs_end
        invert=False
    else:
        nds = nds_beg
        brs = brs_beg
        invert=True

    res=0
    for i in range(len(brs)):
        res += currentInBranch_value(circuit, brs[i], nds[i],mnaVector)
    if invert:
        res *= -1
    return res


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
    else:#vccs
        val=branch.comp.value*voltageInBranch_value(branch.comp.dependent,branch.comp.dependent.node1,mnaVector)
    if branch.node1 == beginningNode:
        return val
    return -val


def currentInResistor(branch,beginningNode):
    resistor=branch.comp.name
    return '\\frac{'+voltageInBranch(branch,beginningNode)+'}{'+resistor+'}'


def currentInResistor_value(branch,beginningNode,mnaVector):
    resistor=branch.comp.value
    return voltageInBranch_value(branch,beginningNode,mnaVector)/resistor


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
    resistor=branch.comp.name
    return '\\frac{('+voltageInBranch(branch,branch.node1)+')^{2}}{'+resistor+'}'


def powerInResistor_value(branch,mnaVector):
    resistor=branch.comp.value
    return voltageInBranch_value(branch,branch.node1,mnaVector)**2/resistor


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
        val=branch.comp.value*voltageInBranch_value(branch.comp.dependent,branch.comp.dependent.node1,mnaVector)
    return abs(val*currentInVS_value(circuit,branch,beginningNode,mnaVector))


def powerInCS(circuit,branch):
    n1 = branch.node1
    val=currentInCS(circuit,branch,n1)
    return '\\left |'+val+' \\times ('+voltageInBranch(branch,n1)+') \\right |'



def powerInCS_value(circuit,branch,mnaVector):
    n1 = branch.node1
    val=currentInBranch_value(circuit,branch,n1,mnaVector)
    return abs(val*voltageInBranch_value(branch,n1,mnaVector))


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


def superNodeVoltageEq(circuit,branch):
    ct=branch.comp.ctype
    if ct=='V':
        val=str(branch.comp.value)
    elif ct=='CCVS':
        val=str(branch.comp.value)+' \\times I_{'+branch.comp.dependent.comp.name+'}'
    else: #'VCVS'
        val = str(branch.comp.value) + ' \\times V_{' + branch.comp.dependent.comp.name + '}'
    return voltageInBranch(branch,branch.node1)+' = ' + val


def superNodeVoltageEq(circuit,branch):
    eqs=list()
    for b in branch:
        ct=b.comp.ctype
        if ct=='V':
            val=str(b.comp.value)
        elif ct=='CCVS':
            val=str(b.comp.value)+' \\times I_{'+b.comp.dependent.comp.name+'}'
        else: #'VCVS'
            val = str(b.comp.value) + ' \\times V_{' + b.comp.dependent.comp.name + '}'
        eqs.append(voltageInBranch(b,b.node1)+' = ' + val)
    return eqs


def superNodeCurrentEq(c,branch):
    nodes=set() #set with all nodes contained in the supernode
    for b in branch:
        nodes.add(b.node1)
        nodes.add(b.node2)
    if 0 in nodes:
        return None

    br=set() #branches that are connected to one of the nodes in the supernode
    for n in nodes:
        for b in c.getBranchesNode(n):
            br.add(b)
    nodes=list(nodes)
    for (n1,n2) in [(nodes[i],nodes[j]) for i in range(len(nodes)) for j in range(i+1, len(nodes))]:
        for b in c.getBranchesNodes([n1,n2]):
            br.remove(b) #removing all branches that belong to the supernode
    eq=''
    for b in br:
        if b.node1 in nodes:
            n=b.node1
        else:
            n = b.node2
        if eq != '':
            eq += ' + '

        eq+=currentInBranch(c,b,n)
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
            eq+=voltageInBranch(b.comp.dependent,b.comp.dependent.node1)
        eqs.append(eq)

    return eqs


def nonVSbranchesConnectedToBranchThroughNode(circuit,branch,node):
    if node==0:
        return None,None
    #this method returns a set of branches that are connected to @branch through @node but that aren't VS branches, so
    # that we can calculate the current in a branch with a VS
    brs=circuit.getBranchesNode(node)
    brs.remove(branch)
    beginningNodes=list()
    for i in range(len(brs)):
        beginningNodes.append(node)
    for br in brs:
        if br.comp.ctype=='V' or br.comp.ctype=='CCVS' or br.comp.ctype=='VCVS':
            beginningNodes.pop(brs.index(br))
            brs.remove(br)
            if br.node1==node:
                n=br.node2
            else:
                n=br.node1
            if n==0:
                return None,None
            (begN2,brs2)=nonVSbranchesConnectedToBranchThroughNode(circuit,br,n)
            if brs2==None:
                return None, None
            to_remove=set()
            for br2 in brs2:
                if br2 in brs:
                    beginningNodes.pop(brs.index(br2))
                    begN2.pop(brs2.index(br2))
                    to_remove.add(br2)
                else:
                    brs.append(br2)
            for bb in to_remove:
                brs.remove(bb)
            for nd in begN2:
                beginningNodes.append(nd)
    return (beginningNodes,brs)