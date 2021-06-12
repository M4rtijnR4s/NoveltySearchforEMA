#!/bin/bash

## Source/activate the python virtual environment 
source "/home/martijn/Documents/Work/CoronaPersonalStealing/NoveltySearchEMA/venv/bin/activate"

## Run optimization tests.
# python runOptimizationThroughBash.py 0 1000000
# python runOptimizationThroughBash.py 1 1000000
# python runOptimizationThroughBash.py 2 1000000
# python runOptimizationThroughBash.py 3 1000000
# python runOptimizationThroughBash.py 4 1000000

## Test and clarification
##    *          Function to call       policy nfe NS --> true, LHC--> False 
# # python runExperimentsThroughBash.py 0 1000 False # test 1
##    *          Function to call       policy nfe NS --> true, LHC--> False    Extra name      Which goals
# # python runExperimentsThroughBash.py 0 1000 False AllMin 1 # test 2


# # policy 1
## Run once with 1000000 to 1000
python runExperimentsThroughBash.py 0 1000000 True 
# python runExperimentsThroughBash.py 0 100000 True
# python runExperimentsThroughBash.py 0 10000 True 
# python runExperimentsThroughBash.py 0 1000 True 
python runExperimentsThroughBash.py 0 1000000 False
# python runExperimentsThroughBash.py 0 100000 False
# python runExperimentsThroughBash.py 0 10000 False 
# python runExperimentsThroughBash.py 0 1000 False 

## Run with different goals
# python runExperimentsThroughBash.py 0 1000000 True 'allMin' 1
# python runExperimentsThroughBash.py 0 1000000 True 'allMax' 2

# # policy 2
## Run once with 1000000 to 1000
python runExperimentsThroughBash.py 1 1000000 True 
# python runExperimentsThroughBash.py 1 100000 True
# python runExperimentsThroughBash.py 1 10000 True 
# python runExperimentsThroughBash.py 1 1000 True 
python runExperimentsThroughBash.py 1 1000000 False
# python runExperimentsThroughBash.py 1 100000 False
# python runExperimentsThroughBash.py 1 10000 False 
# python runExperimentsThroughBash.py 1 1000 False 

## Run with different goals
# python runExperimentsThroughBash.py 1 1000000 True 'allMin' 1
# python runExperimentsThroughBash.py 1 1000000 True 'allMax' 2
# # # policy 3
## Run once with 1000000 to 1000
python runExperimentsThroughBash.py 2 1000000 True 
# python runExperimentsThroughBash.py 2 100000 True
# python runExperimentsThroughBash.py 2 10000 True 
# python runExperimentsThroughBash.py 2 1000 True 
python runExperimentsThroughBash.py 2 1000000 False
# python runExperimentsThroughBash.py 2 100000 False
# python runExperimentsThroughBash.py 2 10000 False 
# python runExperimentsThroughBash.py 2 1000 False 

## Run with different goals
python runExperimentsThroughBash.py 2 1000000 True 'allMin' 1
python runExperimentsThroughBash.py 2 1000000 True 'allMax' 2

# # # policy 4
## Run once with 1000000 to 1000
python runExperimentsThroughBash.py 3 1000000 True 
# python runExperimentsThroughBash.py 3 100000 True
# python runExperimentsThroughBash.py 3 10000 True 
# python runExperimentsThroughBash.py 3 1000 True 
python runExperimentsThroughBash.py 3 1000000 False
# python runExperimentsThroughBash.py 3 100000 False
# python runExperimentsThroughBash.py 3 10000 False 
# python runExperimentsThroughBash.py 3 1000 False 

## Run with different goals
python runExperimentsThroughBash.py 3 1000000 True 'allMin' 1
python runExperimentsThroughBash.py 3 1000000 True 'allMax' 2

# # # policy 5
## Run once with 1000000 to 1000
python runExperimentsThroughBash.py 4 1000000 True 
python runExperimentsThroughBash.py 4 100000 True
python runExperimentsThroughBash.py 4 10000 True 
python runExperimentsThroughBash.py 4 1000 True 
python runExperimentsThroughBash.py 4 1000000 False
python runExperimentsThroughBash.py 4 100000 False
python runExperimentsThroughBash.py 4 10000 False 
python runExperimentsThroughBash.py 4 1000 False 

## Run with different goals
# python runExperimentsThroughBash.py 0 1000000 True 'allMin' 1
# python runExperimentsThroughBash.py 0 1000000 True 'allMax' 2