from os.path import abspath,realpath,dirname,join
import sys
from datastructure import Circuit,Branch,Component

#Get project dir
project_path=dirname(realpath(__file__))

sys.path+=[join(project_path,'parser/')]
from spiceProcessor import spiceLexer, run_parser

sys.path+=[join(project_path,'mna/')]
from mna.randSol import *

sys.path+=[join(project_path,'explainer/')]
from explainer.toplevelcaller import general_ressol,specific_ressol 


def handler(circpath, teacher, theme, question, public, target, freq, unit=None):
    #Parse the SPICE file and run MNA to get solutions
    #circ -> circuit datastructure
    circ=run_parser(abspath(circpath))
    circ.calcImpedances(freq)
    
	#Get base resolution based on the circuit and solutions
    if unit==None:
        resol = general_ressol(circ)
        exe= {
            "teacher": teacher,
            "theme": theme,
            "question": question,
            "ans1": None,
            "ans2": None,
            "ans3": None,
            "correct": None,
            "unit": unit,
            "resol": resol,
            "public": public
        }
    else:
        #should be a cycle
        #for prob in randomsolutions:
        #correct_answer=get_solution(circ,mnastuff,target,questtype)
        resol = general_ressol(circ)
        #Run step by step resolution algorithm
        #correct_answer -> solution of the problem
        #specific_res -> string with the specific explanation
        correct_answer,resol_spec=specific_ressol(circ,target,unit)
        resol += resol_spec

        if type(correct_answer)==tuple or type(correct_answer)==list:
            for a in correct_answer:
                a=abs(a)
        else:
            correct_answer=abs(correct_answer)

        #Generate random wrong solutions based on the correct solution
        ans=randomWrongs(correct_answer,3)

        exe= {
            "teacher": teacher,
            "theme": theme,
            "question": question,
            "ans1": "{:0.5f}".format(ans[0]),
            "ans2": "{:0.5f}".format(ans[1]),
            "ans3": "{:0.5f}".format(ans[2]),
            "correct": "{:0.5f}".format(correct_answer),
            "unit": unit,
            "resol": resol,
            "public": public
        }
    print(exe)
    #Ideal case: use serialization to save the circuit and the solutions
    return exe

#Main used for testing
def main(argv):
    if len(argv)<9:
        print('Usage: python '+argv[0]+' <SPICE circuit> <circuit image> <target> <frequency>')
        print('Example: python '+argv[0]+' examples/example2_AC.cir test.png C1 400')
        print('Example: python '+argv[0]+' examples/exampleThevenin.cir test.png 3,0 0 (For Norton or Thevenin)')
        print('Example: python '+argv[0]+' examples/exampleTransient.cir test.png R10 10s (For transient analyis)')
        print("->circpath, teacher, theme, question, public, target, freq, unit(optionals) ")
        #python3 mytopcaller.py examples/example2_AC.cir 1 1 question1 1 C1 400 V 
        return
    if len(argv)==10:
        return handler(argv[1],argv[2],argv[3],argv[4],argv[5],argv[7],argv[8],argv[9],argv[6])
    else:
        return handler(argv[1],argv[2],argv[3],argv[4],argv[5],argv[6],argv[7],argv[8])  

    if(len(argv[3].split(','))==2):
        print('T')
        handler(argv[1],argv[2],'Test question','T',argv[3].split(','),float(argv[4]))
        print('N')
        handler(argv[1],argv[2],'Test question','N',argv[3].split(','),float(argv[4]))
    elif argv[4][-1]=='s' and argv[4][:-1].replace('.','',1).isdigit():
        print('Transient')
        handler(argv[1],argv[2],'Test question','Trans',argv[3],float(argv[4][:-1]))
    else:
        print('V')
        handler(argv[1],argv[2],'Test question','V',argv[3],float(argv[4]))
        print('I')
        handler(argv[1],argv[2],'Test question','I',argv[3],float(argv[4]))
        print('P')
        handler(argv[1],argv[2],'Test question','P',argv[3],float(argv[4]))
		
if __name__ == '__main__':
        main(sys.argv)
