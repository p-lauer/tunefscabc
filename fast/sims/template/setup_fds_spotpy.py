'''
:author: Patrick Lauer

This file implements FDS into SPOTpy.  
'''

import numpy as np
import spotpy
import csv
import subprocess
import sys
import random
import os
import glob


        
class spot_setup(object):
    slow = 0
    counter = 0

#Eingabeparameter
    def __init__(self):
        self.params = [spotpy.parameter.Uniform('x0',200,400,1,280,200,400),
                       spotpy.parameter.Uniform('x1', 50,200,1,105, 50,200),
                       spotpy.parameter.Uniform('x2',250,450,1,365,250,450),
                       spotpy.parameter.Uniform('x3', 50,200,1,115, 50,200),
                       spotpy.parameter.Uniform('x4',550,750,1,630,550,750),
                       spotpy.parameter.Uniform('x5', 20,200,1, 80, 20,200)]
    def parameters(self):
        return spotpy.parameter.generate(self.params)
        

#Simulation
    def simulation(self,vector,id=(random.randint(50000,500000))):      
        zcall=id
        rnd=random.randint(50000,500000)
        #print str(vector)
        #print str(zcall)
        zcall=str(zcall)+str(rnd)
        str_zcall = str(zcall) + '.fds'
        in_zcall = str(zcall) + '.in'

        inputfile=open(in_zcall,'w')
        inputfile.write('{ID'+ '='+str(zcall)+'}')
        inputfile.write('\n')
        acount = sum(1 for a in vector)
        for aa in range(acount):
            inputfile.write('{x'+ str(aa)+ '='+str(vector[aa])+'}')
            inputfile.write('\n')
        inputfile.flush()
        inputfile.close()
    
        subprocess.check_call(['perl','dprepro',in_zcall,'PU_5_p_TRUE.fds','./sims/'+str_zcall])
        os.chdir('sims')
        ##Simulation (evtl. Binary anpassen)
        subprocess.check_call(['./fds',str_zcall])
        ##Simulationsdaten laden (Anpassen an CHID)
        simdata=[]
        simdata.extend(csv.reader(open('PU_5K_Staub_N2_'+ str(zcall) +'_tga.csv','r'), delimiter=','))
        del simdata[0]
        del simdata[0]
        simulations = []
        

        for data in simdata:
            simulations.append(float(data[2])*100)
        files=glob.glob('PU_5K_Staub_N2_'+ str(zcall) +'*')
        ###subprocess.check_call('tar -cf archiv'+str(zcall)+'.tar PU_5K_Staub_N2_'+ str(zcall) +'*', shell=True)
        try:
            subprocess.check_call('rm '+ str(zcall) +'.fds', shell=True)
        except subprocess.CalledProcessError:
            pass
        subprocess.check_call('rm PU_5K_Staub_N2_'+ str(zcall) +'*', shell=True)
        try:
            subprocess.check_call('rm '+ str(zcall) +'.fds', shell=True)
        except subprocess.CalledProcessError:
            pass
        os.chdir('../')
        try:
            subprocess.check_call('rm '+ str(zcall) +'.in', shell=True)
        except subprocess.CalledProcessError:
            pass
        return simulations
        
    def evaluation(self):
        trydata = open("vorlage.txt")
        observations=[]
        for line in trydata:
            observations.append(float(line))
        return observations
    
    def objectivefunction(self, simulation = simulation, evaluation = evaluation):
        objectivefunction = -spotpy.objectivefunctions.rmse(evaluation = evaluation, simulation = simulation)      
        return objectivefunction
