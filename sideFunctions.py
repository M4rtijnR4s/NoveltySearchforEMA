## important imports
import numpy as np 
import pandas as pd
import os
import matplotlib.pyplot as plt
from ema_workbench.analysis import parcoords
from ema_workbench.analysis import pairs_plotting
from ema_workbench.analysis import feature_scoring
import seaborn as sns

## create relative path 
dirname = os.path.dirname(os.path.abspath('__file__'))
resultFolder = os.path.join(dirname, 'Results')

## 
## 
'''
Combine results of multiple csv's (or dataframes) of individual items

@param fileList; List of files to be combined into single dataframe

Returns single dataframe
'''
def combineResults(fileList):
    nameList = ['Nothing', 'max_P', 'utility', 'inertia', 'reliability']
    for index, fileName in enumerate(fileList):
        if index == 0:
            newDf = pd.read_csv(fileName)
        else:
            newDf = pd.concat([newDf, pd.read_csv(fileName, header=None, names=[nameList[index]])], axis=1)
    return newDf



'''
Create and save a scatterplot containg all output variables

@param: df; df to base the results upon
@param: savename; Name to save figure as
@param: limits (optional); The limits of the the figures
@param: groupby (optional); how to group the results

Returns: axes; Returns the axes so limits can be determined. 
'''
def pairsPlotEMA(df, savename, limits=None, groupby=None):
    ## These are used to plot the outcomes as scatterplot (default)
    x = df[['b', 'q', 'mean', 'stdev', 'delta', 'type']]
    y = df[['max_P', 'utility', 'inertia', 'reliability']]

    ## Use these if you want to print the input as scatterplot 
    # y = df[['b', 'q', 'mean', 'stdev', 'delta']]
    # x = df[['max_P', 'utility', 'inertia', 'reliability', 'type']]

    ## This is always needed
    y = y.to_dict('list')

    ## These are used to plot the outcomes as scatterplot (default)
    y['max_P'] = np.asarray(y['max_P'])
    y['utility'] = np.asarray(y['utility'])
    y['inertia'] = np.asarray(y['inertia'])
    y['reliability'] = np.asarray(y['reliability'])

    ## Use these with the other above if you want to print the input as scatterplot
    # y['b'] = np.asarray(y['b'])
    # y['q'] = np.asarray(y['q'])
    # y['mean'] = np.asarray(y['mean'])
    # y['stdev'] = np.asarray(y['stdev'])
    # y['delta'] = np.asarray(y['delta'])

    # print(y)

    fig, axes = pairs_plotting.pairs_scatter(x, y, group_by=groupby,
                                         legend=True)
        
    if limits is not None:
        for ax in axes:
            axes[ax].set_xlim(limits[ax].get_xlim())
            axes[ax].set_ylim(limits[ax].get_ylim())

    fig.set_size_inches(8,8)
    
    plt.savefig('Results/Figures/'+str(savename)+'_scatterplot.png')
    plt.show()
    return axes

'''
Create and save a heatmap (feature scoring matrix)

@param df; the dataframe used to create the heatmap
@param savename; Name of the figure to be saved as
'''
def plotHeatmap(df, savename):
    x = df[['b', 'q', 'mean', 'stdev', 'delta']]
    y = df[['max_P', 'utility', 'inertia', 'reliability']]

    fs = feature_scoring.get_feature_scores_all(x, y)
    sns.heatmap(fs, cmap='viridis', annot=True, vmin=0, vmax=1)
    plt.savefig('Results/Figures/'+str(savename)+'_featureScoring.png' )
    plt.show()

'''
Minimzes a dataframe including all minimum and maximum values with some random samples

@param lhcDf; input dataframe to minimize
@param sample; the amount of extra random samples to be generated

Returns df; Dataframe that is minimal version of lhcDf
'''
def minimizeDF(lhcDf, sample=15):
    lhcmin = lhcDf.iloc[[lhcDf['max_P'].idxmin(), lhcDf['utility'].idxmin(), lhcDf['inertia'].idxmin(), lhcDf['reliability'].idxmin(), lhcDf['max_P'].idxmax(), lhcDf['utility'].idxmax(), lhcDf['inertia'].idxmax(), lhcDf['reliability'].idxmax()]]
    lhcDfMinimal = lhcDf.sample(sample)
    df = pd.concat([lhcDfMinimal, lhcmin])
    return df

