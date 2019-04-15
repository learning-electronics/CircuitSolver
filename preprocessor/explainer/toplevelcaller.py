from explainer import *

#Get project dir
from os.path import dirname,realpath,join
import sys
project_path=dirname(realpath(__file__))
sys.path+=[join(project_path,'mna/')]
from mnaModule import mna
sys.path+=[project_path]
from datastructure import Branch

def general_ressol(circuit):
	circuit.mnaVector=mna(circuit)['x']
	return general_classic(circuit,circuit.mnaVector)

def specific_ressol(circuit,target,questtype):
	if questtype=='V':
		branch=circuit.getBranchCompName(target)
		return stepByStepVoltage(circuit,branch,circuit.mnaVector)
	elif questtype=='I':
		branch=circuit.getBranchCompName(target)
		return stepByStepCurrent(circuit,branch,circuit.mnaVector)
	elif questtype=='P':
		branch=circuit.getBranchCompName(target)
		return stepByStepPower(circuit,branch,circuit.mnaVector)
	elif questtype=='T':
		return stepByStepThevenin(circuit,Branch(int(target[0]),int(target[1]),None),circuit.mnaVector)
	elif questtype=='N':
		return stepByStepNorton(circuit,Branch(int(target[0]),int(target[1]),None),circuit.mnaVector)
	elif questtype=='Trans':
		branch=circuit.getBranchCompName(target)
		return stepByStepTrans(circuit,branch,circuit.mnaVector)
	else:
		raise Exception('Explainer/Solver: unimplemented exercise type') 
