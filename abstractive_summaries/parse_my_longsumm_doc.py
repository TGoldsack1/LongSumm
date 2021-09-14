'''
Parses longsummm dataset json file to make format input for the given model.
Input size is kept at full document text
Author: Tomas Goldsack
'''

import os, json, re
from nltk.tokenize import sent_tokenize

mode = "test"
is_alt_format = True # arXiv dataset format

longsumm_file = open(f"./my_longsumm_{mode}_abs_full_science_parse.json")
longsumm_dict = json.load(longsumm_file)
longsumm_file.close()

# Desired input format (json)
# { 
#   "article_lines": List[str],
#   "summary_lines": List[str]
# }

doc_datafn = f"./my_longsumm_{mode}_abs_doc.jsonl" if not is_alt_format else \
  f"./my_longsumm_{mode}_abs_doc_alt.jsonl"

doc_datafile = open(doc_datafn, "w")

for paper_id, paper_dict in longsumm_dict.items():

  doc_data = {}
  article_lines = [] if not is_alt_format else ""
  section_names = ""

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

  if is_alt_format:
    doc_data["summary"] = " ".join(summary_sents)
  else:
    doc_data["summary_lines"] = summary_sents


  # A section (abstract)
  if "abstractText" in input_dict.keys():
    abstract_add = (input_dict["abstractText"].replace("\n", " ") + "\n") if is_alt_format else \
      sent_tokenize(input_dict["abstractText"])

    article_lines = article_lines + abstract_add

  # Get IC sectionsstr
  if 'sections' in input_dict.keys():

    for section in input_dict['sections']:
      section_add = (section['text'].replace("\n", " ") + "\n") if is_alt_format else \
        sent_tokenize(section['text'])

      section_name = section['heading'] if 'heading' in section.keys() else ""


      article_lines = article_lines + section_add
      section_names = section_names + section_name + "\n"

    article_lines = article_lines.encode("ascii", "ignore").decode() if is_alt_format \
      else [line.encode("ascii", "ignore").decode() for line in article_lines]

    article_dict_key = "article" if is_alt_format else "article_lines"
    
    doc_data[article_dict_key] = article_lines

    if is_alt_format:
      doc_data["section_names"] = section_names

    # add to output file
    doc_datafile.write(json.dumps(doc_data))
    doc_datafile.write("\n")

doc_datafile.close()



