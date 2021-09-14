'''
Parses longsummm dataset json file to make format input for the given model.
Reduces input size my using only the Abstract, Introduction and Conclusion.
Author: Tomas Goldsack
'''

import os, json, re
from nltk.tokenize import sent_tokenize

mode = "train" # train/test

is_alt_format = True # arXiv dataset format

# Standard format (json)
# { 
#   "article_lines": List[str],
#   "summary_lines": List[str]
# }

# Alt format (json)
# { 
#   "article": str,      # the body of the document, pagragraphs seperated by "/n" (this should include the abstract)
#   "summary": str,     # the  of the document, pagragraphs seperated by "/n" (would usually be "abstract" as per arXiv summaries)
#   "section_names": str # titles of sections, seperated by "/n"
# }

longsumm_file = open(f"./my_longsumm_{mode}_abs_full_science_parse.json")
longsumm_dict = json.load(longsumm_file)
longsumm_file.close()

output_fname = f"./my_longsumm_{mode}_abs_AIC.jsonl" if not is_alt_format else \
  f"./my_longsumm_{mode}_abs_AIC_alt.jsonl"

# AIC
AIC_datafile = open(output_fname, "w")

for paper_id, paper_dict in longsumm_dict.items():
  AIC_data = {}

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
    AIC_data["summary"] = " ".join(summary_sents)
  else:
    AIC_data["summary_lines"] = summary_sents

  # A section (abstract)
  if "abstractText" in input_dict.keys():

    abstract_add = (input_dict["abstractText"].replace("\n", " ") + "\n") if is_alt_format else \
      sent_tokenize(input_dict["abstractText"])

    article_lines = article_lines + abstract_add

    # Get IC sectionsstr
    if 'sections' in input_dict.keys() and len(input_dict['sections']) > 2:
      heading_sections = [s for s in input_dict['sections'] if "heading" in s.keys()]

      # I section (intro)
      intro_matches= [x for x in heading_sections if re.search("intro*", x["heading"].lower())]
      if intro_matches:
        intro = intro_matches[0]['text'] # task first match
        intro_sec_name = intro_matches[0]['heading']

        if len(intro_matches) > 1:
          print(f'MUTLIPLE INTRO MATCHES: {input_dict["id"]}')
      else: 
        intro = input_dict['sections'][0]['text']
        intro_sec_name = input_dict['sections'][0]['heading'] if 'heading' in input_dict['sections'][0].keys() else ""


      intro_add = (intro.replace("\n", " ") + "\n") if is_alt_format else sent_tokenize(intro) 

      article_lines = article_lines + intro_add
      section_names = section_names + intro_sec_name + "\n"

      
      # C section (conclusion)
      conc_matches= [x for x in heading_sections if (re.search("concl*", x["heading"].lower()) or \
        re.search("discuss*", x["heading"].lower()))]

      if conc_matches:
        conc = conc_matches[-1]['text'] # take last match
        conc_sec_name = conc_matches[-1]['heading']

        if len(conc_matches) > 1:
          print(f'MUTLIPLE CONC MATCHES: {input_dict["id"]}')
          print([x['heading'] for x in conc_matches])
      else: 
        conc = input_dict['sections'][-1]['text'] if input_dict['sections'][-1] != intro else ""
        conc_sec_name = input_dict['sections'][-1]['heading'] if 'heading' in input_dict['sections'][-1].keys() else ""
 

      conc_add = (conc.replace("\n", " ") + "\n") if is_alt_format else sent_tokenize(conc) 

      article_lines = article_lines + conc_add
      section_names = section_names + conc_sec_name + "\n"

      article_lines = article_lines.encode("ascii", "ignore").decode() if is_alt_format \
        else [line.encode("ascii", "ignore").decode() for line in article_lines]

      article_dict_key = "article" if is_alt_format else "article_lines"

      AIC_data[article_dict_key] = article_lines

      if is_alt_format:
        AIC_data["section_names"] = section_names

      # add to output file
      AIC_datafile.write(json.dumps(AIC_data))
      AIC_datafile.write("\n")

AIC_datafile.close()

