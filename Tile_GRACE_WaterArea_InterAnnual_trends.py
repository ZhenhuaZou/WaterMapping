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
fig.set_size_inches([9,4.5])
validPercentTile = 0.25 # this could be changed

#################### set up the background map ##############################
map = Basemap(llcrnrlon=-180,llcrnrlat=-62,urcrnrlon=180,urcrnrlat=86,resolution='c',epsg=4326)
map.drawparallels(np.arange(-30,90.1,30),linewidth=0.2,color='none',labels=[0,1,0,0],rotation=90,fontsize=7,fontname='Arial')
map.drawparallels(np.arange(-30,90.1,30),linewidth=0.2,color='none',labels=[1,0,0,0],rotation=-270,fontsize=7,fontname='Arial')
map.drawmeridians(np.arange(map.lonmin,map.lonmax+5,60),linewidth=0.2,color='none',labels=[0,0,1,1],fontsize=7,fontname='Arial')
# draw the grid lines within the map
map.drawmapboundary(linewidth=0.5)
map.fillcontinents(color='white')
map.drawcoastlines(linewidth=0.3,color='grey')
map.drawcountries(linewidth=0.3,color='grey')
############################################ add tick
### bottom
plt.plot([-120,-120],[85,86],linewidth=0.5,color='black')
plt.plot([-60,-60],[85,86],linewidth=0.5,color='black')
plt.plot([0,0],[85,86],linewidth=0.5,color='black')
plt.plot([60,60],[85,86],linewidth=0.5,color='black')
plt.plot([120,120],[85,86],linewidth=0.5,color='black')
### top
plt.plot([-120,-120],[-62,-61],linewidth=0.5,color='black')
plt.plot([-60,-60],[-62,-61],linewidth=0.5,color='black')
plt.plot([0,0],[-62,-61],linewidth=0.5,color='black')
plt.plot([60,60],[-62,-61],linewidth=0.5,color='black')
plt.plot([120,120],[-62,-61],linewidth=0.5,color='black')
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
    GRACEFN = '/home/zhzou/data/GlobalWater/DataRepository/Direct_Annual_5/Grace_LWS/interAnnualGraceLWS_Tile'+'_'+str(ID).zfill(4)+'_'+lon+'_'+lat+'_2002_2016.csv'
    WATERFN = '/home/zhzou/data/GlobalWater/DataRepository/Direct_Annual_5/Water_Area/interAnnualWaterArea_Tile'+'_'+str(ID).zfill(4)+'_'+lon+'_'+lat+'_'+str(validPercentTile)+'_1984_2017.csv'
    
    headers = ['time','allPixel','validPixel','ave']
    headers2 = ['time','outYesNoList','waterAreaSL','Ratios']
    dfGRACE = pd.read_csv(GRACEFN,names = headers)
    dfWATER = pd.read_csv(WATERFN,names = headers2)
    leftLon = int(lon) 
    lowLat = int(lat) 
    xGrace = np.arange(0,15)
    xxGrace = (xGrace/14.0)*4.5 + leftLon + 0.25  
    xWater = np.arange(0,15)
    xxWaterB = (xWater/14.0)*4.5 + leftLon + 0.25
    TimeGrace = dfGRACE['time'].values
    TimeWater = dfWATER['time'].values[18:33]
    #print 'TimeWater: ',TimeWater
    yWaterValidB = dfWATER['outYesNoList'].values[18:33]
    if ((np.max(TimeWater) != np.min(TimeWater)) and (np.sum(yWaterValidB)>0)):
        yGrace = dfGRACE['ave'].values
        yWaterB = dfWATER['waterAreaSL'].values[18:33]
        
        yWaterB[np.where(yWaterValidB == 0)] = np.nan
      
        yGraceCatMean = np.nanmean(yGrace)
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
        #print yPrateB,yPrate,xxWater

        distYGraceRange = np.nanmax(yGrace)-np.nanmin(yGrace)
        distYGrace = (np.nanmax(yGrace)-np.nanmin(yGrace))/abs(yGraceCatMean)
        
        if distYGraceRange <= 5:
            distYGraceCat = 0.25
        elif distYGraceRange <= 10:
            distYGraceCat = 0.4
        elif distYGraceRange <= 20:
            distYGraceCat = 0.55
        elif distYGraceRange <= 30:
            distYGraceCat = 0.7
        elif distYGraceRange <= 40:
            distYGraceCat = 0.85
        else:
            distYGraceCat = 1

        distYWaterRange = np.nanmax(yWater)-np.nanmin(yWater)
        distYWater = (np.nanmax(yWater)-np.nanmin(yWater))/abs(yWaterCatMean)

       
        if distYWater <= 0.1:
            distYWaterCat = 0.25
        elif distYWater <= 0.25:
            distYWaterCat = 0.4
        elif distYWater <= 0.5:
            distYWaterCat = 0.55
        elif distYWater <= 1:
            distYWaterCat = 0.7
        elif distYWater <= 2:
            distYWaterCat = 0.85
        else:
            distYWaterCat = 1
  
        # for those that have the same values, only one or more
        if distYWaterRange ==0: # all nonNan values are the same , or there is only one value 
            if np.nanmin(yWater) ==0: # this case all the values were 0, or there is only one value that is 0
                yyWater = yWater *1.6*0 + lowLat + 2.7 
            else: # this case all nonNan values are the same and are not 0, or there is only one value that is not 0
                yyWater = (yWater/yWater)*1.6*0.5 + lowLat + 2.7 # this case all the values were the same but not 0, set it as a line in the height of middle
        else:
            yyWater = ((yWater - np.nanmin(yWater))/distYWaterRange)*1.6*distYWaterCat + lowLat + 2.7
        
        yyGrace = ((yGrace - np.nanmin(yGrace))/distYGraceRange)*1.6*distYGraceCat + lowLat + 0.7
        yGraceAreaCat = 0.45
        
        WaterValidID = np.isfinite(yWater)
        WaterValidNum = np.sum(np.isfinite(yWater))
        if WaterValidNum < 10: # pay attention to this valid threshold
            waterColorName = 0
        else:
            yyyWater = yWater[WaterValidID]
            xxxTime = TimeWater[WaterValidID]

            if (np.nanmin(yyyWater)==np.nanmax(yyyWater)):
                waterColorName = 0
            else:
                # linear regression
                xxxTime = sm.add_constant(xxxTime)
                results = sm.OLS(yyyWater,xxxTime).fit()
                pvalue = results.pvalues[1] # pay attention to this
                interceptValue = results.params[0]
                beta = results.params[1]
                #print pvalue,' ',beta
                if pvalue < 0.05:
                    if beta < 0:
                        waterColorName = -1 # significant decreasing
                    elif beta >0:
                        waterColorName = 1 # significant increasing
                    else:
                        waterColorName = 0 # not significant
                else:
                    waterColorName = 0 # no significant relationship
                # check whether pvalue or beta is nan
                if np.isnan(pvalue):
                    print 'pvalue is nan of ID: ',ID
                    pvalue = 1
                if np.isnan(beta):
                    print 'beta is nan of ID: ',ID
                    beta=0

        ############### Grace
        GraceValidID = np.isfinite(yGrace)
        GraceValidNum = np.sum(np.isfinite(yGrace))
        if GraceValidNum < 10: # pay attention to this valid threshold
            graceColorName = 0
        else:
            yyyGrace = yGrace[GraceValidID]
            xxxGrace = TimeGrace[GraceValidID]
            if (np.nanmin(yyyGrace)==np.nanmax(yyyGrace)):
                graceColorName = 0
            else:
                # linear regression
                xxxGrace = sm.add_constant(xxxGrace)
                results = sm.OLS(yyyGrace,xxxGrace).fit()
                pvalue = results.pvalues[1] # pay attention to this
                interceptValue = results.params[0]
                beta = results.params[1]
                #print pvalue,' ',beta
                if pvalue < 0.05:
                    if beta < 0:
                        graceColorName = -1 # significant decreasing
                    elif beta >0:
                        graceColorName = 1 # significant increasing
                    else:
                        graceColorName = 0 # not significant
                else:
                    graceColorName = 0 # no significant relationship
                # check whether pvalue or beta is nan
                if np.isnan(pvalue):
                    print 'pvalue is nan of ID: ',ID
                    pvalue = 1
                if np.isnan(beta):
                    print 'beta is nan of ID: ',ID
                    beta=0
        
        ####### final colors
        if graceColorName ==1:
            if waterColorName ==1:
                finalColor = 'blue'
            elif waterColorName ==0:
                finalColor = 'royalblue'
            else:
                finalColor = 'dodgerblue'

        elif graceColorName ==0:
            if waterColorName ==1:
                finalColor = 'dimgray'
            elif waterColorName ==0:
                finalColor = 'darkgray'
            else:
                finalColor = 'gainsboro'
        else:
            if waterColorName ==1:
                finalColor = 'darkorange'
            elif waterColorName ==0:
                finalColor = 'lightcoral'
            else:
                finalColor = 'red'


        # add patches
        def draw_screen_poly2(lats,lons,m,finalColor):
            x,y=m(lons,lats)
            xy = zip(x,y)
            poly = Polygon(xy,facecolor=finalColor,edgecolor=finalColor,linewidth=0.1)
            plt.gca().add_patch(poly)

        lats1 = [lowLat+0.2,lowLat+5-0.2,lowLat+5-0.2,lowLat+0.2]
        lons1 = [leftLon+0.2,leftLon+0.2,leftLon+5-0.2,leftLon+5-0.2]
        draw_screen_poly2(lats1,lons1,map,finalColor)
        
        plt.plot(xxGrace,yyGrace,linewidth=yGraceAreaCat,color='black')
        plt.plot(xxWater,yyWater,linewidth=yWaterAreaCat,marker='o',markersize = yWaterAreaCat-0.08,markeredgewidth=0.04,color='black') # plot doesn't show [nan, 5, nan]

