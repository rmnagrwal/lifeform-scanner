# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 18:28:21 2020

@author: Raman Agarwal
"""


import random, pylab, numpy
import pandas as pd

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

def getDataPd(filepath1, header1 = [0]):
    df = pd.read_csv(filepath1, header = header1 )
    return df

def rSquared(observed, predicted):
    error = ((predicted - observed)**2).sum()
    # print(error)
    meanError = error/len(observed)
    # print(meanError,numpy.var(observed))
    return (1 - (meanError/numpy.var(observed)))

def genFits(xVals, yVals, degrees):
    models = []
    for d in degrees:
        model = pylab.polyfit(xVals, yVals, d)
        models.append(model)
    return models

def testFits(models, degrees, xVals, yVals, title):
    pylab.plot(xVals, yVals, 'o', label = 'Data')
    for i in range(len(models)):
        estYVals = pylab.polyval(models[i], xVals)
        error = rSquared(yVals, estYVals)
        pylab.plot(xVals, estYVals,
                   label = 'Fit of degree '\
                   + str(degrees[i])\
                   + ', R2 = ' + str(round(error, 5)))
    pylab.legend(loc = 'best')
    pylab.title(title)

def getData(fileName):
    dataFile = open(fileName, 'r')
    distances = []
    masses = []
    dataFile.readline() #discard header
    for line in dataFile:
        d, m = line.split()
        distances.append(float(d))
        masses.append(float(m))
    dataFile.close()
    return (masses, distances)
    
def labelPlot():
    pylab.title('Measured Displacement of Spring')
    pylab.xlabel('|Force| (Newtons)')
    pylab.ylabel('Distance (meters)')

def plotData(fileName):
    xVals, yVals = getData(fileName)
    xVals = pylab.array(xVals)
    yVals = pylab.array(yVals)
    xVals = xVals*9.81  #acc. due to gravity
    pylab.plot(xVals, yVals, 'bo',
               label = 'Measured displacements')
    labelPlot()
    
def fitData(fileName):
    xVals, yVals = getData(fileName)
    xVals = pylab.array(xVals)
    yVals = pylab.array(yVals)
    xVals = xVals*9.81 #get force
    pylab.plot(xVals, yVals, 'bo',
               label = 'Measured points')                 
    model = pylab.polyfit(xVals, yVals, 1)
    xVals = xVals + [2]
    yVals = yVals + []
    estYVals = pylab.polyval(model, xVals)
    pylab.plot(xVals, estYVals, 'r',
               label = 'Linear fit, r**2 = '
               + str(round(rSquared(yVals, estYVals), 5)))                
    model = pylab.polyfit(xVals, yVals, 2)
    estYVals = pylab.polyval(model, xVals)
    pylab.plot(xVals, estYVals, 'g--',
               label = 'Quadratic fit, r**2 = '
               + str(round(rSquared(yVals, estYVals), 5)))
    pylab.title('A Linear Spring')
    labelPlot()
    pylab.legend(loc = 'best')
    
random.seed(0)

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
            
    
    
# def getTempData(fileName):
#     inFile = open(fileName)
#     fileLines = list(inFile)
#     data = []
#     for i in range(0,28):
#         data.append(tempDatum(fileLines[i]))
#     return data
    
# def getYearlyMeans(data):
#     years = {}
#     for d in data:
#         try:
#             years[d.getYear()].append(d.gettemp())
#         except:
#             years[d.getYear()] = [d.gettemp()]
#     for y in years:
#         years[y] = sum(years[y])/len(years[y])
#     #print(years)
#     return years
    
# data = getTempData('tempData.csv')

myFilePath = 'airPortData.csv'
myDataframe = getDataPd(myFilePath)
tempData = []
precipData = []
envVar = [tempData, precipData]
varNames = ['TMAX', 'PRCP']
yearH = 'DATE'
latH = 'LATITUDE'
longH = 'LONGITUDE'
#print(myDataframe[latH][4], myDataframe[longH][4], myDataframe[yearH][4], my)
getEnvData(myDataframe, envVar, varNames, yearH, latH, longH)
#print(tempData[2].getdata())
xvals, yvals = [], []
for data1 in tempData:
    xvals.append(data1.getyear())
    yvals.append(data1.getdata())
xvals, yvals = xvals[:-1], yvals[:-1]
pylab.plot(xvals,yvals)
futureYears = [2030,2040,2050,2060,2070,2080]
# print(xvals[-1])
# print(len(xvals), len(yvals))
# model = pylab.polyfit(xvals, yvals, 3)
# estvals = pylab.polyval(model, xvals+ futureYears)
# pylab.plot(xvals + futureYears , estvals)

# dataSet1 = {}
# dataSet1['x'] = []
# dataSet1['y'] = []
# dataSet2 = {}
# dataSet2['x'] = []
# dataSet2['y'] = []
# for i in range(len(data)):
#     if data[i].getYear()==2003:
#         dataSet1['x'].append(data[i].getmonth())
#         dataSet1['y'].append(data[i].gettemp())
        
#     if data[i].getYear()==2004:
#         dataSet2['x'].append(data[i].getmonth())
#         dataSet2['y'].append(data[i].gettemp())
# pylab.plot(dataSet1['x'], dataSet1['y'], 'blue')
# pylab.plot(dataSet2['x'], dataSet2['y'], 'red')
# model = pylab.polyfit(dataSet1['x'], dataSet1['y'],4)
# estvals = pylab.polyval(model, dataSet2['x'] )
# pylab.plot(dataSet2['x'], estvals, '--', 'green')

        
# years = getYearlyMeans(data)
# xVals, yVals = [], []
# for e in sorted(years):
#     xVals.append(e)
#     yVals.append(years[e])
# # print(xVals)
# # print(yVals)
# pylab.plot(xVals, yVals)
# pylab.xlabel('Year')
# pylab.ylabel('Mean yearly temp (C)')
# pylab.title('Temperature data')
      
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
    
# # #UNCOVER FOR SECOND DEMO    
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
pylab.plot(xvals + futureYears , estvals)
# # #print(rSquares[1])