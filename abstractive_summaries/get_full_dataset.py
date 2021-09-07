'''
Combines the article and summary jsons to form full matched dataset.
Author: Tomas Goldsack
'''

import os, json, random

paper_json_dir = "./json/"
summaries_dir = "./by_clusters/"

# Load in as dictionaries
papers_dict = {}

# Load in the source data (paper content)
for json_file in os.listdir(paper_json_dir):
  paper_id = json_file.split('.')[0] 

  try:
    input_file = open(paper_json_dir + json_file)
    input_dict = json.load(input_file) # this is a json file output from science-parse
    input_file.close()

    papers_dict[paper_id] = { 'X' : input_dict }
  
  except Exception as e:
    print(e)
    print(json_file)
    print(input_file.readlines())
    print("-"*30)

# print('### COLLECTED INPUTS ###')
# print(list(papers_dict.keys())[:10])
# print(len(list(papers_dict.keys())))
# print("#"*20)

# Load in the ground truth data (paper summaries)
for root, dirs, files in os.walk(summaries_dir):
  for filename in files:
    if filename.split('.')[1] == "json":

      try:
        summary_file = open(root + '/' + filename)
        summary_dict = json.load(summary_file)
        summary_file.close()

        print(summary_dict['id'])

        papers_dict[str(summary_dict['id'])]['Y'] = summary_dict

      except Exception as e:
        print("Error:")
        print(e)
        print(filename)
        print("-"*30)


papers_dict_full = { k : v for k, v in papers_dict.items() if k and v}
papers_dict_full = { k : v for k, v in papers_dict_full.items() if ('X' in list(v.keys()) and 'Y' in list(v.keys()))}#

print("Papers where all data is there: ", len(papers_dict_full.keys()))

not_full = { k : v for k, v in papers_dict.items() if k not in papers_dict_full.keys() }

print("Papers with missing data (X or Y): ", len(not_full.keys()))

with open("missing_data_instances.json", "w") as output_file: # none of these have summaries
  output_file.write(json.dumps(not_full, indent=4, sort_keys=False))


# with open("all_longsumm_abs_full.json", "w") as output_file:
#   output_file.write(json.dumps(my_train, indent=4, sort_keys=False))

random.seed(0)
test_size = 21

# Extract my test data
my_test_dict_ids = random.sample(list(papers_dict_full.keys()), test_size) 

my_test = { k : v for k, v in papers_dict_full.items() if k in my_test_dict_ids }
my_train = { k : v for k, v in papers_dict_full.items() if k not in my_test_dict_ids }

print("My training set length: ", len(my_train.keys()))
print("My test set length: ", len(my_test.keys()))

# with open("my_longsumm_train_abs.json", "w") as output_file:
#   output_file.write(json.dumps(my_train, indent=4, sort_keys=False))

# with open("my_longsumm_test_abs.json", "w") as output_file:
#   output_file.write(json.dumps(my_test, indent=4, sort_keys=False))