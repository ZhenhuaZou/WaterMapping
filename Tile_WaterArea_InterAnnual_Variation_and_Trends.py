#!/usr/bin/env python2
# import modules
import glob
import statsmodels.api as sm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from datetime import datetime
import matplotlib
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
# set the parameters of paper size
fig = plt.figure(1)
#fig,ax=plt.subplots()
fig.set_size_inches([8.98,4.49])

#################################################################################################################################
validPercentTile = 0.25 # this could be changed

#################### set up the background map ##############################
map = Basemap(llcrnrlon=-180,llcrnrlat=-61,urcrnrlon=180,urcrnrlat=86,resolution='c',epsg=4326)
map.drawparallels(np.arange(-30,90.1,30),linewidth=0.2,color='none',labels=[0,1,0,0],rotation=90,fontsize=7,fontname='Arial')
map.drawparallels(np.arange(-30,90.1,30),linewidth=0.2,color='none',labels=[1,0,0,0],rotation=-270,fontsize=7,fontname='Arial')
map.drawmeridians(np.arange(map.lonmin,map.lonmax+5,60),linewidth=0.2,color='none',labels=[0,0,1,1],fontsize=7,fontname='Arial')

# draw the grid lines within the map
map.drawmeridians(np.arange(-180,180,5),linewidth=0.2,color='white')
map.drawparallels(np.arange(-55,85,5),linewidth=0.2,color='white')
map.drawmapboundary(linewidth=0.5)
map.fillcontinents(color='gainsboro')
map.drawcoastlines(linewidth=0.2,color='grey')
map.drawcountries(linewidth=0.2,color='grey')
############################################ add tick
plt.plot([-120,-120],[85,86],linewidth=0.5,color='black')
plt.plot([-60,-60],[85,86],linewidth=0.5,color='black')
plt.plot([0,0],[85,86],linewidth=0.5,color='black')
plt.plot([60,60],[85,86],linewidth=0.5,color='black')
plt.plot([120,120],[85,86],linewidth=0.5,color='black')
### bottom
plt.plot([-120,-120],[-61,-60],linewidth=0.5,color='black')
plt.plot([-60,-60],[-61,-60],linewidth=0.5,color='black')
plt.plot([0,0],[-61,-60],linewidth=0.5,color='black')
plt.plot([60,60],[-61,-60],linewidth=0.5,color='black')
plt.plot([120,120],[-61,-60],linewidth=0.5,color='black')
### left
plt.plot([-180,-179],[60,60],linewidth=0.5,color='black')
plt.plot([-180,-179],[30,30],linewidth=0.5,color='black')
plt.plot([-180,-179],[0,0],linewidth=0.5,color='black')
plt.plot([-180,-179],[-30,-30],linewidth=0.5,color='black')
### right
plt.plot([179,180],[60,60],linewidth=0.5,color='black')
plt.plot([179,180],[30,30],linewidth=0.5,color='black')
plt.plot([179,180],[0,0],linewidth=0.5,color='black')
plt.plot([179,180],[-30,-30],linewidth=0.5,color='black')

# add patches
def draw_screen_poly(lats,lons,m):
    x,y=m(lons,lats)
    xy = zip(x,y)
    poly = Polygon(xy,facecolor='gainsboro',edgecolor='gainsboro')
    plt.gca().add_patch(poly)

lats1 = [40,50.5,50.5,40]
lons1 = [-92.5,-92.5,-75,-75]
draw_screen_poly(lats1,lons1,map)
lats2 = [49.7,55.5,55.5,49.7]
lons2 = [-102.6,-102.6,-94,-94]
draw_screen_poly(lats2,lons2,map)
lats3=[-16.5,3.5,3.5,-16.5]
lons3=[26.7,26.7,36.5,36.5]
draw_screen_poly(lats3,lons3,map)
lats4=[40.5,48,48,40.5]
lons4=[56.5,56.5,63,63]
draw_screen_poly(lats4,lons4,map)
lats5=[50,57,57,50]
lons5=[103,103,111,111]
draw_screen_poly(lats5,lons5,map)
lats6=[59,67,67,59]
lons6=[-125.8,-125.8,-109.8,-109.8]
draw_screen_poly(lats6,lons6,map)

