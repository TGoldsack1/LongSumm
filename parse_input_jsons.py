'''
Parses the json input files into different formats to be used a model inputs.
Author: Tomas Goldsack
'''

import os, json

paper_json_dir = "./json_inputs/"
summaries_dir = "./abstractive_summaries/by_clusters/"

# Load in as dictionaries
papers_dict = {}

i = 0

for json_file in os.listdir(paper_json_dir):
  paper_id = json_file.split('.')[0] 

  try:
    input_file = open(paper_json_dir + json_file)
    input_dict = json.load(input_file) # this is a json file output from science-parse v2
    input_file.close()

    if i == 0:
      page_tokens = [x['tokens'] for x in input_dict['doc']['pages']]
      print(page_tokens[0])
      # print([x['text'] for x in page_tokens])

    i += 1

    papers_dict[paper_id] = { 'X' : input_dict }
  
  except Exception as e:
    print(e)
    print(json_file)
    print(input_file.readlines())
    print("-"*30)

print('### COLLECTED INPUTS ###')
print(list(papers_dict.keys())[:10])
print(len(list(papers_dict.keys())))
print("#"*20)

for root, dirs, files in os.walk(summaries_dir):
  for filename in files:
    if filename.split('.')[1] == "json":

      try:
        summary_file = open(root + '/' + filename)
        summary_dict = json.load(summary_file)
        summary_file.close()

        papers_dict[str(summary_dict['id'])]['Y'] = summary_dict

      except Exception as e:
        print(e)
        print(filename)
        print("-"*30)

print("PRINTING")
with open("dataset.json", "w") as output_file:
  for key, value in papers_dict.items():
    if key and value:
      if 'X' in list(value.keys()) and 'Y' in list(value.keys()):
        output_file.write(json.dumps({ key: value }, indent=4, sort_keys=False))

## Long Summariser Pointer-Generator Cohan 2018

# Input format (json)
# { 
#   'article_id': str,
#   'abstract_text': List[str], # this is actually the summary 
#   'article_text': List[str],  # so this should include the abstract
#   'section_names': List[str],
#   'sections': List[List[str]]
# }