# get the tile selection
TileSelFN = '/data/ifs/users/zhzou/GlobalWater/StaAnnualSub001Deg_MaxSeasonAs3/WaterAreaAnnual_NoDistantToQual/intraAnnualAddArea_FlexibleSelection/Tile_Selection_Grace.csv'
dfTileSel = pd.read_csv(TileSelFN,names = ['TileSel'])
IDs = dfTileSel['TileSel'].values
IDNum = len(IDs)
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

plt.text(-178, 17, 'Background colors', fontsize=7,fontname='Arial')
# add patches
def draw_screen_poly3(lats,lons,m,finalColor):
    x,y=m(lons,lats)
    xy = zip(x,y)
    poly = Polygon(xy,facecolor=finalColor,edgecolor='k',linewidth=0.25)
    plt.gca().add_patch(poly)

lats11 = [11,15,15,11]
lons11 = [-178,-178,-174,-174]
draw_screen_poly3(lats11,lons11,map,'blue')
plt.text(-172,11,'LWS increase & Water increase',fontsize=7,fontname='Arial')

lats10 = [6,10,10,6]
lons10 = [-178,-178,-174,-174]
draw_screen_poly3(lats10,lons10,map,'royalblue')
plt.text(-172,6,'LWS increase & Water no trend',fontsize=7,fontname='Arial')

