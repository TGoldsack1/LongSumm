
#!/bin/bash

# make sure to run:
# sudo docker run -p "0.0.0.0:8080:8080" allenai/scienceparse:2.0.3

#INPUT_DIR="$(pwd)/abstractive_summaries"
INPUT_DIR="$(pwd)/extractive_summaries"

pdf_paths="$INPUT_DIR/pdf/*.pdf" 

for file in $pdf_paths; do
  echo "-------------------------------------------"
  filename=$(basename -- "$file")
  filename="${filename%.*}"
  echo "${filename}"
  echo "${file}"
  output_path="$INPUT_DIR/json/$filename.json"
  echo "$output_path"
  curl -v -H "Content-type: application/pdf" --data-binary @"$file" "http://localhost:8080/v1" -o "$output_path"
done