#################### add plot to the map ##################################
def addplot(ID,lon,lat,validPercentTile):
    WATERFN = '/home/zhzou/data/GlobalWater/DataRepository/Direct_Annual_5/Water_Area/interAnnualWaterArea_Tile'+'_'+str(ID).zfill(4)+'_'+lon+'_'+lat+'_'+str(validPercentTile)+'_1984_2017.csv'
    headers = ['time','outYesNoList','waterAreaSL','Ratios']
    dfWATER = pd.read_csv(WATERFN,names = headers)
    leftLon = int(lon) 
    lowLat = int(lat) 
    xWater = np.arange(0,34)
    xxWaterB = (xWater/33.0)*4.5 + leftLon + 0.25
    TimeWater = dfWATER['time'].values
    #print 'TimeWater: ',TimeWater
    yWaterValidB = dfWATER['outYesNoList'].values
    if ((np.max(TimeWater) != np.min(TimeWater)) and (np.sum(yWaterValidB)>0)):
        yWaterB = dfWATER['waterAreaSL'].values
        yWaterB[np.where(yWaterValidB == 0)] = np.nan
        yWaterCatMean = np.nanmean(yWaterB)
        # get the water body area per unit land category
        waterAreaPerUnitLandi = dfWATER['Ratios'].values[0]
        if waterAreaPerUnitLandi <= 0.01:
            yWaterAreaCat = 0.25
        elif  waterAreaPerUnitLandi<= 0.025:
            yWaterAreaCat = 0.35
        elif  waterAreaPerUnitLandi <= 0.05:
            yWaterAreaCat = 0.45
        elif  waterAreaPerUnitLandi <= 0.1:
            yWaterAreaCat = 0.55
        elif  waterAreaPerUnitLandi<= 0.2:
            yWaterAreaCat = 0.65
        else:
            yWaterAreaCat = 0.75
        # add the first one to the last
        yWater = yWaterB * 1.0
        xxWater = xxWaterB * 1.0
    
        # ###################################get the range category
        distYWaterRange = np.nanmax(yWater)-np.nanmin(yWater)
        distYWater = (np.nanmax(yWater)-np.nanmin(yWater))/abs(yWaterCatMean)
        if distYWater <= 0.1:
            distYWaterCat = 0.35
        elif distYWater <= 0.25:
            distYWaterCat = 0.48
        elif distYWater <= 0.5:
            distYWaterCat = 0.61
        elif distYWater <= 1:
            distYWaterCat = 0.74
        elif distYWater <= 2:
            distYWaterCat = 0.87
        else:
            distYWaterCat = 1

        # for those that have the same values, only one or more
        if distYWaterRange ==0: # all nonNan values are the same , or there is only one value 
            if np.nanmin(yWater) ==0: # this case all the values were 0, or there is only one value that is 0
                yyWater = yWater *2*0 + lowLat + 1.5 
            else: # this case all nonNan values are the same and are not 0, or there is only one value that is not 0
                yyWater = (yWater/yWater)*2*0.5 + lowLat + 1.5 # this case all the values were the same but not 0, set it as a line in the height of middle
        else:
            yyWater = ((yWater - np.nanmin(yWater))/distYWaterRange)*2*distYWaterCat + lowLat + 1.5
        #print distYWater, distYWaterCat
        # trends
        WaterValidID = np.isfinite(yWater)
        WaterValidNum = np.sum(np.isfinite(yWater))
        if WaterValidNum < 10: # pay attention to this valid threshold
            waterColorName = 'black'
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
                    waterColorName = 'magenta' # significant decreasing
                    
                elif beta >0:
                    waterColorName = 'blue' # significant increasing    
                else:
                    waterColorName = 'darkgreen' # not significant                
            else:
                waterColorName = 'darkgreen' # no significant relationship
               
            # check whether pvalue or beta is nan
            if np.isnan(pvalue):
                print 'pvalue is nan of ID: ',ID
                pvalue = 1
               
            if np.isnan(beta):
                print 'beta is nan of ID: ',ID
                beta=0   
        plt.plot(xxWater,yyWater,linewidth=yWaterAreaCat,marker='o',markersize = yWaterAreaCat-0.08,markeredgewidth=0.04,color=waterColorName) # plot doesn't show [nan, 5, nan]
    
# get the tile selection
TileSelFN = '/data/ifs/users/zhzou/GlobalWater/StaAnnualSub001Deg_MaxSeasonAs3/WaterAreaAnnual_NoDistantToQual/intraAnnualAddArea_FlexibleSelection/Tile_Selection.csv'
dfTileSel = pd.read_csv(TileSelFN,names = ['TileSel'])
IDs = dfTileSel['TileSel'].values
IDNum = len(IDs)
results = []
if __name__=='__main__':
    for IDi in range(0,IDNum): # the original is (1,IDNum)
        ID = IDs[IDi]
        filenameMaskB = '/data/ifs/users/zhzou/GlobalWater/Climate/Mask001DegBound/mask_WorldBound_tmpGrid_001Deg_'+str(ID).zfill(4)+'_*.tif' 
        filenameMasks = glob.glob(filenameMaskB)
        filenameMask = filenameMasks[0]
        stringMask = filenameMask.split('_')
        lon = stringMask[5]
        lat = stringMask[6].split('.')[0]
        resultsi = addplot(ID,lon,lat,validPercentTile)
        results.append(resultsi)
resultjj = np.asarray(results)
#resultii = np.reshape(len(results),1)
#np.savetxt('/home/zhzou/data/GlobalWater/SumFreqFrom8DaysInt_GE5/statistics/Tile_trends_MaxAnnualArea.csv',resultjj,delimiter=',')

