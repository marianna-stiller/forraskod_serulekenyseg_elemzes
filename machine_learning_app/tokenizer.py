"""
This file selects the important values from the ASTs and writes into CSVs.

For example:
acunetix_ast.txt line 2:	"kind": "program",
acunetix_ast.csv word 1:	program
"""

import csv
import os

array = []

with os.scandir('tanulo_adatok/AST/') as entries:
	for entry in entries:
		if os.path.splitext(entry)[1] == '.txt':
			try:
				with open(entry, 'r', encoding='utf-8') as f:
					data = f.read()
					data_1 = data.replace('"', '').replace(',', '').replace('{', '').replace('}', '').split('\n')

					for i in data_1:
						if 'kind:' in i:
							array.append(i.replace('kind:','').strip())
						if 'name:' in i:
							array.append(i.replace('name:','').strip())
						if 'raw:' in i:
							array.append(i.replace('raw:','').strip())

			except Exception as e:
				print('FILE: ',entry)
				print('PROBLEM: ',e)

			def listToString(array):
				string = " "
				return(string.join(array))

			listed = listToString(array)

			with open(os.path.splitext(entry)[0]+'.csv', 'w', newline='', encoding='utf-8') as e_f:
				writer = csv.writer(e_f,delimiter='^')
				writer.writerow([listed,""])
			array = []