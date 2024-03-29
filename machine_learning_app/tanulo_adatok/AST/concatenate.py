"""
This file concatenates the CSVs.
"""

import os
import pandas as pd
import glob

entries = os.listdir()
lines = []
db = 0

for entry in entries:
	if os.path.splitext(entry)[1] == '.csv' and os.path.splitext(entry)[0] != 'concatenated' and os.path.splitext(entry)[0] != 'concatenated_titled' and os.path.splitext(entry)[0] != 'toimport_vulnerabilities_ast':
		db += 1
		with open(entry, 'r') as f:
			for line in f:
				lines.append(line)

with open('concatenated.csv', 'w') as ff:
	for i in lines:
		ff.write(i)