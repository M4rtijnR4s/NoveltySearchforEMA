from ema_workbench.em_framework.optimization import GenerationalBorg as Borg
from ema_workbench.em_framework.evaluators import optimize
import random
import math
import copy
from sklearn.metrics.pairwise import manhattan_distances
import numpy as np

from ema_workbench import MultiprocessingEvaluator as Evaluator
# from ema_workbench import MultiprocessingEvaluator as Evaluator
'''
Alter class and create altered optimization function to clarify that it is about exploration. 
Borg is set as default algorithm and searchover is uncertainties by default. Everything else is the sme as all other evaluators.

extends the multiprocessingevaluator from the ema workbench
'''
class ExplorationEvaluator(Evaluator):

	def explore(self, algorithm=Borg, nfe=10000, searchover='uncertainties',
                 reference=None, constraints=None, convergence_freq=1000,
                 logging_freq=5, **kwargs):

		return optimize(self._msis, algorithm=algorithm, nfe=int(nfe),
                        searchover=searchover, evaluator=self,
                        reference=reference, constraints=constraints,
                        convergence_freq=convergence_freq,
                        logging_freq=logging_freq, **kwargs)


# from ema_workbench.em_framework.optimization import TournamentSelector as Selector
# from platypus.core import Selector
from platypus.core import ParetoDominance
from platypus.operators import TournamentSelector

'''
Extends the tournamentSelector from platypusOpt

Assumption is to have only two parents (hence the dirty fix with count works)

Only function to be adjusted is the select_one. 
We now select based on the novelty function to have the most novel parents create children. 
First parent is most novel, second parent is by definition not the most novel, 
second parent is not equal to first parent, and is closer to first parent, thus allowed to have lower crowding distance.
'''
class TournamentExplorationSelector(TournamentSelector):

	count = 0

	def select_one(self, population):
		self.count+=1
		
		from platypus.core import crowding_distance
		crowding_distance(population)
		winner = random.choice(population)
		if self.count % 2 == 1:
			if math.isinf(winner.crowding_distance):
				self.previous = winner
				return winner
		
			for _ in range(self.tournament_size-1):
				candidate = random.choice(population)
				if candidate.crowding_distance > winner.crowding_distance:
					winner = candidate
			self.previous = winner

		else:
			base = self.previous.objectives
			base_dist = manhattan_distances([base],[winner.objectives])
			for _ in range(self.tournament_size-1):
				candidate = random.choice(population)
				new_dist = manhattan_distances([base], [candidate.objectives])
				if(base_dist==0 and new_dist>0):
					base_dist = new_dist
					winner = candidate
				elif(new_dist>0 and new_dist<base_dist):
					base_dist = new_dist
					winner = candidate
				
		return winner