from bs4 import BeautifulSoup, Doctype
import requests
import lxml

import pandas as pd

# VARIABLE SETUP
full_book = {
  'title': [],
  'content': [],
}
has_next = True
next_link = f'https://mourningcrow.wordpress.com/2021/06/25/chapter-1-devil-venerable-also-wants-to-know/'

# HTML SKELETON SETUP
doc = BeautifulSoup()
doc.append(Doctype('html'))
html = doc.new_tag('html', lang='en-US')
doc.append(html)
head = doc.new_tag('head')
html.append(head)
meta = doc.new_tag('meta', charset='utf-8')
head.append(meta)
title = doc.new_tag('title')
title.string = 'Devil Venerable Also Wants to Know'
head.append(title)
body = doc.new_tag('body')
html.append(body)

while (has_next):
  # HTTP GET requests
  page = requests.get(next_link)

  # Checking if we successfully fetched the URL
  if page.status_code == requests.codes.ok:
    bs = BeautifulSoup(page.text, 'lxml')
    # print(bs)
  else:
    print('status_code failed')
    quit()

  article = bs.find('article')
  # print(page_article[0])

  header = article.find('header')
  title = header.find('h1').string

  doc_header = doc.new_tag('h1')
  doc_header.string = title
  body.append(header)
  print(f'TITLE: ', title)

  content = bs.find("div", class_="entry-content")
  paragraphs = content.find_all('p')

  chapter_string = ""
  for p in paragraphs:
    body.append(p)
    if "class" in p.attrs.keys():
      continue
    chapter_string = chapter_string + p.text + '\n'

  full_book['title'].append(title)
  full_book['content'].append(chapter_string)

  navigation = content.find('h2')
  nav_links = navigation.find_all('a')
  has_next = False
  for link in nav_links:
    if link.text == "Next" or link.text == "next":
      next_link = link['href']
      has_next = True
  # has_next = False

f = open("output.html", "a")
f.write(doc.prettify())
f.write("\n")
f.close()

# CONVERT TO EPUB 
# pandoc -t epub3 -o output.epub output.html