#legend
plt.text(-178,9,'Colors',fontsize=7,fontname='Arial')
xL = np.arange(0,6.3,0.1)
yL = np.sin(xL)
xxL = (xL/6.3)*5
yyL = ((yL+1)/2)*2
xxLP = xxL + (-178)
yyLP = yyL * 0.68 + (3.5) +1
plt.plot(xxLP,yyLP,linewidth=0.45,linestyle='-',color='magenta')
xxLW = xxL + (-178)
yyLW = yyL * 0.68 + (-2) +1
plt.plot(xxLW,yyLW,linewidth=0.45,linestyle='-',color='blue')
xxLG = xxL + (-178)
yyLG = yyL * 0.68 + (-7.5) +1
plt.plot(xxLG,yyLG,linewidth=0.45,linestyle='-',color='darkgreen')
xxLN = xxL + (-178)
yyLN = yyL * 0.68 + (-13) +1
plt.plot(xxLN,yyLN,linewidth=0.45,linestyle='-',color='black')

plt.text(-172,3.5,'Slope < 0 and P < 0.05',fontsize=7,fontname='Arial')
plt.text(-172,-2,'Slope > 0 and P < 0.05',fontsize=7,fontname='Arial')
plt.text(-172,-7.5,'Slope = 0 or P   0.05 ',fontsize=7,fontname='Arial')
plt.text(-172,-13,'Valid observations < 10 years',fontsize=7,fontname='Arial')
## height
plt.text(-178,-20,'Amplitudes',fontsize=7,fontname='Arial')
plt.text(-178,-25.5,'(Range/mean)',fontsize=7,fontname='Arial')
xxLH = xxL + (-178)

yyLH05 = yyL * 0.35 + (-31) + 1
yyLH06 = yyL * 0.48 + (-36.5) + 1
yyLH07 = yyL * 0.61 + (-42) + 1
yyLH08 = yyL * 0.74 + (-47.5) + 1
yyLH09 = yyL * 0.87 + (-53) + 1
yyLH10 = yyL * 1.0 + (-58.5) + 1

plt.plot(xxLH,yyLH05,linewidth=0.45,linestyle='-',color='black')
plt.plot(xxLH,yyLH06,linewidth=0.45,linestyle='-',color='black')
plt.plot(xxLH,yyLH07,linewidth=0.45,linestyle='-',color='black')
plt.plot(xxLH,yyLH08,linewidth=0.45,linestyle='-',color='black')
plt.plot(xxLH,yyLH09,linewidth=0.45,linestyle='-',color='black')
plt.plot(xxLH,yyLH10,linewidth=0.45,linestyle='-',color='black')


plt.text(-172,-31,'(0,0.1]',fontsize=7,fontname='Arial')
plt.text(-172,-36.5,'(0.1,0.25]',fontsize=7,fontname='Arial')
plt.text(-172,-42,'(0.25,0.5]',fontsize=7,fontname='Arial')
plt.text(-172,-47.5,'(0.5,1]',fontsize=7,fontname='Arial')
plt.text(-172,-53,'(1,2]',fontsize=7,fontname='Arial')
plt.text(-172,-58.5,'>2',fontsize=7,fontname='Arial')

# Thickness
## height
plt.text(-134,-20,'Linewidths',fontsize=7,fontname='Arial')
plt.text(-134,-25.5,'(Water coverage)',fontsize=7,fontname='Arial')
xxLT = xxL + (-134)
yyLT05 = yyL * 0.68  + (-31) + 1
yyLT06 = yyL * 0.68  + (-36.5) + 1
yyLT07 = yyL * 0.68  + (-42) + 1
yyLT08 = yyL * 0.68  + (-47.5) + 1
yyLT09 = yyL * 0.68  + (-53) + 1
yyLT10 = yyL * 0.68  + (-58.5) + 1

plt.plot(xxLT,yyLT05,linewidth=0.25,linestyle='-',color='black')
plt.plot(xxLT,yyLT06,linewidth=0.35,linestyle='-',color='black')
plt.plot(xxLT,yyLT07,linewidth=0.45,linestyle='-',color='black')
plt.plot(xxLT,yyLT08,linewidth=0.55,linestyle='-',color='black')
plt.plot(xxLT,yyLT09,linewidth=0.65,linestyle='-',color='black')
plt.plot(xxLT,yyLT10,linewidth=0.75,linestyle='-',color='black')

plt.text(-128,-31,'(0%,1%]',fontsize=7,fontname='Arial')
plt.text(-128,-36.5,'(1%,2.5%]',fontsize=7,fontname='Arial')
plt.text(-128,-42,'(2.5%,5%]',fontsize=7,fontname='Arial')
plt.text(-128,-47.5,'(5%,10%]',fontsize=7,fontname='Arial')
plt.text(-128,-53,'(10%,20%]',fontsize=7,fontname='Arial')
plt.text(-128,-58.5,'>20%',fontsize=7,fontname='Arial')


filenameout = '/data/ifs/users/zhzou/Figures/Direct_Annual/Tile_WaterArea_InterAnnual_Variation_and_Trends_'+str(validPercentTile)+'.pdf'
plt.savefig(filenameout,dpi=800,bbox_inches='tight')
#plt.show()
