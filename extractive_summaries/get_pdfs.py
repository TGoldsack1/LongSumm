'''
Retrieves the extractive pdf files
Author: Tomas + Zhihao
'''


import requests
import urllib.request
from bs4 import BeautifulSoup
import io

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

with open("./talksumm_papers_titles_url.txt", "r") as input_txt:
  for line in input_txt.readlines()[:1]:
    title, url = line.replace("\n", "").split("\t") 

    print(url)

    response = requests.get(url, allow_redirects=True)

    if response.history:
      print("Request was redirected")
      for resp in response.history:
          print(resp.status_code, resp.url)
      print("Final destination:")
      print(response.status_code, response.url)

      red_response = requests.get(response.url + ".pdf")

      print(red_response.content)

      #soup = BeautifulSoup(response.content, "html.parser")

    else:
      print("Request was not redirected")

      soup = BeautifulSoup(response.content, "html.parser")

      pdf_links = get_pdf_links(soup)

    print("-"*10)


    if (len(pdf_links) > 0):
      count += 1
    #pdf_links = [link for link in pdf_links if '-supp' not in link]
    # print(pdf_links)

    # download_file(url, "./pdfs/" + title)

    print(count)
    # print("#"*50)


