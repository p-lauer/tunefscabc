# -*- coding: utf-8 -*-
'''
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import spotpy as spotpy2
from setup_fds_spotpy import spot_setup as spot_setup2

#Create samplers for every algorithm:
spot_setup2=spot_setup2()
rep=20000
db_name='{ID}'

sampler=spotpy2.algorithms.fscabc(spot_setup2,    dbname=db_name,    dbformat='csv')
sampler.sample(rep,eb=int({x0}),a={x1},peps=0.425,kpow=int({x2}),ownlimit=True,limit=int({x3}))
db_file=spotpy2.analyser.load_csv_results(db_name)
tomate=spotpy2.analyser.get_maxlikeindex(db_file)[1]