'''
Create ad save a parallel plot. 

@param: df; Main dataframe for plot generation
@param: savename; name to save figure as
@param: output; Boolean to use output (true --> yes; False --> no)
@param: uncertainty; boolean to use uncertainty (True --> yes; False --> no )
@param: limits; The limits to be used for the graphs (default is None)
@param: col; what color should the main results get
@param: mini; extra dataframe to be given color red (not recommended)
@param: maxi;  extra dataframe to be given color green (not recommended)
'''
def parallelPlot(df, savename, output=True, uncertainty=False, limits=None, col=None, mini=None, maxi=None):
    # if output is true only output,
    if(output):
        outcomes = df[ ['max_P', 'utility', 'inertia', 'reliability']]
    # if not output and uncertainty only uncertainty
    elif(uncertainty):
        outcomes = df[['b', 'q', 'mean', 'stdev', 'delta']]
    # if not output and not uncertainty use all.
    else:
        outcomes = df

    # If no limits take default limits. 
    if limits is None:
        limits = parcoords.get_limits(outcomes)
    else:
        limits = limits[outcomes.columns]
    

    axes = parcoords.ParallelAxes(limits)
    axes.plot(outcomes, color=col)
    if maxi is not None: 
        axes.plot(maxi, color="green")
    if mini is not None: 
        axes.plot(mini, color="red")
    # axes.invert_axis('max_P')
    plt.savefig('Results/Figures/'+str(savename)+'_parallelPlot.png')
    plt.show()


'''
Get single dataframe of the results requested

@param: policy; what policy was it about (computer science way 0=1, 1=2 etc. )
@param: novelty; nboolean novelty results or latin hypercube results (true is novelty)
@param: nfe; The number of functional evaluations the experiment had
@param: prefix; Was there a prefix in the name
@param: optimization; Was it an optimization experiment (obsolete)

Returns single dataframe
'''
def getDf(policy, novelty, nfe=1000000, prefix='', optimization=False):
    if novelty:
        if not optimization:
            fl = os.path.join(resultFolder, 'NoveltySearch-'+str(prefix)+'Experiment_Policy'+str(policy)+'-nfe'+str(nfe)+'.csv')
            df =  pd.read_csv(fl)
        else:
            fl = os.path.join(resultFolder, 'Optmization_Policy'+str(policy)+'-nfe'+str(nfe)+'.csv')
            df =  pd.read_csv(fl)
    else:
        LHCFile1 = os.path.join(resultFolder, str(prefix)+'LHC-Experiment_Policy'+str(policy)+'-nfe'+str(nfe)+'/experiments.csv')
        LHCFile2 = os.path.join(resultFolder, str(prefix)+'LHC-Experiment_Policy'+str(policy)+'-nfe'+str(nfe)+'/max_P.csv')
        LHCFile3 = os.path.join(resultFolder, str(prefix)+'LHC-Experiment_Policy'+str(policy)+'-nfe'+str(nfe)+'/utility.csv')
        LHCFile4 = os.path.join(resultFolder, str(prefix)+'LHC-Experiment_Policy'+str(policy)+'-nfe'+str(nfe)+'/inertia.csv')
        LHCFile5 = os.path.join(resultFolder, str(prefix)+'LHC-Experiment_Policy'+str(policy)+'-nfe'+str(nfe)+'/reliability.csv')
        df = combineResults([LHCFile1, LHCFile2, LHCFile3, LHCFile4, LHCFile5])

    return df


'''
Generate and print scenarios (EMA way) to be used for further testing and reliability checks

@param df; Dataframe to get the scenarios from
''' 
def getScenarios(df):
    for index, row in df.iterrows():
        print("Scenario('scenarioReference"+str(index)+"', b="+str(row['b'])+", q="+str(row['q'])+", mean="+str(row['mean'])+", stdev="+str(row['stdev'])+", delta="+str(row['delta'])+"),")


