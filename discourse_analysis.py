'''
# Use rouge and BERTscore at sentence-level to compare each sentence
# in each section with the each sentence in the summary + compute
# average.
'''

import os, json, re
import pandas as pd
import numpy as np
from bert_score import BERTScorer
from rouge_score import rouge_scorer
from nltk.tokenize import sent_tokenize

df = pd.DataFrame()

longsumm_fp = "./abstractive_summaries/all_longsumm_abs_full_science_parse.json"
longsumm_file = open(longsumm_fp, "r")
longsumm_json = json.loads(longsumm_file.read())

for id_str, content in longsumm_json.items():
    if "X" in content.keys() and "Y" in content.keys() and "id" in content["X"].keys() \
        and content["X"]["id"] != "empty" and "sections" in content["X"].keys():
        
        summary_text = " ".join(content["Y"]["summary"])
        
        if "sections" not in content['X'].keys():
            print(content['X'])
            
        title = content["X"]["title"] if "title" in content["X"].keys() else "N/A"
        year = content["X"]["year"] if "year" in content["X"].keys() else "N/A"
        abstract = content["X"]["abstractText"] if "abstractText" in content["X"].keys() else "N/A"
        
        full_text = " ".join([sec["text"] for sec in content["X"]["sections"]])
        sections = content["X"]["sections"] if "sections" in content['X'].keys() else "N/A"
        
        df = df.append([[id_str, title, summary_text, sections, abstract, full_text, year]])
        
df.columns =['ls_id', 'title', 'summary', 'sections', 'abstract', 'full_text', "year"]

print(len(df))


metrics = ['rouge1', 'rouge2', 'rougeL']
rs = rouge_scorer.RougeScorer(metrics, use_stemmer=True)
bs = BERTScorer(lang="en") 

example_1 = "This is an example sentence."
example_2 = "An example sentence, this is."

print(rs.score(example_1.strip(), example_2.strip()))
print(bs.score([example_1.strip()], [example_2.strip()])) # precision, recall, f-score

paper_sec_scores = []

i = 1
for index, row in df.iterrows():
    sections = row['sections']
    summary = row['summary']
    summary_sents = sent_tokenize(summary)
    section_scores = {}
    
    print(f'{i}/{len(list(df["summary"]))}')

    for section in sections:
        heading = section["heading"] if "heading" in section.keys() else "[N/A]"
        text = section["text"] if "text" in section.keys() else ""
        
        text_sents = sent_tokenize(text)
        
        BERTscores = []
        rouge_scores = []
        
        for text_sent in text_sents:            
            for summary_sent in summary_sents:
                rs_results = rs.score(text_sent.strip(), summary_sent.strip())
                bs_results = bs.score([text_sent.strip()], [summary_sent.strip()])[2].item()

                rouge_scores.append({k: np.average([v.fmeasure, v.recall]) for k,v in rs_results.items()})
                BERTscores.append(bs_results)
        
        section_scores[heading] = {
            'BERTScore': np.average(BERTscores),
            'rouge1': np.average([item['rouge1'] for item in rouge_scores]),
            'rouge2': np.average([item['rouge2'] for item in rouge_scores]),
            'rougeL': np.average([item['rougeL'] for item in rouge_scores])
        }
    
    paper_sec_scores.append(section_scores)

    with open("./sec_scores_record.txt", "w") as output_file:
      output_file.write(json.dumps(paper_sec_scores))
        
    i += 1


df['section_scores'] = paper_sec_scores
df.to_csv("section_analysis_ds.csv", sep="\t")
