# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 18:28:21 2020

@author: Raman Agarwal
"""


import random, pylab, numpy
import pandas as pd
from matplotlib import pyplot as plt
import datetime
#set line width
pylab.rcParams['lines.linewidth'] = 4
#set font size for titles 
pylab.rcParams['axes.titlesize'] = 20
#set font size for labels on axes
pylab.rcParams['axes.labelsize'] = 20
#set size of numbers on x-axis
pylab.rcParams['xtick.labelsize'] = 16
#set size of numbers on y-axis
pylab.rcParams['ytick.labelsize'] = 16
#set size of ticks on x-axis
pylab.rcParams['xtick.major.size'] = 7
#set size of ticks on y-axis
pylab.rcParams['ytick.major.size'] = 7
#set size of markers
pylab.rcParams['lines.markersize'] = 10
#set number of examples shown in legends
pylab.rcParams['legend.numpoints'] = 1



random.seed(0)

def getDataPd(filepath1, header1 = [0]):
    df = pd.read_csv(filepath1, header = header1 )
    return df

def rSquared(observed, predicted):
    error = ((predicted - observed)**2).sum()
    # print(error)
    meanError = error/len(observed)
    # print(meanError,numpy.var(observed))
    return (1 - (meanError/numpy.var(observed)))


class envVariable(object):
    def __init__(self, lat1, long1, year1, data1):
        self.latitude = float(lat1)
        self.longitude = float(long1)
        self.year = int(year1)
        self.data = float(data1)
        
    def getloc(self):
        return (self.latitude, self.longitude)
    def getyear(self):
        return self.year
    def getdata(self):
        return self.data
    
def getEnvData(df, variables, varHeader, 
               yearHeader, latHeader, longHeader):
    length1 = df.shape[0]
    for j in range(len(variables)):
        for i in range(length1):
            object1 = envVariable(df[latHeader][i], df[longHeader][i], df[yearHeader][i], df[varHeader[j]][i])
            variables[j].append(object1)

def splitData(xVals, yVals):
    toTrain = random.sample(range(len(xVals)),
                            len(xVals)//2)
    trainX, trainY, testX, testY = [],[],[],[]
    for i in range(len(xVals)):
        if i in toTrain:
            trainX.append(xVals[i])
            trainY.append(yVals[i])
        else:
            testX.append(xVals[i])
            testY.append(yVals[i])
    return trainX, trainY, testX, testY          
    
outPath = 'outputGraphs'
curTime = datetime.datetime.now()
curTime = curTime.strftime("%Y%m%d%H%M%S")
# print(curTime)
myFilePath = 'airPortData.csv'
myDataframe = getDataPd(myFilePath)
tempData = []
precipData = []
envVar = [tempData, precipData]
varNames = ['TAVG', 'PRCP']
plotTitles = ['Temperature', 'Precipitation']
yearH = 'DATE'
latH = 'LATITUDE'
longH = 'LONGITUDE'
futureYears = [2030,2040,2050,2060,2070,2080]
#print(myDataframe[latH][4], myDataframe[longH][4], myDataframe[yearH][4], my)
getEnvData(myDataframe, envVar, varNames, yearH, latH, longH)
#print(tempData[2].getdata())


for k in range(len(envVar)):
    xvals, yvals = [], []
    for data1 in envVar[k]:
        xvals.append(data1.getyear())
        yvals.append(data1.getdata())
    xvals, yvals = xvals[:-1], yvals[:-1]
    
    numSubsets = 10
    dimensions = (1, 2, 3, 4)
    rSquares = {}
    rSqMeanStd = []
    for d in dimensions:
        rSquares[d] = []
            
    for f in range(numSubsets):
        trainX, trainY, testX, testY = splitData(xvals, yvals)
        for d in dimensions:
            model = pylab.polyfit(trainX, trainY, d)
            estYVals = pylab.polyval(model, testX)
            rSquares[d].append(rSquared(testY, estYVals))
    print('Curves for -> '+plotTitles[k])
    print('Mean R-squares for test data')
    # print(rSquares)
    for d in dimensions:
        mean = round(sum(rSquares[d])/len(rSquares[d]), 4)
        sd = round(numpy.std(rSquares[d]), 4)
        rSqMeanStd.append((d,mean,sd))
        print('For dimensionality', d, 'mean =', mean,
              'Std =', sd)
    bestFitDegi = 0
    for i in range(1,len(rSqMeanStd)):
        if rSqMeanStd[i][1]>rSqMeanStd[i-1][1]:
            bestFitDegi = i
        else:
            break
    model = pylab.polyfit(xvals,yvals,rSqMeanStd[bestFitDegi][0])
    estvals = pylab.polyval(model, xvals+ futureYears)
    plt.plot(xvals,yvals, label = 'Observed Data')
    plt.plot(xvals + futureYears , estvals,'--', color = 'red', label = 'Best fit curve')
    lastPointStr = '('+str(futureYears[-1])+', '+str(estvals[-1].round(1))+')'
    plt.annotate(lastPointStr, (futureYears[-1],estvals[-1]))
    plt.grid()
    plt.legend()
    plt.title(label=plotTitles[k])
    plt.savefig(curTime+plotTitles[k]+'.png')
    plt.show()

    # # #print(rSquares[1])