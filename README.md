# NoveltySearchforEMA
Novelty search for exploratory modelling

All novelty search related functions (that make novelty search work) can be found in Exploration.py. 

## Initialization and execution

Before being able to run the experiments make sure that you have a virtual environment, to keep your own computer as clean as possible. To create the virtual environment 'venv' on linux do the following, while making sure you are in the right directory and assuming the virtual environment dependency is installed:

```
virtualenv venv 
```
Once you have the virtual environment you can activate this python environment with the simple command: 

```
source venv/bin/activate
```

or 

```
source /home/user/path/to/project/venv/bin/activate
```

After setting up the virtual environment for the first time you must activate and initialize it by downloading and installing all dependencies. For running cython make sure to also look at how to install C as that is a requirement for cython. Installing all dependencies can done as follows.

```
pip install -r requirementsFinal.txt
```
Once everything is setup and initialized the experiments can be started. To completely replicate all results, first you would have to run test.py in OptimizedLevers to generate the solutions to the lake problem. After this you can run the indiviual tabs in optimization.ipynb to gather the policies that will be used in the experiments. 

Running the experiments is done using a Linux bash file, bashScriptCallExperiment.sh. This will run all experiments as explained in the experimental setup of my report. The experiments will run using a cythonized version of the dps lake model. This cythonized version is close to 100 times faster than the normal dps lake model. 
Make sure this bash script is executable. This can be done by running the following command: 

``` 
chmod +x bashScriptCallExperiment.sh 

```

Once this is done create a folder `Results` and `Results/Figures` in the main project folder and you can simply write `./bashScriptCallExperiment.sh` in your terminal and this will run all relevant experiments. 

The analysis of the experiments is done in policy<x>Experiments.ipynb where <x> stands for the policy that is being analyzed raning from 1 to 5. All analysis is identical, except for minor details due to the experiments, so the only analysis with explanations is policy1Experiments.ipynb so far. The analysis creates multiple plots, compares dataframe for similarities and generates scenarios that can be used to verify the existence of the solutions using unexpectedEntryTest.py. These still have to be manually copied in place to actually work. 

