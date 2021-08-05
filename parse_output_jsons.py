'''
Parses the json output files of models into the require format 
for the evaluation script.
Author: Tomas + Zhihao
'''

import os, json

annotations_dir = "./annotations" # where we store the output to be evaluated

input_json_dir = "./predicted_summaries/"

## CHANGE THIS TO CHANGE FILE ##

#input_json_file = "simplified_my_longsumm_test_AIC_news_pretrained_allenai_output.json"
#input_json_file = "simplified_my_longsumm_test_AIC_my_pretrained_allenai_output.json"
input_json_file = "simplified_my_longsumm_test_SEC_my_pretrained_allenai_output.json"
input_json_file = "simplified_my_longsumm_test_SEC_news_pretrained_allenai_output.json"


input_json_filepath = input_json_dir + input_json_file

# Format for evaluation script
# {
# "paper_id_1":"summary of paper 1",
# "paper_id_2":"summary of the paper 2"
# }

input_json_file_contents = open(input_json_filepath, "r")
input_json_lines = input_json_file_contents.readlines()
input_json_file_contents.close()


if "allenai" in input_json_file:
  
  output_dict_ground_truth = {}
  output_dict_simple_pred = {}
  output_dict_pred = {}
  
  for i, line in enumerate(input_json_lines):
    
    input_dict = json.loads(line) # { "ground_truth": str, "prediction": str, "simplified_prediction": str }
    
    output_dict_ground_truth[i] = input_dict["ground_truth"]
    output_dict_simple_pred[i] = input_dict["simplified_prediction"]
    output_dict_pred[i] = input_dict["prediction"]

  # output ground truth 
  with open(annotations_dir + "/my_test_ground_truth.json", "w") as gt_out:
    gt_out.write(json.dumps(output_dict_ground_truth, indent=4, sort_keys=False))

  # output predicted summary 
  with open(annotations_dir + "/" + input_json_file.replace("simplified_", ""), "w") as gt_out:
    gt_out.write(json.dumps(output_dict_pred, indent=4, sort_keys=False))

  # output predicted simplified summary
  with open(annotations_dir + "/" + input_json_file, "w") as gt_out:
    gt_out.write(json.dumps(output_dict_simple_pred, indent=4, sort_keys=False))


# test_annotations_testsplit.json