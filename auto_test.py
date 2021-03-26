# Author: Darren K.J. Chen
# Copyright © 2020 Darren ( Kuan-Ju ) Chen | All Rights Reserved

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

print('\nOptions Arbitrage Proof Program (*Auto*) | Powered by Darren K.J. Chen \nCopyright © 2020 Darren ( Kuan-Ju ) Chen | All Rights Reserved')
print('\n===========================================\n')

def gpStrategy(min_line, max_line):
	rg = range(min_line, max_line)
	print('\n', opCurrentData.iloc[rg], '\n')

	cmbF_list  =  {}
	cmbF_price =  list()
	for i in rg:
		cmbF = float(opCurrentData.iloc[i, 6]) + float(opCurrentData.iloc[i, 2]) - float(opCurrentData.iloc[i, 9])
		cmbF_price.append(cmbF)
		cmbF_list.update({cmbF : i})
	print('Cmb. F. Price List:', cmbF_price)

	LF_STK = float(opCurrentData.iloc[cmbF_list[min(cmbF_price)], 6])
	SF_STK = float(opCurrentData.iloc[cmbF_list[max(cmbF_price)], 6])

	print('\n=====<<CALL>>=====')
	print('BUY  TXO - %.0f CALL' %LF_STK)
	print('SELL TXO - %.0f CALL' %SF_STK)

	print('\n=====<<PUT>>======')
	print('BUY  TXO - %.0f  PUT' %SF_STK)
	print('SELL TXO - %.0f  PUT' %LF_STK)

	print('\n==================')

	return max(cmbF_price) - min(cmbF_price)

while 1:
	start_line = int(input('Pls input start line code >> '))
	ln         = int(input('Pls input total LN.       >> '))

	driver = webdriver.PhantomJS()
	driver.get('https://info512.taifex.com.tw/Future/OptQuote_Norl.aspx')
	soup = BeautifulSoup(driver.page_source,'lxml')
	opCurrentData = pd.read_html(str(soup.select('#divDG')[0]),header=0)[0]

	tmp_dict = {}
	tmp_ls = list()
	for i in range(ln):
		tmp = gpStrategy(start_line + i, start_line + i + 4)
		tmp_ls.append(tmp)
		tmp_dict.update({tmp : i})
	print('MAX PROFIT is', gpStrategy(start_line + tmp_dict[max(tmp_ls)], start_line + tmp_dict[max(tmp_ls)] + 4))
	tmp = input('\nPress ENTER to refresh >> ')
