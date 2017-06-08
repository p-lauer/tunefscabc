from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import numpy as np
import spotpy
import random
import subprocess
import os
import time
        
class spot_setup(object):
    def __init__(self):
        self.params = [spotpy.parameter.Uniform('eb', 1, 500, 1.5, 3.0, 1, 500),
                       spotpy.parameter.Uniform('a', 0.01, 1, 1.5, 3.0, 0.01, 10),
                       spotpy.parameter.Uniform('kpow', 1, 20, 1.5, 3.0, 1, 20),
                       spotpy.parameter.Uniform('limit', 1, 100, 1.5, 3.0, 1, 100)
                       ]
    def parameters(self):
        return spotpy.parameter.generate(self.params)

    def file_len(self,fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def simulation(self,vector,id=(random.randint(50000,500000))):      
        zcall=id
        rnd=random.randint(50000,500000)
        zcall=str(zcall)+str(rnd)
        str_zcall = str(zcall) + '.py'
        in_zcall = str(zcall) + '.in'
        inputfile=open(in_zcall,'w')
        acount = sum(1 for a in vector)
        inputfile.write('{ID'+ '='+str(zcall)+'}')
        inputfile.write('\n')
        print(vector)
        vector[0]=int(round(vector[0]))
        vector[2]=int(round(vector[2]))
        vector[3]=int(round(vector[3]))
        print(vector)
        for aa in range(acount):
            inputfile.write('{x'+ str(aa)+ '='+str(vector[aa])+'}')
            inputfile.write('\n')
        inputfile.flush()
        inputfile.close()        
        os.mkdir('./sims/'+str(zcall), 0755)
        subprocess.check_call(['perl','dprepro',in_zcall,'template.tpl','./sims/'+str(zcall)+'/'+str_zcall])
        os.chdir('sims')
        subprocess.check_call(['cp -r template/* '+ str(zcall)+'/'],shell = True)
        os.chdir(str(zcall))
        locals=dict()
        execfile(str_zcall,dict(),locals)
        #subprocess.check_call(['python',str_zcall])
        #time.sleep(10)
        simulations=[]
        simulations.append(self.file_len(str(zcall)+'.csv'))
        simulations.append(locals['tomate'])
        try:
            subprocess.check_call('rm '+ str(zcall) +'.py', shell=True)
        except subprocess.CalledProcessError:
            pass
        try:
            subprocess.check_call('rm '+ str(zcall) +'.csv', shell=True)
        except subprocess.CalledProcessError:
            pass
        os.chdir('../')
        try:
            subprocess.check_call('rm -r '+ str(zcall), shell=True)
        except subprocess.CalledProcessError:
            pass
        os.chdir('../')
        try:
            subprocess.check_call('rm '+ str(zcall) +'.in', shell=True)
        except subprocess.CalledProcessError:
            pass


        return simulations
        
    def evaluation(self):
        observations= []
        observations.append(0)
        observations.append(0)
        return observations
    
    def objectivefunction(self, simulation = simulation, evaluation = evaluation):
        objectivefunction = -spotpy.objectivefunctions.rmse(evaluation = evaluation, simulation = simulation)      
        return objectivefunction
