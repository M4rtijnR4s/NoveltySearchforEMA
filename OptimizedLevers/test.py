from dpsFunction import lake_model as lake_problem
import math
import numpy as np

from scipy.optimize import brentq

from ema_workbench import (Model, RealParameter, ScalarOutcome, Constant,
                           ema_logging, MultiprocessingEvaluator,
                           CategoricalParameter, Scenario)
                           
ema_logging.log_to_stderr(ema_logging.INFO)

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

# reference is optional, but can be used to implement search for
# various user specified scenarios along the lines suggested by
# Watson and Kasprzyk (2017)
reference = Scenario('reference', b=0.4, q=2, mean=0.02, stdev=0.01)

with MultiprocessingEvaluator(lake_model) as evaluator:
	results = evaluator.optimize(searchover='levers', nfe=1000000,
                   epsilons=[0.1, ] * len(lake_model.outcomes),
                   reference=reference)


print(results.columns)
results.to_csv("Results/Optimized-test-noseed.csv")


# override some of the defaults of the model
lake_model.constants = [Constant('alpha', 0.41),
                    Constant('reps', 100),
                    Constant('steps', 100), 
                    Constant('seed', 0)]

# reference is optional, but can be used to implement search for
# various user specified scenarios along the lines suggested by
# Watson and Kasprzyk (2017)
reference = Scenario('reference', b=0.4, q=2, mean=0.02, stdev=0.01)

with MultiprocessingEvaluator(lake_model) as evaluator:
	results = evaluator.optimize(searchover='levers', nfe=1000000,
                   epsilons=[0.1, ] * len(lake_model.outcomes),
                   reference=reference)


print(results.columns)
results.to_csv("Results/Optimized-test-seed-0.csv")


# override some of the defaults of the model
lake_model.constants = [Constant('alpha', 0.41),
                    Constant('reps', 100),
                    Constant('steps', 100), 
                    Constant('seed', 1)]

# reference is optional, but can be used to implement search for
# various user specified scenarios along the lines suggested by
# Watson and Kasprzyk (2017)
reference = Scenario('reference', b=0.4, q=2, mean=0.02, stdev=0.01)

with MultiprocessingEvaluator(lake_model) as evaluator:
	results = evaluator.optimize(searchover='levers', nfe=1000000,
                   epsilons=[0.1, ] * len(lake_model.outcomes),
                   reference=reference)


print(results.columns)
results.to_csv("Results/Optimized-test-seed-1.csv")

# override some of the defaults of the model
lake_model.constants = [Constant('alpha', 0.41),
                    Constant('reps', 100),
                    Constant('steps', 100), 
                    Constant('seed', 2)]

# reference is optional, but can be used to implement search for
# various user specified scenarios along the lines suggested by
# Watson and Kasprzyk (2017)
reference = Scenario('reference', b=0.4, q=2, mean=0.02, stdev=0.01)

with MultiprocessingEvaluator(lake_model) as evaluator:
	results = evaluator.optimize(searchover='levers', nfe=1000000,
                   epsilons=[0.1, ] * len(lake_model.outcomes),
                   reference=reference)


print(results.columns)
results.to_csv("Results/Optimized-test-seed-2.csv")

# override some of the defaults of the model
lake_model.constants = [Constant('alpha', 0.41),
                    Constant('reps', 100),
                    Constant('steps', 100), 
                    Constant('seed', 3)]

# reference is optional, but can be used to implement search for
# various user specified scenarios along the lines suggested by
# Watson and Kasprzyk (2017)
reference = Scenario('reference', b=0.4, q=2, mean=0.02, stdev=0.01)

with MultiprocessingEvaluator(lake_model) as evaluator:
	results = evaluator.optimize(searchover='levers', nfe=1000000,
                   epsilons=[0.1, ] * len(lake_model.outcomes),
                   reference=reference)


print(results.columns)
results.to_csv("Results/Optimized-test-seed-3.csv")

# override some of the defaults of the model
lake_model.constants = [Constant('alpha', 0.41),
                    Constant('reps', 100),
                    Constant('steps', 100), 
                    Constant('seed', 4)]

# reference is optional, but can be used to implement search for
# various user specified scenarios along the lines suggested by
# Watson and Kasprzyk (2017)
reference = Scenario('reference', b=0.4, q=2, mean=0.02, stdev=0.01)

with MultiprocessingEvaluator(lake_model) as evaluator:
	results = evaluator.optimize(searchover='levers', nfe=1000000,
                   epsilons=[0.1, ] * len(lake_model.outcomes),
                   reference=reference)


print(results.columns)
results.to_csv("Results/Optimized-test-seed-4.csv")


# override some of the defaults of the model
lake_model.constants = [Constant('alpha', 0.41),
                    Constant('reps', 100),
                    Constant('steps', 100), 
                    Constant('seed', 5)]

# reference is optional, but can be used to implement search for
# various user specified scenarios along the lines suggested by
# Watson and Kasprzyk (2017)
reference = Scenario('reference', b=0.4, q=2, mean=0.02, stdev=0.01)

with MultiprocessingEvaluator(lake_model) as evaluator:
	results = evaluator.optimize(searchover='levers', nfe=1000000,
                   epsilons=[0.1, ] * len(lake_model.outcomes),
                   reference=reference)


print(results.columns)
results.to_csv("Results/Optimized-test-seed-5.csv")
