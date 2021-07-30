
#!/bin/bash

# make sure to run:
# docker run -p 127.0.0.1:8080:8080 allenai/scienceparse:2.0.3

INPUT_DIR="$(pwd)/inputs/*.pdf"


for file in ./inputs/*.pdf; do
  echo "-------------------------------------------"
  filename=$(basename -- "$file")
  filename="${filename%.*}"
  echo "${filename}"
  echo "${file}"
  output_path="./inputs/json/$filename.json"
  echo "$output_path"
  #curl -v -H "Content-type: application/pdf" --data-binary @"$file" "http://localhost:8080/v1/json/pdf" --http0.9 -o "$output_path"
  curl -v -H "Content-type: application/pdf" --data-binary @"$file" "http://localhost:8080/v1" --http0.9 -o "$output_path"
  #curl -v -H "Content-type: application/pdf" --data-binary @"$file" "http://scienceparse.allenai.org/v1" -o "$output_path"
done