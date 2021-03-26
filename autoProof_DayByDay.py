# Author: Darren K.J. Chen
# Copyright © 2020 Darren ( Kuan-Ju ) Chen | All Rights Reserved

import csv
import math

print('Options Arbitrage Proof Program (*Auto*) | Powered by Darren K.J. Chen \nCopyright © 2020 Darren ( Kuan-Ju ) Chen | All Rights Reserved')

dataImportFile          =  input('Pls input the File Path, which use for import data >> ')
if dataImportFile      ==  '':
	dataImportFile      =  "D:\kjchen\Projects\OptionAnalysis\EN_20200901_TXO_OP_HISTORY6EFE9E00-D095-40CB-B08D-8D53240D3CDE.csv"

contractMonth           =  input('Pls input Contract Month >> ') # + '_MONTH'
if contractMonth.find('W') == -1:
	contractMonth = contractMonth + '  '

tradingSession          =  input('Is Trading Session Regular? (Type \'True\' or \'False\', Defalut is True) >> ')
if tradingSession      ==  'False':
	tradingSession      =  'After-Hours'
else:
	tradingSession      =  'Regular'

import_data             =  list()
stk_price_allow         =  list()
cmb_futures_price       =  list()
stk_price_min_allow     =  math.ceil(float(input('Pls input the price now  >> ')) / 100 - 3) * 100

for i in range(7):
	stk_price_allow.append(float(stk_price_min_allow + i * 100))

with open(dataImportFile, newline = '') as importData:
	data = csv.DictReader(importData)

	for datum in data:
		if float(datum['Strike Price']) in stk_price_allow and datum['Contract'] == 'TXO' and datum['Trading Session'] == tradingSession and datum['Contract Month(Week)'] == contractMonth:
			import_data.append(datum)

for i in range(14):
	tmp = 0
	print('------------------------')
	for j, k in import_data[i].items():
		print(j, ':', k)
	if i % 2 == 1:
		tmp = float(import_data[i]['Strike Price']) - float(import_data[i]['Open']) + float(import_data[i-1]['Open'])
		cmb_futures_price.append(tmp)
		print('>-------------<CMB. FUTURES PRICE>-------------<')
		print('%s Cmb. futures Price: %.5f' %(import_data[i]['Strike Price'], tmp))
		print('>---------------------<#-#>--------------------<')
		print('>----------------------------------------------<')
print('Cmb. futures price List:\n', cmb_futures_price)

cmb_futures_price_max_positions = [i for i, j in enumerate(cmb_futures_price) if j == max(cmb_futures_price)]
cmb_futures_price_min_positions = [i for i, j in enumerate(cmb_futures_price) if j == min(cmb_futures_price)]

print('>-------------<PORTFOLIO>-------------<')
for i in cmb_futures_price_min_positions:
	print('LONG  FUTURES: TXO -', import_data[i*2]['Strike Price'])
for i in cmb_futures_price_max_positions:
	print('SHORT FUTURES: TXO -', import_data[i*2]['Strike Price'])
print('** NOTE: Take one of LONG FUTURES n SHORT FUTURES **')
print('>----------------<#-#>----------------<')
print('>-------------------------------------<')

print('>-------------<CLOSE TRADE>-------------<')
LF_CALL_PROFIT =   float(import_data[cmb_futures_price_min_positions[0]*2]['Close'])   - float(import_data[cmb_futures_price_min_positions[0]*2]['Open'])
print('LF_CALL_PROFIT', LF_CALL_PROFIT)
LF_PUT_PROFIT  = - float(import_data[cmb_futures_price_min_positions[0]*2+1]['Close']) + float(import_data[cmb_futures_price_min_positions[0]*2+1]['Open'])
print('LF_PUT_PROFIT', LF_PUT_PROFIT)

SF_CALL_PROFIT = - float(import_data[cmb_futures_price_max_positions[0]*2]['Close'])   + float(import_data[cmb_futures_price_max_positions[0]*2]['Open'])
print('SF_CALL_PROFIT', SF_CALL_PROFIT)
SF_PUT_PROFIT  =   float(import_data[cmb_futures_price_max_positions[0]*2+1]['Close']) - float(import_data[cmb_futures_price_max_positions[0]*2+1]['Open'])
print('SF_PUT_PROFIT', SF_PUT_PROFIT)

print('## <TOTAL PROFIT : %.5f> ##' %(LF_CALL_PROFIT + LF_PUT_PROFIT + SF_CALL_PROFIT + SF_PUT_PROFIT))
print('>-----------------<#-#>-----------------<')
print('>---------------------------------------<')

while 1:
	pass
