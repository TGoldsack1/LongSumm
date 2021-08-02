
#!/bin/bash

# make sure to run:
# sudo docker run -p "0.0.0.0:8080:8080" allenai/scienceparse:2.0.3

INPUT_DIR="$(pwd)/inputs/*.pdf"


for file in ./inputs/*.pdf; do
  echo "-------------------------------------------"
  filename=$(basename -- "$file")
  filename="${filename%.*}"
  echo "${filename}"
  echo "${file}"
  output_path="./inputs/json/$filename.json"
  echo "$output_path"
  curl -v -H "Content-type: application/pdf" --data-binary @"$file" "http://localhost:8080/v1" -o "$output_path"
done