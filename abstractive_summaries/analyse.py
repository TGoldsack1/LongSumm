'''
Analyse the abstractive summaries of LongSumm to determine which section they
most commonly are derived from. 
Author: Tomas Goldsack
'''

import json

input_file = "./all_longsumm_abs_full.json"

longsumm_file = open(input_file)
longsumm_dict = json.load(longsumm_file)
longsumm_file.close()

# Iterate through instances 
for X, Y in longsumm_dict.items():
  
