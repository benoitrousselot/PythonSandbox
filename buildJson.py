import json
import csv
import requests


def BuildBasketComponents(sourceFile):
	basketComponents = []
	with open(sourceFile, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for line in csvfile.readlines():
			array = line.decode().split(',')
			basketComponents.append({'instrumentId': array[1], 'amount': float(array[2])})
	return basketComponents
	
basketId = 'myBasket'
basketCurrency = 'USD'
basketRiskFreeRate = 0.001
estimationWindow = 120
probabilityLevel = 'Percent97'
horizon = 1

data = {}  
data['basket'] = { 'basketId': basketId, 'currency': basketCurrency, 'components': BuildBasketComponents('spx.csv'), 'riskFreeRate': basketRiskFreeRate }
data['estimationWindow'] = estimationWindow
data['probabilityLevel'] = probabilityLevel
data['horizon'] = horizon
		
with open('jsonData.txt', 'w') as outfile:  
    json.dump(data, outfile, indent=2)
	
url = 'http://ps-tb-02/custom-baskets/v1/exante-analysis'
response = requests.post(url, data = data)

print(response)