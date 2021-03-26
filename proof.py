# Author: Darren K.J. Chen
# Copyright © 2020 Darren ( Kuan-Ju ) Chen | All Rights Reserved

print('Options Arbitrage Proof Program (Manual) | Powered by Darren K.J. Chen \nCopyright © 2020 Darren ( Kuan-Ju ) Chen | All Rights Reserved')

# import datetime as d
#
# year           = int(input('Pls input trade year >> '))
# month          = int(input('Pls input trade month >> '))
# day            = int(input('Pls input trade day >> '))
# date           = d.date(year, month, day)

contractName   = str(input('Pls input the contract name >> '))  # e.g. 'TXO'
contractMonth  = str(input('Pls input the contract month >> ')) # e.g. '202009'

def main():
	f1_LONG = True
	f1_strikePrice       = float(input('Pls input futures 1 strike price >> '))
	f2_strikePrice       = float(input('Pls input futures 2 strike price >> '))

	f1_call_openPrice    = float(input('Pls input futures 1 call open price >> '))
	f1_put_openPrice     = float(input('Pls input futures 1 put open price >> '))
	f2_call_openPrice    = float(input('Pls input futures 2 call open price >> '))
	f2_put_openPrice     = float(input('Pls input futures 2 put open price >> '))

	f1_cmb_price = f1_strikePrice - f1_put_openPrice + f1_call_openPrice
	f2_cmb_price = f2_strikePrice - f2_put_openPrice + f2_call_openPrice

	print('Futures 1 Cmb. Price : %.5f' %f1_cmb_price)
	print('Futures 2 Cmb. Price : %.5f' %f2_cmb_price)

	if abs(f1_cmb_price - f2_cmb_price) < 10:
		print('** This combination is not recommended **')
		return;
	if f1_cmb_price > f2_cmb_price:
		print('Buy %s - %s - %.0f PUT / cost: %.5f'   %(contractName, contractMonth, f1_strikePrice, f1_put_openPrice))
		print('Sell %s - %s - %.0f CALL / cost: %.5f' %(contractName, contractMonth, f1_strikePrice, f1_call_openPrice))
		print('Buy PUT + Sell CALL become SHORT FUTURES, code 1')

		print('Sell %s - %s - %.0f PUT / cost: %.5f'  %(contractName, contractMonth, f2_strikePrice, f2_put_openPrice))
		print('Buy %s - %s - %.0f CALL / cost: %.5f'  %(contractName, contractMonth, f2_strikePrice, f2_call_openPrice))
		print('Sell PUT + Buy CALL become LONG FUTURES, code 2')
	else:
		f1_LONG = not f1_LONG
		print('Sell %s - %s - %.0f PUT / cost: %.5f'  %(contractName, contractMonth, f1_strikePrice, f1_put_openPrice))
		print('Buy %s - %s - %.0f CALL / cost: %.5f'  %(contractName, contractMonth, f1_strikePrice, f1_call_openPrice))
		print('Sell PUT + Buy CALL become LONG FUTURES, code 1')

		print('Buy %s - %s - %.0f PUT / cost: %.5f'   %(contractName, contractMonth, f2_strikePrice, f2_put_openPrice))
		print('Sell %s - %s - %.0f CALL / cost: %.5f' %(contractName, contractMonth, f2_strikePrice, f2_call_openPrice))
		print('Buy PUT + Sell CALL become SHORT FUTURES, code 2')

	f1_call_closePrice   = float(input('Pls input futures 1 call close price >> '))
	f1_put_closePrice    = float(input('Pls input futures 1 put close price >> '))
	f2_call_closePrice   = float(input('Pls input futures 2 call close price >> '))
	f2_put_closePrice    = float(input('Pls input futures 2 put close price >> '))

	print('Futures 1 is LONG :', f1_LONG)

	if f1_LONG:
		f1_put_profit    =  - f1_put_closePrice   +  f1_put_openPrice
		f1_call_profit   =  - f1_call_openPrice   +  f1_call_closePrice
		f2_put_profit    =  - f2_put_openPrice    +  f2_put_closePrice
		f2_call_profit   =  - f2_call_closePrice  +  f2_call_openPrice

		print('[Close Time]')
		print('LONG %s - %s - %.0f PUT / cost: %.5f'   %(contractName, contractMonth, f1_strikePrice, f1_put_openPrice))
		print('--> Close Price: %.5f / Profit: %.5f'   %(f1_put_closePrice, f1_put_profit))
		print('SHORT %s - %s - %.0f CALL / cost: %.5f' %(contractName, contractMonth, f1_strikePrice, f1_call_openPrice))
		print('--> Close Price: %.5f / Profit: %.5f'   %(f1_call_closePrice, f1_call_profit))

		print('SHORT %s - %s - %.0f PUT / cost: %.5f'  %(contractName, contractMonth, f2_strikePrice, f2_put_openPrice))
		print('--> Close Price: %.5f / Profit: %.5f'   %(f2_put_closePrice, f2_put_profit))
		print('LONG %s - %s - %.0f CALL / cost: %.5f'  %(contractName, contractMonth, f2_strikePrice, f2_call_openPrice))
		print('--> Close Price: %.5f / Profit: %.5f'   %(f2_call_closePrice, f2_call_profit))
	else:
		f1_put_profit    =  f1_put_closePrice   -  f1_put_openPrice
		f1_call_profit   =  f1_call_openPrice   -  f1_call_closePrice
		f2_put_profit    =  f2_put_openPrice    -  f2_put_closePrice
		f2_call_profit   =  f2_call_closePrice  -  f2_call_openPrice

		print('[Close Time]')
		print('SHORT %s - %s - %.0f PUT / cost: %.5f'  %(contractName, contractMonth, f1_strikePrice, f1_put_openPrice))
		print('--> Close Price: %.5f / Profit: %.5f'   %(f1_put_closePrice, f1_put_profit))
		print('LONG %s - %s - %.0f CALL / cost: %.5f'  %(contractName, contractMonth, f1_strikePrice, f1_call_openPrice))
		print('--> Close Price: %.5f / Profit: %.5f'   %(f1_call_closePrice, f1_call_profit))

		print('LONG %s - %s - %.0f PUT / cost: %.5f'   %(contractName, contractMonth, f2_strikePrice, f2_put_openPrice))
		print('--> Close Price: %.5f / Profit: %.5f'   %(f2_put_closePrice, f2_put_profit))
		print('SHORT %s - %s - %.0f CALL / cost: %.5f' %(contractName, contractMonth, f2_strikePrice, f2_call_openPrice))
		print('--> Close Price: %.5f / Profit: %.5f'   %(f2_call_closePrice, f2_call_profit))
	print('[RESULT] Totol Profit : %.5f' %(f1_put_profit + f1_call_profit + f2_put_profit + f2_call_profit))

while 1:
	main()

# op_info_fmt = {
#     'tradeDate'         : '19880808',
#     'contractName'      : 'TXO',
# 	'contractMonth'     : '198808',
#     'strikePrice'       : -8.88888,
# 	'call_openPrice'    : -8.88888,
# 	'put_openPrice'     : -8.88888,
# 	'cmb_price'         : -8.88888,
#
# 	'call_closePrice'   : -8.88888,
# 	'put_closePrice'    : -8.88888,
#
# 	'put_profit'        : -8.88888,
# 	'call_profit'       : -8.88888
# }
