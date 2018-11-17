from os.path import abspath,realpath,relpath,dirname,join
import sys
from datastructure import Circuit,Branch,Component

#Get project dir
project_path=dirname(realpath(__file__))

sys.path+=[join(project_path,'parser/')]
from spiceProcessor import run_parser

sys.path+=[join(project_path,'mna/')]
from randSol import randomWrongs

sys.path+=[join(project_path,'explainer/')]
from toplevelcaller import general_ressol,specific_ressol 

import MySQLdb as mysql

#Inputs:
#circpath -> Path to the SPICE circuit
#imgpath -> Path to the image of the circuit
#questtext -> General question text
#questtype -> Type of question, either 'V' (Tension) , 'I' (Current), 'P' (Power), 'T' (Thevenin Equivalent), 'N' (Norton Equivalent)
#target -> Name of the component or nodes(thevenin/norton) that the question is about FIXME
#freq -> Circuit freq in hertz (freq=0 -> DC)
#This function handles all the backend operations to solve and store a question.
#It is strongly advised to surround this function with a try..except block
def handler(circpath,imgpath,questtext,questtype,target,freq):
	#Get project dir
	project_path=dirname(realpath(__file__))

	#Connect to the DB
	_connect=mysql.connect(user='ele',passwd='itsucks',host='localhost', db='CIRCUITDB')
	_cursor=_connect.cursor()

	#Parse the SPICE file and run MNA to get solutions
	#circ -> circuit datastructure
	circ=run_parser(abspath(circpath))
	circ.calcImpedances(freq)

	#Get base resolution based on the circuit and solutions
	#baseres -> string with the general expanation
	baseres=general_ressol(circ)

	#print(relpath(abspath(circpath),project_path))
	#Insert into the DB the Cirucit
	_cursor.execute('CALL sp_CreateCircuit(%s,%s,%s,%s);',(relpath(abspath(circpath),project_path),relpath(abspath(imgpath),project_path),baseres,questtext))

	#Get the attributed circuit id (cid)
	cid=int(_cursor.fetchall()[0][0])
	print('CircuitID = '+str(cid))

	#should be a cycle
	#for prob in randomsolutions:
	#correct_answer=get_solution(circ,mnastuff,target,questtype)

	#Run step by step resolution algorithm
	#correct_answer -> solution of the problem
	#specific_res -> string with the specific explanation
	correct_answer,specific_res=specific_ressol(circ,target,questtype)

	correct_answer=abs(correct_answer) #FIXME be careful with future implementations
	print('correct_answer=',correct_answer)

	#Generate random wrong solutions based on the correct solution
	ws=randomWrongs(correct_answer,3)

	#Insert into the DB the Exercise
	_cursor.execute('CALL sp_CreateExercise(%s,%s,%s,%s,%s,%s,%s,%s);',(cid,questtype,target,correct_answer,ws[0],ws[1],ws[2],specific_res))
	print('ExerciseID =',_cursor.fetchall()[0][0])

#Main used for testing
def main(argv):
	if len(argv)!=5:
		print('Usage: python '+argv[0]+' <SPICE circuit> <circuit image> <targetcomp> <frequency>')
		print('Example: python '+argv[0]+' examples/example2_AC.cir test.png C1 400')
		return

	print('V')
	handler(argv[1],argv[2],'Test question','V',argv[3],float(argv[4]))
	print('I')
	handler(argv[1],argv[2],'Test question','I',argv[3],float(argv[4]))
	print('P')
	handler(argv[1],argv[2],'Test question','P',argv[3],float(argv[4]))
	#crashes it

if __name__ == '__main__':
        main(sys.argv)
