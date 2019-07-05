#!/usr/bin/env python2
# import modules
import glob
import statsmodels.api as sm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib



#################### add plot to the map ##################################
def addplot(ID):
    
    WATERFN = '/home/zhzou/data/GlobalWater/DataRepository/NG_Submission/Annual_Hydrological_Basin/Water_Area/interAnnualAddArea_Tile_MatchID_'+str(ID)+'_1984_2017_Direct_only025.csv'
    headers2 = ['time','outYesNoList','waterAreaSL','Ratios']
    dfWATER = pd.read_csv(WATERFN,names = headers2)
    TimeWater = dfWATER['time'].values
    #print 'TimeWater: ',TimeWater
    yWaterValidB = dfWATER['outYesNoList'].values
    if ((np.max(TimeWater) != np.min(TimeWater)) and (np.sum(yWaterValidB)>0)):
        yWaterB = dfWATER['waterAreaSL'].values
       
        yWaterB[np.where(yWaterValidB == 0)] = np.nan
      
        # get the mean values of prate, grace, and water
        yWaterCatMean = np.nanmean(yWaterB)
        
        # add the first one to the last
        yWater = yWaterB * 1.0
      
        distYWaterRange = np.nanmax(yWater)-np.nanmin(yWater)
        distYWater = (np.nanmax(yWater)-np.nanmin(yWater))/abs(yWaterCatMean)

        
        WaterValidID = np.isfinite(yWater)
        WaterValidNum = np.sum(np.isfinite(yWater))
        if WaterValidNum < 10: # pay attention to this valid threshold
            outTrend = -10
        else:
            yyyWater = yWater[WaterValidID]
            xxxTime = TimeWater[WaterValidID]
            # linear regression
            xxxTime = sm.add_constant(xxxTime)
            results = sm.OLS(yyyWater,xxxTime).fit()
            pvalue = results.pvalues[1] # pay attention to this
            interceptValue = results.params[0]
            beta = results.params[1]
            #print pvalue,' ',beta
            if pvalue < 0.05:
                if beta < 0:
                    outTrend = -1
                elif beta >0:
                    outTrend = 1
                else:
                    outTrend = 0
            else:
                outTrend = 0
            # check whether pvalue or beta is nan
            if np.isnan(pvalue):
                print 'pvalue is nan of ID: ',ID
                pvalue = 1
                outTrend = 10
            if np.isnan(beta):
                print 'beta is nan of ID: ',ID
                beta=0
                outTrend = 20
    else:
        if np.max(TimeWater) == 0:
            outTrend = -40 #  no yearlong water pixels in the entire tile across all years
        elif np.max(TimeWater) == 1:
            outTrend = -30 # this means no layers have the valid pixels meet the >25% of the maximum wter area requirement
        elif np.max(TimeWater) == 2:
            outTrend = -20 # # this means no valid water pixels meet the requirement for all layers (>0.05*numEle) 
    return outTrend



TileSelFN = '/data/ifs/users/zhzou/GlobalWater/StaAnnualSub001Deg_005P_05Y_MaxSeasonAs3_SumFreq8Days_AnnualFreqFromMonth2019_HB05/HBSelection/HB_Selection.csv'
dfTileSel = pd.read_csv(TileSelFN,names = ['TileSel'])
IDs = dfTileSel['TileSel'].values
IDNum = len(IDs)
results = []
if __name__=='__main__':
    for IDi in range(0,IDNum): # the original is (1,IDNum)
        ID = IDs[IDi]
        resultsi = addplot(ID)
        results.append(resultsi)
resultjj = np.asarray(results)
resultii = int(np.reshape(len(results),1))
np.savetxt('/home/zhzou/data/GlobalWater/DataRepository/NG_Submission/Annual_Hydrological_Basin/Tile_trends_MaxAnnualArea_HB05.csv',resultjj,delimiter=',')
