'''
Evaluation Metrics on summarization and simplification.
1. BERTScore
2. SARI
​
ref: https://github.com/Tiiiger/bert_score/blob/master/example/Demo.ipynb
​
Author: Zhihao + Tomas
'''
​
import json
from bert_score import BERTScorer
​
# In situations when we want to call the `score` function repeatedly, it is better to cache the model in a `scorer` object. 
# rescale_with_baseline=True: Although this artifact does not affect the ranking ability of BERTScore, it affects the readability
scorer = BERTScorer(lang="en") 
​
def BERTScore_evaluation(cands, refs):
​
    P, R, F1 = scorer.score(cands, refs)
    # print(f"System level F1 score: {F1.mean():.4f}")
    
    return round(F1.mean().item(), 4)
​
​
## CHANGE THIS TO CHANGE FILE ##
input_json_file = "simplified_my_longsumm_test_AIC_news_pretrained_allenai_output.json"
# input_json_file = "simplified_my_longsumm_test_AIC_my_pretrained_allenai_output.json"
# input_json_file = "simplified_my_longsumm_test_SEC_news_pretrained_allenai_output.json"
# input_json_file = "simplified_my_longsumm_test_SEC_my_pretrained_allenai_output.json"
​
​
input_json_dir = "../predicted_summaries/"
input_json_dir = input_json_dir + input_json_file
​
input_json_file_contents = open(input_json_dir, "r")
input_json_lines = input_json_file_contents.readlines()
input_json_file_contents.close()
​
output_dict_ground_truth = []
output_dict_simplified = []
output_dict_summarized = []
​
for i, line in enumerate(input_json_lines):
    input_dict = json.loads(line) # { "ground_truth": str, "prediction": str, "simplified_prediction": str }
​
    output_dict_ground_truth.append(input_dict["ground_truth"])
    output_dict_simplified.append(input_dict["simplified_prediction"])
    output_dict_summarized.append(input_dict["prediction"])
​
assert len(output_dict_ground_truth) == len(output_dict_summarized) == len(output_dict_simplified)
​
​
# BERTScore
ground_summarize_bertscore_mean_f1 = BERTScore_evaluation(output_dict_ground_truth, output_dict_summarized)
ground_simple_bertscore_mean_f1 = BERTScore_evaluation(output_dict_ground_truth, output_dict_simplified)
summarize_simple_bertscore_mean_f1 = BERTScore_evaluation(output_dict_summarized, output_dict_simplified)
print('ground_summarize_bertscore_mean_f1:', ground_summarize_bertscore_mean_f1)
print('ground_simple_bertscore_mean_f1', ground_simple_bertscore_mean_f1)
print('summarize_simple_bertscore_mean_f1:', summarize_simple_bertscore_mean_f1)