lats101 = [1,5,5,1]
lons101 = [-178,-178,-174,-174]
draw_screen_poly3(lats101,lons101,map,'dodgerblue')
plt.text(-172,1,'LWS increase & Water decrease',fontsize=7,fontname='Arial')

lats01 = [-4,0,0,-4]
lons01 = [-178,-178,-174,-174]
draw_screen_poly3(lats01,lons01,map,'dimgray')
plt.text(-172,-4,'LWS no trend & Water increase',fontsize=7,fontname='Arial')

lats00 = [-9,-5,-5,-9]
lons00 = [-178,-178,-174,-174]
draw_screen_poly3(lats00,lons00,map,'darkgray')
plt.text(-172,-9,'LWS no trend & Water no trend',fontsize=7,fontname='Arial')

lats001 = [-14,-10,-10,-14]
lons001 = [-178,-178,-174,-174]
draw_screen_poly3(lats001,lons001,map,'gainsboro')
plt.text(-172,-14,'LWS no trend & Water decrease',fontsize=7,fontname='Arial')

lats011 = [-19,-15,-15,-19]
lons011 = [-178,-178,-174,-174]
draw_screen_poly3(lats011,lons011,map,'darkorange')
plt.text(-172,-19,'LWS decrease & Water increase',fontsize=7,fontname='Arial')

lats010 = [-24,-20,-20,-24]
lons010 = [-178,-178,-174,-174]
draw_screen_poly3(lats010,lons010,map,'lightcoral')
plt.text(-172,-24,'LWS decrease & Water no trend',fontsize=7,fontname='Arial')

lats0101 = [-29,-25,-25,-29]
lons0101 = [-178,-178,-174,-174]
draw_screen_poly3(lats0101,lons0101,map,'red')
plt.text(-172,-29,'LWS decrease & Water decrease',fontsize=7,fontname='Arial')

## Grace height
xL = np.arange(0,6.3,0.1)
yL = np.sin(xL)
xxL = (xL/6.3)*5
yyL = ((yL+1)/2)*2
plt.text(-178,-36,'GRACE LWS (lower curve of tile)',fontsize=7,fontname='Arial')
plt.text(-178,-41,'(Line amplitudes, range) ',fontsize=7,fontname='Arial')
xxLH = xxL + (-178)
xxLH2 = xxL + (-178)+30

yyLH05 = yyL * 0.25 + (-47) + 1
yyLH06 = yyL * 0.4 + (-53) + 1
yyLH07 = yyL * 0.55 + (-59) + 1
yyLH08 = yyL * 0.7 + (-47) + 1
yyLH09 = yyL * 0.85 + (-53) + 1
yyLH10 = yyL * 1.0 + (-59) + 1

