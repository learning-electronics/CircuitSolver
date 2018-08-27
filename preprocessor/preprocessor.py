from os.path import abspath,realpath,relpath,dirname,join
import sys
from datastructure import Circuit,Branch,Component

#Get project dir
project_path=dirname(realpath(__file__))

sys.path+=[join(project_path,'parser/')]
from spiceProcessor import run_parser

sys.path+=[join(project_path,'mna/')]
from mnaModule import mna
#from mnaModule_DC import mna
from randSol import randomWrongs

sys.path+=[join(project_path,'explainer/')]
from circuit2na import stepByStepNA,stepByStepExercise 

import MySQLdb as mysql

#Inputs:
#circpath -> Path to the SPICE circuit
#imgpath -> Path to the image of the circuit
#questtext -> General question text
#questtype -> Type of question, either 'V' (Tension) , 'I' (Current), 'P' (Power)
#compname -> Name of the component that the question is about
#freq -> Circuit freq in hertz (freq=0 -> DC)
#This function handles all the backend operations to solve and store a question.
#It is strongly advised to surround this function with a try..except block
def handler(circpath,imgpath,questtext,questtype,compname,freq):
	#Get project dir
	project_path=dirname(realpath(__file__))

	#Connect to the DB
	_connect=mysql.connect(user='ele',passwd='itsucks',host='localhost', db='CIRCUITDB')
	_cursor=_connect.cursor()

	#Parse the SPICE file and run MNA to get solutions
	#circ -> circuit datastructure
	#mnastuff -> MNA related variables
	circ=run_parser(abspath(circpath))
	circ.calcImpedances(freq)
	mnastuff=mna(circ)

	#Get base resolution based on the circuit and solutions
	#baseres -> string with the general expanation
	baseres=stepByStepNA(circ,mnastuff['x'])

	print(relpath(abspath(circpath),project_path))
	#Insert into the DB the Cirucit
	_cursor.execute('CALL sp_CreateCircuit(%s,%s,%s,%s);',(relpath(abspath(circpath),project_path),relpath(abspath(imgpath),project_path),baseres,questtext))

	#Get the attributed circuit id (cid)
	cid=int(_cursor.fetchall()[0][0])
	print('CircuitID = '+str(cid))

	#should be a cycle
	#for prob in randomsolutions:
	#correct_answer=get_solution(circ,mnastuff,compname,questtype)

	#Run step by step resolution algorithm
	#correct_answer -> solution of the problem
	#specific_res -> string with the specific explanation
	correct_answer,specific_res=stepByStepExercise(circ,compname,questtype,mnastuff['x'])

	#Generate random wrong solutions based on the correct solution
	wss=randomWrongs(correct_answer,3)
	ws1=wss[0]
	ws2=wss[1]
	ws3=wss[2]

	#Insert into the DB the Exercise
	_cursor.execute('CALL sp_CreateExercise(%s,%s,%s,%s,%s,%s,%s,%s);',(cid,questtype,compname,correct_answer,ws1,ws2,ws3,specific_res))
	print(_cursor.fetchall())

#Main used for testing
def main(argv):
	handler(argv[1],argv[2],'Test question','V','R1',0)

if __name__ == '__main__':
        main(sys.argv)
