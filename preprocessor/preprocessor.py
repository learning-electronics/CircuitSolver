import sys
from datastructure import Circuit,Branch,Component

sys.path+=['parser/']
from spiceProcessor import run_parser

sys.path+=['mna/']
from mnaModule import mna
from respSel import get_solution 

sys.path+=['explainer/']
from circuit2na import stepByStepNA 

import MySQLdb as mysql

def handler(circpath,imgpath,questtext,questtype,compname):
	_connect=mysql.connect(user='ele',passwd='itsucks',host='localhost', db='CIRCUITDB')
	_cursor=_connect.cursor()

	circ=run_parser(circpath)
	mnastuff=mna(circ)
	#print(mnastuff)

	#get base resolution
	baseres=stepByStepNA(circ)

	_cursor.execute('CALL sp_CreateCircuit(%s,%s,%s,%s);',(circpath,imgpath,baseres,questtext))

	cid=int(_cursor.fetchall()[0][0])
	print('CircuitID = '+str(cid))

	#should be a cycle
	#for prob in randomsolutions:
	correct_answer=get_solution(circ,mnastuff,compname,questtype)

	#TODO
	ws1=-1
	ws2=-2
	ws3=-3

	specific_res='rip'

	_cursor.execute('CALL sp_CreateExercise(%s,%s,%s,%s,%s,%s,%s,%s);',(cid,questtype,compname,correct_answer,ws1,ws2,ws3,specific_res))
	print(_cursor.fetchall())

def main(argv):
	handler(argv[1],'cir.png','Test question','V','R1')

if __name__ == '__main__':
        main(sys.argv)
