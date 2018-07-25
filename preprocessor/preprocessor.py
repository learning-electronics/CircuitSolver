import sys
from datastructure import Circuit,Branch,Component

sys.path+=['parser/']
from spiceProcessor import run_parser

sys.path+=['mna/']
from mnaModule import mna
from respSel import get_solution 

import MySQLdb as mysql

def handler(circpath,imgpath,questtext,questtype,compname):
	_connect=mysql.connect(user='ele',passwd='itsucks',host='localhost', db='CIRCUITDB')
	_cursor=_connect.cursor()

	circ=run_parser(circpath)
	mnastuff=mna(circ)
	#print(mnastuff)

	#get base resolution
	baseres="This is the base resolution"

	sqlquery='CALL sp_CreateCircuit(\''+circpath+'\',\''+imgpath+'\',\''+baseres+'\',\''+questtext+'\');'
	print(sqlquery)
	_cursor.execute(sqlquery)

	cid=_cursor.fetchall()[0][0]
	print('CircuitID = '+str(cid))

	#should be a cycle
	#for prob in randomsolutions:
	correct_answer=get_solution(circ,mnastuff,compname,questtype)

	#TODO
	ws1=-1
	ws2=-2
	ws3=-3

	specific_res='rip'

	sqlquery='CALL sp_CreateExercise('+str(cid)+',\''+questtype+'\',\''+compname+'\','+str(correct_answer)+','+str(ws1)+','+str(ws2)+','+str(ws3)+',\''+specific_res+'\');'
	print(sqlquery)
	_cursor.execute(sqlquery)
	print(_cursor.fetchall())

def main(argv):
	handler('example1.cir','cir.png','Test question','V','R1')

if __name__ == '__main__':
        main(sys.argv)
