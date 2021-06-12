'''
An example of the lake problem using the ema workbench.

The model itself is adapted from the Rhodium example by Dave Hadka,
see https://gist.github.com/dhadka/a8d7095c98130d8f73bc

'''
import math

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from OptimizedLevers.dpsFunction import lake_model as lake_problemCython

from ema_workbench import (Model, RealParameter, ScalarOutcome, Constant, Policy, Scenario, 
                           ema_logging, MultiprocessingEvaluator, CategoricalParameter)
from ema_workbench.em_framework.evaluators import MC
from ema_workbench import save_results

def avg(lst):
    return sum(lst) / len(lst)

def lake_problem(
    b=0.42,          # decay rate for P in lake (0.42 = irreversible)
    q=2.0,           # recycling exponent
    mean=0.02,       # mean of natural inflows
    stdev=0.001,     # future utility discount rate
    delta=0.98,      # standard deviation of natural inflows
    alpha=0.4,       # utility from pollution
    nsamples=100,    # Monte Carlo sampling of natural inflows
        **kwargs):
    try:
        decisions = [kwargs[str(i)] for i in range(100)]
    except KeyError:
        decisions = [0, ] * 100

    Pcrit = brentq(lambda x: x**q / (1 + x**q) - b * x, 0.01, 1.5)
    nvars = len(decisions)
    X = np.zeros((nvars,))
    average_daily_P = np.zeros((nvars,))
    decisions = np.array(decisions)
    reliability = 0.0

    for _ in range(nsamples):
        X[0] = 0.0

        natural_inflows = np.random.lognormal(
            math.log(mean**2 / math.sqrt(stdev**2 + mean**2)),
            math.sqrt(math.log(1.0 + stdev**2 / mean**2)),
            size=nvars)

        for t in range(1, nvars):
            X[t] = (1 - b) * X[t - 1] + X[t - 1]**q / (1 + X[t - 1]**q) + \
                decisions[t - 1] + natural_inflows[t - 1]
            average_daily_P[t] += X[t] / float(nsamples)

        reliability += np.sum(X < Pcrit) / float(nsamples * nvars)

    max_P = np.max(average_daily_P)
    utility = np.sum(alpha * decisions * np.power(delta, np.arange(nvars)))
    inertia = np.sum(np.absolute(np.diff(decisions)) < 0.02) / float(nvars - 1)

    return max_P, utility, inertia, reliability