plt.plot(xxLH,yyLH05,linewidth=0.45,linestyle='-',color='black')
plt.plot(xxLH,yyLH06,linewidth=0.45,linestyle='-',color='black')
plt.plot(xxLH,yyLH07,linewidth=0.45,linestyle='-',color='black')
plt.plot(xxLH2,yyLH08,linewidth=0.45,linestyle='-',color='black')
plt.plot(xxLH2,yyLH09,linewidth=0.45,linestyle='-',color='black')
plt.plot(xxLH2,yyLH10,linewidth=0.45,linestyle='-',color='black')


plt.text(-172,-47,'(0,5]',fontsize=7,fontname='Arial')
plt.text(-172,-53,'(5,10]',fontsize=7,fontname='Arial')
plt.text(-172,-59,'(10,20]',fontsize=7,fontname='Arial')
plt.text(-142,-47,'(20,30]',fontsize=7,fontname='Arial')
plt.text(-142,-53,'(30,40]',fontsize=7,fontname='Arial')
plt.text(-142,-59,'>40 cm',fontsize=7,fontname='Arial')

# Water height
plt.text(-47,-36,'Water (upper curve of tile)',fontsize=7,fontname='Arial')
plt.text(-47,-41,'(Line amplitudes, range/mean)',fontsize=7,fontname='Arial')
xxLH = xxL + (-47)
xxLH2 = xxL + (-47) +35
yyLH05 = yyL * 0.25 + (-47) + 1
yyLH06 = yyL * 0.4 + (-53) + 1
yyLH07 = yyL * 0.55 + (-59) + 1
yyLH08 = yyL * 0.7 + (-47) + 1
yyLH09 = yyL * 0.85 + (-53) + 1
yyLH10 = yyL * 1.0 + (-59) + 1

plt.plot(xxLH,yyLH05,linewidth=0.45,linestyle='-',color='black')
plt.plot(xxLH,yyLH06,linewidth=0.45,linestyle='-',color='black')
plt.plot(xxLH,yyLH07,linewidth=0.45,linestyle='-',color='black')
plt.plot(xxLH2,yyLH08,linewidth=0.45,linestyle='-',color='black')
plt.plot(xxLH2,yyLH09,linewidth=0.45,linestyle='-',color='black')
plt.plot(xxLH2,yyLH10,linewidth=0.45,linestyle='-',color='black')

plt.text(-41,-47,'(0,0.1]',fontsize=7,fontname='Arial')
plt.text(-41,-53,'(0.1,0.25]',fontsize=7,fontname='Arial')
plt.text(-41,-59,'(0.25,0.5]',fontsize=7,fontname='Arial')
plt.text(-6,-47,'(0.5,1]',fontsize=7,fontname='Arial')
plt.text(-6,-53,'(1,2]',fontsize=7,fontname='Arial')
plt.text(-6,-59,'>2',fontsize=7,fontname='Arial')

# Water coverage
plt.text(45,-36,'Water (upper curve of tile)',fontsize=7,fontname='Arial')
plt.text(45,-41,'(Line widths, water coverage)',fontsize=7,fontname='Arial')
xxLT = xxL + (45)
xxLT2 = xxL + (45) +34
yyLT05 = yyL * 0.68  + (-47) + 1
yyLT06 = yyL * 0.68  + (-53) + 1
yyLT07 = yyL * 0.68  + (-59) + 1
yyLT08 = yyL * 0.68  + (-47) + 1
yyLT09 = yyL * 0.68  + (-53) + 1
yyLT10 = yyL * 0.68  + (-59) + 1

plt.plot(xxLT,yyLT05,linewidth=0.25,linestyle='-',color='black')
plt.plot(xxLT,yyLT06,linewidth=0.35,linestyle='-',color='black')
plt.plot(xxLT,yyLT07,linewidth=0.45,linestyle='-',color='black')
plt.plot(xxLT2,yyLT08,linewidth=0.55,linestyle='-',color='black')
plt.plot(xxLT2,yyLT09,linewidth=0.65,linestyle='-',color='black')
plt.plot(xxLT2,yyLT10,linewidth=0.75,linestyle='-',color='black')

plt.text(51,-47,'(0%,1%]',fontsize=7,fontname='Arial')
plt.text(51,-53,'(1%,2.5%]',fontsize=7,fontname='Arial')
plt.text(51,-59,'(2.5%,5%]',fontsize=7,fontname='Arial')
plt.text(85,-47,'(5%,10%]',fontsize=7,fontname='Arial')
plt.text(85,-53,'(10%,20%]',fontsize=7,fontname='Arial')
plt.text(85,-59,'>20%',fontsize=7,fontname='Arial')
filenameout = '/data/ifs/users/zhzou/Figures/Tile_GraceLWS_WaterArea_InterAnnual_Variation_and_Trends.pdf'
plt.savefig(filenameout,dpi=800,bbox_inches='tight')
#plt.show()