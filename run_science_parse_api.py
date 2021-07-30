from pathlib import Path
import tempfile

from IPython.display import Image
import requests

from science_parse_api.test_helper import test_data_dir

try:
    # Tries to find the folder `test_data`
    test_data_directory = test_data_dir()
    test_pdf_paper = Path(test_data_directory, 
                      'example_for_test.pdf').resolve()
    image_file_name = str(Path(test_data_directory, 
                               'example_test_pdf_as_png.png'))
except FileNotFoundError:
    # If it cannot find that folder will get the pdf and 
    # image from Github. This will occur if you are using 
    # Google Colab
    pdf_url = ('https://github.com/UCREL/science_parse_py_api/'
               'raw/master/test_data/example_for_test.pdf')
    temp_test_pdf_paper = tempfile.NamedTemporaryFile('rb+')
    test_pdf_paper = Path(temp_test_pdf_paper.name)
    with test_pdf_paper.open('rb+') as test_fp:
        test_fp.write(requests.get(pdf_url).content)
        
    image_url = ('https://github.com/UCREL/science_parse_py_api'
                 '/raw/master/test_data/example_test_pdf_as_png.png')
    image_file = tempfile.NamedTemporaryFile('rb+', suffix='.png')
    with Path(image_file.name).open('rb+') as image_fp:
        image_fp.write(requests.get(image_url).content)
    image_file_name = image_file.name
    

Image(filename=image_file_name)

import pprint
from science_parse_api.api import parse_pdf

host = 'http://127.0.0.1'
port = '8080'
output_dict = parse_pdf(host, test_pdf_paper, port=port)

print(output_dict)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(output_dict)