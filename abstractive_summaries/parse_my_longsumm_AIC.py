'''
Parses longsummm dataset json file to make format input for the given model.
Reduces input size my using only the Abstract, Introduction and Conclusion.
Author: Tomas Goldsack
'''

import os, json, re
from nltk.tokenize import sent_tokenize

mode = "test"

longsumm_file = open(f"./my_longsumm_{mode}_abs_full.json")
longsumm_dict = json.load(longsumm_file)
longsumm_file.close()


## pointer-generator-pytorch-allennlp
# Desired input format (json)
# { 
#   "article_lines": List[str],
#   "summary_lines": List[str]
# }

# AIC
AIC_datafile = open(f"./my_longsumm_{mode}_abs_AIC.jsonl", "w")

for paper_id, paper_dict in longsumm_dict.items():
  AIC_data = {}

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

  AIC_data["summary_lines"] = summary_sents

  # A section (abstract)
  if "abstractText" in input_dict.keys():
    article_lines = article_lines + sent_tokenize(input_dict["abstractText"])

    # Get IC sectionsstr
    if 'sections' in input_dict.keys() and len(input_dict['sections']) > 2:
      heading_sections = [s for s in input_dict['sections'] if "heading" in s.keys()]

      # I section (intro)
      intro_matches= [x for x in heading_sections if re.search("intro*", x["heading"].lower())]
      if intro_matches:
        intro = intro_matches[0]['text'] # task first match
        if len(intro_matches) > 1:
          print(f'MUTLIPLE INTRO MATCHES: {input_dict["id"]}')
      else: 
        intro = input_dict['sections'][0]['text']

      article_lines = article_lines + sent_tokenize(intro)
      
      # C section (conclusion)
      conc_matches= [x for x in heading_sections if (re.search("concl*", x["heading"].lower()) or \
        re.search("discuss*", x["heading"].lower()))]

      if conc_matches:
        conc = conc_matches[-1]['text'] # take last match
        if len(conc_matches) > 1:
          print(f'MUTLIPLE CONC MATCHES: {input_dict["id"]}')
          print([x['heading'] for x in conc_matches])
      else: 
        conc = input_dict['sections'][-1]['text'] if input_dict['sections'][-1] != intro else "" 

      article_lines = article_lines + sent_tokenize(conc)

      article_lines = [line.encode("ascii", "ignore").decode() for line in article_lines]

      AIC_data["article_lines"] = article_lines

      # add to output file
      AIC_datafile.write(json.dumps(AIC_data))
      AIC_datafile.write("\n")

AIC_datafile.close()



