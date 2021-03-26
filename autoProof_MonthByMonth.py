# Author: Darren K.J. Chen
# Copyright © 2020 Darren ( Kuan-Ju ) Chen | All Rights Reserved

# ------------DEBUG------------
# Traceback (most recent call last):
#   File "autoProof_MonthByMonth.py", line 143, in <module>
#     DAILY_TOTAL_PROFIT_LIST.append(dayProof(key.replace("/0", "").replace("/", ""), key))
#   File "autoProof_MonthByMonth.py", line 63, in dayProof
#     for j, k in op_import_data[i].items():
# IndexError: list index out of range

import csv
import math

print('\nOptions Arbitrage Proof Program (*Auto*) | Powered by Darren K.J. Chen \nCopyright © 2020 Darren ( Kuan-Ju ) Chen | All Rights Reserved')
print('\n===========================================\n')

tradeMonth                          =    input('Pls input Trade Month >> ')

OP_dataImportFile                   =    input('Pls input the File Path, which use for import Options Historical Data >> ')
if OP_dataImportFile               ==    '':
	OP_dataImportFile               =    "D:\kjchen\Database\OPTIONS_TXO_Historical_Data\OP_" + tradeMonth + ".csv"
	print('Defalut << %s' %OP_dataImportFile)

INDEX_dataImportFile                =    input('Pls input the File Path, which use for import Total INDEX Historical Data >> ')
if INDEX_dataImportFile            ==    '':
	INDEX_dataImportFile            =    "D:\kjchen\Database\TAIEX_Total_Index_Historical_Data\INDEX_" + tradeMonth + ".csv"
	print('Defalut << %s' %INDEX_dataImportFile)

contractMonth                       =    input('Pls input Contract Month >> ')
if contractMonth.find('W')         ==    -1:
	contractMonth = contractMonth   +    '  '

tradingSession                      =    input('Is Trading Session Regular? (Type \'True\' or \'False\', Defalut is True) >> ')
if tradingSession                  ==    'False':
	tradingSession                  =    'After-Hours'
else:
	tradingSession                  =    'Regular'
	print('Defalut << Regular')


index_import_data                   =    {}
with open(INDEX_dataImportFile, newline = '') as importData:
	data                            =   csv.DictReader(importData)
	tmp                             =   0
	for datum in data:
		tmp += 1
		if tmp > 2:
			index_import_data.update({datum[tradeMonth[0] + tradeMonth[1] + tradeMonth[2] + tradeMonth[3] + '/' + tradeMonth[4] + tradeMonth[5] + ' TAIEX Total Index Historical Data'] : datum[None][0].replace(',', '')})