if __name__ == '__main__':
    ema_logging.log_to_stderr(ema_logging.INFO)

    # instantiate the model
    lake_model = Model('lakeproblem', function=lake_problemCython)
    # lake_model.time_horizon = 100

    # specify uncertainties
    lake_model.uncertainties = [RealParameter('b', 0.1, 0.45),
                                RealParameter('q', 2.0, 4.5),
                                RealParameter('mean', 0.01, 0.05),
                                RealParameter('stdev', 0.001, 0.005),
                                RealParameter('delta', 0.93, 0.99)]

    # set levers, one for each time step
    lake_model.levers = [RealParameter("c1", -2, 2),
                         RealParameter("c2", -2, 2),
                         RealParameter("r1", 0, 2),
                         RealParameter("r2", 0, 2),
                         RealParameter("w1", 0, 1)
                         ]

    # specify outcomes
    lake_model.outcomes = [ScalarOutcome('max_P',),
                           ScalarOutcome('utility'),
                           ScalarOutcome('inertia'),
                           ScalarOutcome('reliability')]

    # override some of the defaults of the model For normal
    # lake_model.constants = [Constant('alpha', 0.41),
    #                         Constant('nsamples', 100)]

    # override some of the defaults of the model For cython
    lake_model.constants = [Constant('alpha', 0.41),
                    Constant('reps', 100),
                    Constant('steps', 100), 
                    Constant('seed', None)]

    # generate some random policies by sampling over levers
    n_scenarios = 100000
    scenarioReference = [Scenario('scenarioReference0', b=0.3569907160294662, q=4.5, mean=0.05, stdev=0.0010509606239627, delta=0.9899999961789584),
Scenario('scenarioReference1', b=0.3634450631260745, q=4.499617441797741, mean=0.0498764237853059, stdev=0.0010682668803204, delta=0.9899999550991438),
Scenario('scenarioReference2', b=0.45, q=2.621292382762292, mean=0.049752473093891, stdev=0.001, delta=0.99),
Scenario('scenarioReference3', b=0.45, q=4.10885281027123, mean=0.0404130443409147, stdev=0.001, delta=0.9899999930165314),
Scenario('scenarioReference4', b=0.45, q=2.0, mean=0.0234851301665161, stdev=0.001, delta=0.99),
Scenario('scenarioReference5', b=0.362071679837997, q=4.49956653354773, mean=0.0499998359446319, stdev=0.0010055369580853, delta=0.9899911518172346),
Scenario('scenarioReference6', b=0.3633614847239376, q=4.4997365064078965, mean=0.0499999277431624, stdev=0.0010055369580853, delta=0.9899910115243484),
Scenario('scenarioReference7', b=0.3602477471962437, q=4.5, mean=0.05, stdev=0.0010002084888193, delta=0.989999469469306),
Scenario('scenarioReference8', b=0.4499942173714698, q=2.788028178006221, mean=0.0499942699122895, stdev=0.0010178089415438, delta=0.9899999979046116),
Scenario('scenarioReference9', b=0.45, q=2.0, mean=0.0135737346024443, stdev=0.001, delta=0.99),
Scenario('scenarioReference10', b=0.45, q=2.0, mean=0.0169347547461444, stdev=0.001, delta=0.99),
Scenario('scenarioReference11', b=0.45, q=2.00612079945004, mean=0.0387867232492596, stdev=0.0010170456421597, delta=0.9899995778341774),
Scenario('scenarioReference12', b=0.3742947622613507, q=4.484051031696184, mean=0.0499937813987234, stdev=0.0010531304566715, delta=0.989999873387762),
Scenario('scenarioReference13', b=0.3501857035134059, q=4.499999818365104, mean=0.0498853964386582, stdev=0.001, delta=0.9899909271144828)]
    policyReference = Policy('policyReference', c1=-0.324375, c2=0.966297, r1=1.634259, r2=1.536966, w1=0.858481)
    

    with MultiprocessingEvaluator(lake_model) as evaluator:
        res = evaluator.perform_experiments(scenarios=scenarioReference, policies=policyReference)

    save_results(res, 'Results/UnexpectedExperiments/unexpectedEntry-pol0.tar.gz')

    resIn, resOut = res
    output2 = pd.DataFrame.from_dict(resIn) 
    output = pd.DataFrame.from_dict(resOut)
    print(output)
    print(output2)
    # output2.to_csv("nonOptimizedFirst_4-1000_inpt-2.csv")
    # output.to_csv("nonOptimizedFirst_4-1000-output-3.csv")
    # # print(resOut)
    # pMaxOut = max(resOut['max_P'])
    # pMinOut = min(resOut['max_P'])
    # pAvgOut = avg(resOut['max_P'])
    # print(pMaxOut)
    # print(pMinOut)
    # print(pAvgOut)
    # intertiaMaxOut = max(resOut['inertia'])
    # intertiaMinOut = min(resOut['inertia'])
    # intertiaAvgOut = avg(resOut['inertia'])
    # print(intertiaMaxOut)
    # print(intertiaMinOut)
    # print(intertiaAvgOut)
    # utilityMaxOut = max(resOut['utility'])
    # utilityMinOut = min(resOut['utility'])
    # utilityAvgOut = avg(resOut['utility'])
    # print(utilityMaxOut)
    # print(utilityMinOut)
    # print(utilityAvgOut)
    # reliabilityMaxOut = max(resOut['reliability'])
    # reliabilityMinOut = min(resOut['reliability'])
    # reliabilityAvgOut = avg(resOut['reliability'])
    # print(reliabilityMaxOut)
    # print(reliabilityMinOut)
    # print(reliabilityAvgOut)
