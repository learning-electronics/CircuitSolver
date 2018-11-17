from explainer import *

#Get project dir
from os.path import dirname,realpath,join
import sys
project_path=dirname(realpath(__file__))
sys.path+=[join(project_path,'mna/')]
from mnaModule import mna

def general_ressol(circuit):
	circuit.mnaVector=mna(circuit)['x']
	return general_classic(circuit,circuit.mnaVector)

def specific_ressol(circuit,target,questtype):
	branch=circuit.getBranchCompName(target)
	if questtype=='V':
		return stepByStepVoltage(circuit,branch,circuit.mnaVector)
	elif questtype=='I':
		return stepByStepCurrent(circuit,branch,circuit.mnaVector)
	elif questtype=='P':
		return stepByStepPower(circuit,branch,circuit.mnaVector)
	elif questtype=='T':
		return stepByStepThevenin(circuit,branch,circuit.mnaVector)
	elif questtype=='N':
		return stepByStepNorton(circuit,branch,circuit.mnaVector)
	else:
		raise Exception('circuit2na: unimplemented exercise type') 