dailyCost                           =    list()
def dayProof(dt, dt_key):
	op_import_data                  =    list()

	stk_price_allow                 =    list()
	stk_price_min_allow             =    math.ceil(float(index_import_data[dt_key]) / 100 - 3) * 100
	for i in range(7):
		stk_price_allow.append(float(stk_price_min_allow + i * 100))

	with open(OP_dataImportFile, newline = '') as importData:
		data = csv.DictReader(importData)
		for datum in data:
			if float(datum['Strike Price']) in stk_price_allow and datum['Date'].replace("/0", "").replace("/", "") == dt and datum['Trading Session'] == tradingSession and datum['Contract Month(Week)'] == contractMonth and datum['Contract'] == 'TXO':
				op_import_data.append(datum)

	cmb_futures_price               =    list()
	tmp_cmb_futures_price           =    list()
	for i in range(14):
		tmp = 0
		print('------------------------')
		for j, k in op_import_data[i].items():
			print(j, ':', k)
		if i % 2 == 1:
			try:
				if op_import_data[i]['Close']     !=  '-' and op_import_data[i-1]['Close'] != '-':
					tmp = float(op_import_data[i]['Strike Price']) - float(op_import_data[i]['Open']) + float(op_import_data[i-1]['Open'])
					tmp_cmb_futures_price.append(tmp)
					print('>-------------<CMB. FUTURES PRICE>-------------<')
					print('%s Cmb. futures Price: %.5f' %(op_import_data[i]['Strike Price'], tmp))
					print('>---------------------<#-#>--------------------<')
					print('>----------------------------------------------<')
				else:
					op_import_data[i]['Close']    +=  1
					op_import_data[i-1]['Close']  +=  1

			except:
				tmp = -8.88888
				print('>-------------<CMB. FUTURES PRICE>-------------<')
				print('%s Cmb. futures Price: %s' %(op_import_data[i]['Strike Price'], 'NULL'))
				print('>---------------------<#-#>--------------------<')
				print('>----------------------------------------------<')
				continue

			finally:
				cmb_futures_price.append(tmp)

	print('Cmb. futures price List:\n', tmp_cmb_futures_price)

	cmb_futures_price_max_positions =   [i for i, j in enumerate(cmb_futures_price) if j == max(tmp_cmb_futures_price)]
	cmb_futures_price_min_positions =   [i for i, j in enumerate(cmb_futures_price) if j == min(tmp_cmb_futures_price)]

	print('>-------------<PORTFOLIO>-------------<')
	for i in cmb_futures_price_min_positions:
		print('LONG  FUTURES: TXO -', op_import_data[i*2]['Strike Price'])
	for i in cmb_futures_price_max_positions:
		print('SHORT FUTURES: TXO -', op_import_data[i*2]['Strike Price'])
	print('** NOTE: Take one of LONG FUTURES n SHORT FUTURES **')
	print('>----------------<#-#>----------------<')
	print('>-------------------------------------<')

	print('>-------------<CLOSE TRADE>-------------<')
	# float(index_import_data[dt_key])
	TXO_A_VALUE    =   41000
	TXO_B_VALUE    =   21000
	TXO_MULT       =   50

	LF_CALL_COST   =   float(op_import_data[cmb_futures_price_min_positions[0]*2]['Open']   ) * TXO_MULT
	LF_CALL_PROFIT =   float(op_import_data[cmb_futures_price_min_positions[0]*2]['Close']  ) - float(op_import_data[cmb_futures_price_min_positions[0]*2]['Open'])
	print('LF_CALL_COST'  , LF_CALL_COST)
	print('LF_CALL_PROFIT', LF_CALL_PROFIT)

	LF_PUT_COST    =   float(op_import_data[cmb_futures_price_min_positions[0]*2+1]['Open'] ) + max(float(TXO_A_VALUE)  - max((-float(op_import_data[cmb_futures_price_min_positions[0]*2+1]['Strike Price']) + float(index_import_data[dt_key])) * TXO_MULT, 0), float(TXO_B_VALUE))
	LF_PUT_PROFIT  = - float(op_import_data[cmb_futures_price_min_positions[0]*2+1]['Close']) + float(op_import_data[cmb_futures_price_min_positions[0]*2+1]['Open'])
	print('LF_PUT_COST'  , LF_PUT_COST)
	print('LF_PUT_PROFIT', LF_PUT_PROFIT)

	SF_CALL_COST    =  float(op_import_data[cmb_futures_price_max_positions[0]*2+1]['Open'] ) + max(float(TXO_A_VALUE) - max((float(op_import_data[cmb_futures_price_max_positions[0]*2]['Strike Price'])  - float(index_import_data[dt_key])) * TXO_MULT, 0), float(TXO_B_VALUE))
	SF_CALL_PROFIT = - float(op_import_data[cmb_futures_price_max_positions[0]*2]['Close']  ) + float(op_import_data[cmb_futures_price_max_positions[0]*2]['Open'])
	print('SF_CALL_COST', SF_CALL_COST)
	print('SF_CALL_PROFIT', SF_CALL_PROFIT)

	SF_PUT_COST    =   float(op_import_data[cmb_futures_price_max_positions[0]*2+1]['Open'] ) * TXO_MULT
	SF_PUT_PROFIT  =   float(op_import_data[cmb_futures_price_max_positions[0]*2+1]['Close']) - float(op_import_data[cmb_futures_price_max_positions[0]*2+1]['Open'])
	print('SF_PUT_COST', SF_PUT_COST)
	print('SF_PUT_PROFIT', SF_PUT_PROFIT)

	TOTAL_COST = LF_CALL_COST + LF_PUT_COST + SF_CALL_COST + SF_PUT_COST
	dailyCost.append(TOTAL_COST)
	print('## <TOTAL COST : %.5f> ##' %TOTAL_COST)

	TOTAL_PROFIT   = LF_CALL_PROFIT + LF_PUT_PROFIT + SF_CALL_PROFIT + SF_PUT_PROFIT
	print('## <TOTAL PROFIT : %.5f> ##' %TOTAL_PROFIT)

	print('>-----------------<#-#>-----------------<')
	print('>---------------------------------------<')

	return TOTAL_PROFIT

DAILY_TOTAL_PROFIT_LIST = list()
for key in index_import_data:
	DAILY_TOTAL_PROFIT_LIST.append(dayProof(key.replace("/0", "").replace("/", ""), key))

print('>-------------<MONTH  PROFIT>-------------<')

MONTH_TATAL_PROFIT = 0
print('MONTH PROFIT = %.5f\n-------------------------------------------\n' %MONTH_TATAL_PROFIT)
for i in DAILY_TOTAL_PROFIT_LIST:
	MONTH_TATAL_PROFIT += i
	print('MONTH PROFIT + %.5f = %.5f' %(i, MONTH_TATAL_PROFIT))
print('Daily Cost:', dailyCost)
print('\nMAX COST =', max(dailyCost))

print('\n** MONTH RESULT PROFIT = %.5f **\n' %MONTH_TATAL_PROFIT)

print('=>-------##--------<=|=>-------##--------<=')
print('>-----------------------------------------<')
print('\n===========================================')

while 1:
	pass
