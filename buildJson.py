import json
import csv
import requests

class Basket:
	def __init__(self, basketId, basketCurrency, basketCompositionPath, basketRiskFreeRate):
		self.basketId = basketId
		self.basketCurrency = basketCurrency
		self.basketCompositionPath = basketCompositionPath
		self.basketRiskFreeRate = basketRiskFreeRate

def BuildOptimisationJsonData(basket, estimationWindow, optimisationTarget, benchmark=None, instMin=None, instMax=None, maxConstituants=None, adv=None, borrowRate=None, maxTurnover=None):
	data = {}  
	data['basket'] = BuildBasket(basket)
	if (benchmark != None):
		data['benchmark'] = BuildBasket(benchmark)	
	data['estimationWindow'] = estimationWindow
	data['optimisationTarget'] = optimisationTarget
	if (instMin == None and instMax == None):
		instrumentMinMaxWeight = None
	else:
		if (instMin == None):
			instMin = 0			
		if (instMax == None):
			instMax = 100		
		instrumentMinMaxWeight = { 'min': instMin, 'max' : instMax }		
	data['instrumentMinMaxWeight'] = instrumentMinMaxWeight
	if (maxConstituants != None):
		data[''] = maxConstituants
	if (adv != None):
		data['averageDailyVolume'] = adv
	if (borrowRate != None):
		data['borrowRate'] = borrowRate
	if (maxTurnover != None):
		data['maxTurnover'] = maxTurnover		
	return data

def BuildFactorialAnalysisJsonData(basket, estimationWindow, probabilityLevel, factorsList):
	data = {}  
	data['basket'] = BuildBasket(basket)
	data['estimationWindow'] = estimationWindow
	data['probabilityLevel'] = probabilityLevel
	data['factorList'] = factorsList
	return data
	
def BuildBacktestJsonDataWithBenchmark(basket, benchmark, probabilityLevel, startDate, endDate):
	data = BuildBacktestJsonData(basket, probabilityLevel, startDate, endDate)
	data['benchmark'] = BuildBasket(benchmark)	
	return data
	
def BuildBacktestJsonData(basket, probabilityLevel, startDate, endDate):
	data = {}  
	data['basket'] = BuildBasket(basket)
	data['probabilityLevel'] = probabilityLevel
	data['startDate'] = startDate
	data['endDate'] = endDate
	return data
	
def BuildExanteAnalysisJsonDataWithBenchmark(basket, benchmark, estimationWindow, probabilityLevel, horizon):
	data = BuildExanteAnalysisJsonData(basket, estimationWindow, probabilityLevel, horizon)
	data['benchmark'] = BuildBasket(benchmark)	
	return data
	
def BuildExanteAnalysisJsonData(basket, estimationWindow, probabilityLevel, horizon):
	data = {}  
	data['basket'] = BuildBasket(basket)
	data['estimationWindow'] = estimationWindow
	data['probabilityLevel'] = probabilityLevel
	data['horizon'] = horizon
	return data

def BuildBasket(basket):
	return { 'basketId': basket.basketId, 'currency': basket.basketCurrency, 'components': BuildBasketComponents(basket.basketCompositionPath), 'riskFreeRate': basket.basketRiskFreeRate }

def BuildBasketComponents(sourceFile):
	basketComponents = []
	with open(sourceFile, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for line in csvfile.readlines():
			array = line.decode().split(',')
			basketComponents.append({'instrumentId': array[1], 'amount': float(array[2])})
	return basketComponents

	
	
	
# Define constants
basketId = 'myBasket'
benchmarkId = 'myBench'
basketCurrency = 'USD'
basketRiskFreeRate = 0.001
estimationWindow = 120
probabilityLevel = 'Percent97'
horizon = 1
startDate = '2017-02-01'
endDate = '2017-03-01'
factorsList = ['BCOM Index', 'BDIY Index']


# Build basket
basket = Basket(basketId, basketCurrency, 'spx.csv', basketRiskFreeRate)

# Build benchmark
benchmark = Basket(benchmarkId, basketCurrency, 'spx.csv', basketRiskFreeRate)

# Build json data
factoData = BuildFactorialAnalysisJsonData(basket, estimationWindow, probabilityLevel, factorsList)
backtestData = BuildBacktestJsonDataWithBenchmark(basket, benchmark, 'Percent97', startDate, endDate)
exanteData = BuildExanteAnalysisJsonDataWithBenchmark(basket, benchmark, 120, 'Percent97', 1)
optimData = BuildOptimisationJsonData(basket, 120, 'equiWeight', instMax = 0.2)
	
	
# Dump json data
with open('factoJsonData.txt', 'w') as outfile:  
    json.dump(factoData, outfile, indent=2)
with open('backtestJsonData.txt', 'w') as outfile:  
    json.dump(backtestData, outfile, indent=2)
with open('exanteJsonData.txt', 'w') as outfile:  
    json.dump(exanteData, outfile, indent=2)
with open('optimJsonData.txt', 'w') as outfile:  
    json.dump(optimData, outfile, indent=2)
	
	
# Call web services
	
#url = 'http://ps-tb-02/custom-baskets/v1/exante-analysis'
#response = requests.post(url, data = data)
#print(response.text)