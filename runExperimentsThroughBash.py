from ema_workbench.em_framework.samplers import sample_uncertainties
from OptimizedLevers.dpsFunction import lake_model as lake_problem
import sys
import math
import numpy as np
import pandas as pd

from scipy.optimize import brentq

from ema_workbench import (Model, RealParameter, ScalarOutcome, Constant,
                           ema_logging, MultiprocessingEvaluator,
                           CategoricalParameter, Scenario, Policy)
from ema_workbench import save_results

from Exploration import ExplorationEvaluator
from Exploration import TournamentExplorationSelector
from ema_workbench.em_framework.optimization import EpsNSGAII
from ema_workbench.em_framework.optimization import GenerationalBorg
from ema_workbench.em_framework.evaluators import MC
from ema_workbench.em_framework.evaluators import LHS
from datetime import datetime

                           
ema_logging.log_to_stderr(ema_logging.INFO)

policyList = [Policy('pol1', c1=-0.324375,c2=0.966297, r1=1.634259, r2=1.536966, w1=0.858481),
Policy('pol2', c1=0.677892,c2=0.116634, r1=1.497320, r2=0.445654, w1=0.770312), 
Policy('pol3', c1=0.317884,c2=0.005661, r1=0.457124, r2=0.820411, w1=0.646500), 
Policy('pol4', c1=0.835592,c2=0.258739, r1=1.855603, r2=0.102020, w1=0.532751), 
Policy('pol5', c1=1.057577,c2=-0.061549, r1=1.948418, r2=1.939679, w1=0.269329)
]

goalList = [[ScalarOutcome('max_P',
                                 kind=ScalarOutcome.MINIMIZE),  # @UndefinedVariable
                   ScalarOutcome('utility',
                                 kind=ScalarOutcome.MAXIMIZE),  # @UndefinedVariable
                   ScalarOutcome('inertia',
                                 kind=ScalarOutcome.MAXIMIZE),  # @UndefinedVariable
                   ScalarOutcome('reliability',
                                 kind=ScalarOutcome.MAXIMIZE)],  # @UndefinedVariable
                                [ScalarOutcome('max_P',
                                 kind=ScalarOutcome.MINIMIZE),  # @UndefinedVariable
                   ScalarOutcome('utility',
                                 kind=ScalarOutcome.MINIMIZE),  # @UndefinedVariable
                   ScalarOutcome('inertia',
                                 kind=ScalarOutcome.MINIMIZE),  # @UndefinedVariable
                   ScalarOutcome('reliability',
                                 kind=ScalarOutcome.MINIMIZE)],  # @UndefinedVariable
                                 [ScalarOutcome('max_P',
                                 kind=ScalarOutcome.MAXIMIZE),  # @UndefinedVariable
                   ScalarOutcome('utility',
                                 kind=ScalarOutcome.MAXIMIZE),  # @UndefinedVariable
                   ScalarOutcome('inertia',
                                 kind=ScalarOutcome.MAXIMIZE),  # @UndefinedVariable
                   ScalarOutcome('reliability',
                                 kind=ScalarOutcome.MAXIMIZE)]  # @UndefinedVariable
                                 ]

# instantiate the model
lake_model = Model('lakeproblem', function=lake_problem)
# specify uncertainties
lake_model.uncertainties = [RealParameter('b', 0.1, 0.45),
                        RealParameter('q', 2.0, 4.5),
                        RealParameter('mean', 0.01, 0.05),
                        RealParameter('stdev', 0.001, 0.005),
                        RealParameter('delta', 0.93, 0.99)]

# set levers
lake_model.levers = [RealParameter("c1", -2, 2),
                 RealParameter("c2", -2, 2),
                 RealParameter("r1", 0, 2),
                 RealParameter("r2", 0, 2),
                 RealParameter("w1", 0, 1)
                 ]
# specify outcomes
lake_model.outcomes = [ScalarOutcome('max_P',
                                 kind=ScalarOutcome.MINIMIZE),  # @UndefinedVariable
                   ScalarOutcome('utility',
                                 kind=ScalarOutcome.MAXIMIZE),  # @UndefinedVariable
                   ScalarOutcome('inertia',
                                 kind=ScalarOutcome.MAXIMIZE),  # @UndefinedVariable
                   ScalarOutcome('reliability',
                                 kind=ScalarOutcome.MAXIMIZE)]  # @UndefinedVariable

# override some of the defaults of the model
lake_model.constants = [Constant('alpha', 0.41),
                    Constant('reps', 100),
                    Constant('steps', 100), 
                    Constant('seed', None)]

# some policy reference determined in the optimization experiments
# print(sys.argv[1]) # which policy
# print(sys.argv[2]) # how many nfe? 
# print(sys.argv[3]) # novelty search or latin hypercube
# print(sys.argv[4]) # name to save results as
# print(sys.argv[5]) # What goals selected [0]=default, [1] = allMin [2]=allMax

savename = "Experiment_Policy"+str(sys.argv[1])+"-nfe"+str(sys.argv[2])+'-'+str(sys.argv[4])

if (len(sys.argv)>4):
   savename = str(sys.argv[4])+'-'+savename
   lake_model.outcomes = goalList[sys.argv[5]]

references = policyList[int(sys.argv[1])]
nfe=int(sys.argv[2])

if(sys.argv[3]=='True'):
    savename = "NoveltySearch-"+str(savename)
    now = datetime.now()
    startNovelty = now.strftime("%H:%M:%S")


    with ExplorationEvaluator(lake_model) as evaluator:
            results = evaluator.explore(searchover='uncertainties', nfe=nfe,
                            epsilons=[0.1, ] * len(lake_model.outcomes), reference = references,
                            algorithm=GenerationalBorg, selector=TournamentExplorationSelector(2))

    now = datetime.now()

    endNovelty = now.strftime("%H:%M:%S")
                
    results.to_csv("Results/"+savename+".csv")
    print(startNovelty+" until: "+endNovelty)
    with open('Results/timetable.txt', 'a') as f:
        f.write(savename+" from: "+str(startNovelty)+"until: "+str(endNovelty)+'\n' )
else:
    savename = "LHC-"+str(savename)
    now = datetime.now()

    startLHC = now.strftime("%H:%M:%S")

    with MultiprocessingEvaluator(lake_model) as evaluator:
            res = evaluator.perform_experiments(scenarios=nfe, policies=references)

    now = datetime.now()

    endLHC = now.strftime("%H:%M:%S")

    save_results(res,"Results/"+savename+'.tar.gz')

    print(startLHC+" until: "+endLHC)
    
    with open('Results/timetable.txt', 'a') as f:
        f.write(savename+" from: "+str(startLHC)+"until: "+str(endLHC)+'\n')