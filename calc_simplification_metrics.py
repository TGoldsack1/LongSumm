'''
Evaluation Metrics on summarization and simplification.
1. BERTScore
2. other Metrics
​
ref: https://github.com/Tiiiger/bert_score/blob/master/example/Demo.ipynb
ref: https://github.com/feralvam/easse
​
Author: Zhihao + Tomas
'''
​
import json
​
​
# CHANGE THIS TO CHANGE FILE 
# input_json_file = "simplified_my_longsumm_test_AIC_news_pretrained_allenai_output.json"
# input_json_file = "simplified_my_longsumm_test_AIC_my_pretrained_allenai_output.json"
​
# input_json_file = "simplified_my_longsumm_test_SEC_news_pretrained_allenai_output.json"
# input_json_file = "simplified_my_longsumm_test_SEC_my_pretrained_allenai_output.json"
​
# input_json_file = "simplified_my_longsumm_test_AIC_news_pretrained_BART_output.jsonl"
input_json_file = "simplified_my_longsumm_test_SEC_news_pretrained_BART_output.jsonl"
​
​
input_json_dir = "./predicted_summaries/"
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
# ---------------------------- BERTScore
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
ground_summarize_bertscore_mean_f1 = BERTScore_evaluation(output_dict_ground_truth, output_dict_summarized)
ground_simple_bertscore_mean_f1 = BERTScore_evaluation(output_dict_ground_truth, output_dict_simplified)
summarize_simple_bertscore_mean_f1 = BERTScore_evaluation(output_dict_summarized, output_dict_simplified)
print('ground_summarize_bertscore_mean_f1:', ground_summarize_bertscore_mean_f1)
print('ground_simple_bertscore_mean_f1', ground_simple_bertscore_mean_f1)
print('summarize_simple_bertscore_mean_f1:', summarize_simple_bertscore_mean_f1)
​
# --------------------------- FKGL
from easse.fkgl import corpus_fkgl
​
ground_fkgl = round(corpus_fkgl(output_dict_ground_truth), 4)
summarize_fkgl = round(corpus_fkgl(output_dict_summarized), 4)
simple_fkgl = round(corpus_fkgl(output_dict_simplified), 4)
print('ground_fkgl:', ground_fkgl)
print('summarize_fkgl', summarize_fkgl)
print('simple_fkgl:', simple_fkgl)
​
# ---------------------------  corpus_quality_estimation
from easse.quality_estimation import corpus_quality_estimation
​
def prinf_socre(ground_summarize_quality_estimation_scores):
	for key,value in ground_summarize_quality_estimation_scores.items():
		print(key,':',round(value, 4))
​
​
ground_summarize_quality_estimation_scores = corpus_quality_estimation(output_dict_ground_truth, output_dict_summarized)
ground_simple_quality_estimation_scores = corpus_quality_estimation(output_dict_ground_truth, output_dict_simplified)
summarize_simple_quality_estimation_scores = corpus_quality_estimation(output_dict_summarized, output_dict_simplified)
​
print('-------------------ground_summarize_quality_estimation_scores:')
prinf_socre(ground_summarize_quality_estimation_scores)
​
print('-------------------ground_simple_quality_estimation_scores:')
prinf_socre(ground_simple_quality_estimation_scores)
​
print('-------------------summarize_simple_quality_estimation_scores:')
prinf_socre(summarize_simple_quality_estimation_scores)