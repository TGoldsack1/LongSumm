'''
Parses longsummm dataset json file to make format input for the given model.
Input size is kept at full document text
Author: Tomas Goldsack
'''

import os, json, re
from nltk.tokenize import sent_tokenize

mode = "train"

longsumm_file = open(f"./my_longsumm_{mode}_abs_full_science_parse.json")
longsumm_dict = json.load(longsumm_file)
longsumm_file.close()

# Desired input format (json)
# { 
#   "article_lines": List[str],
#   "summary_lines": List[str]
# }

doc_datafile = open(f"./my_longsumm_{mode}_abs_doc.jsonl", "w")

for paper_id, paper_dict in longsumm_dict.items():

  doc_data = {}
  article_lines = []
  
  summary_sents = paper_dict['Y']['summary']
  input_dict = paper_dict['X'] 
  # X format:
  # {
  #   "sections": [{ "heading": str, "text": str }], 
  #   "year": int,
  #   "references": [{...}],
  #   "id" : str,
  #   "authors" : [{ "name": str, "affiliations": str }]
  #   "abstractText": str,
  #   "title": str
  # }

  doc_data["summary_lines"] = summary_sents

  # A section (abstract)
  if "abstractText" in input_dict.keys():
    article_lines = article_lines + sent_tokenize(input_dict["abstractText"])

  # Get IC sectionsstr
  if 'sections' in input_dict.keys():

    for section in input_dict['sections']:
      article_lines = article_lines + sent_tokenize(section['text'])

    article_lines = [line.encode("ascii", "ignore").decode() for line in article_lines]

    doc_data["article_lines"] = article_lines

    # add to output file
    doc_datafile.write(json.dumps(doc_data))
    doc_datafile.write("\n")

doc_datafile.close()



