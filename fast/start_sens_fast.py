# -*- coding: utf-8 -*-
'''
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import spotpy
from spot_setup_fscabc import spot_setup

#Create samplers for every algorithm:
spot_setup=spot_setup()
rep=1400

sampler=spotpy.algorithms.fast(spot_setup,    dbname='sample01',    dbformat='csv',parallel='mpi')
sampler.sample(rep)
