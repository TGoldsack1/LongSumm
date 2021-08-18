'''
Retrieves the extractive pdf files
Author: Tomas + Zhihao
'''


import requests
import urllib.request
from bs4 import BeautifulSoup
import io
from time import sleep
import numpy as np


def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)    
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()
 

def get_pdf_links(soup):
  # print(soup)

  list_of_pdf = set()
  p = soup.find_all('a')

  for link in p:
    href = (link.get('href'))
    if href and ".pdf" in href:
      pdf_link = href
      list_of_pdf.add(pdf_link)

  return list(list_of_pdf)


count = 0





import requests
import re

# example url of one of the articles
acl_url = "https://aclanthology.org/"


url = "https://aclanthology.org/D15-1250/"

# req = requests.get(url)
# text = req.text

# # regular expression to find a url that ends with '.pdf'
regex = re.compile('(http)(?!.*(http))(.*?)(\.pdf)')
# result = regex.search(text)
# start_i, end_i = result.span()
# pdf_url = text[start_i:end_i]
# print(pdf_url)

# download_file(pdf_url, "./pdf/" + "test")

print("------")
print("AUTO:")
with open("./talksumm_papers_titles_url.txt", "r") as input_txt:
  for line in input_txt.readlines():
    title, url = line.replace("\n", "").split("\t") 

    sleep(np.random.randint(1,15))

    print(url)
    response = requests.get(url, allow_redirects=True)

    # If the request is redirected (ACL paper)
    if (response.url and "anthology" in response.url) or "anthology" in url:
      print("Request was redirected or is acl")
      # for resp in response.history:
      #     print(resp.status_code, resp.url)
      
      # print("Final destination:")
      # print(response.status_code, response.url)
      # print(response.url)
      # red_response = requests.get(response.url)
      # print(red_response.text)
      # result = regex.search(red_response.text)
      # start_i, end_i = result.span()
      # pdf_url = text[start_i:end_i]
      # print(pdf_url)
      
      ind = -2 if url.endswith("/") else -1
      new_red_url = acl_url + url.split("/")[ind].upper()
      print(new_red_url)
      new_red_response = requests.get(new_red_url)
      result = regex.search(new_red_response.text)
      start_i, end_i = result.span()
      pdf_url = new_red_response.text[start_i:end_i]
      print(pdf_url)
      
      count += 1
      #soup = BeautifulSoup(response.content, "html.parser")
      
      download_url = pdf_url
        
    else:
      print("Request was not redirected")

      soup = BeautifulSoup(response.content, "html.parser")

      pdf_links = get_pdf_links(soup)

      if (len(pdf_links) > 0):
        count += 1
      
      pdf_links = [link for link in pdf_links if '-supp' not in link]
      
      if len(pdf_links) > 1:
        print("MORE THAN 1")
        print(pdf_links)
        download_url = pdf_links[-1]
      if len(pdf_links) == 0:
        print("NO LINKS")
        continue
      else:
        print(pdf_links[0])
        count += 1 
        download_url = pdf_links[0]

    try:  
      download_file(download_url, "./pdf/" + title)
    except:
      print("ERROR: DOWNLOAD FAILED")
    print("#####")

print(count)
