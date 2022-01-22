import requests
from bs4 import BeautifulSoup

URL = "https://agogie.com/pages/reviews"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
print("Author List")
print()
auth = soup.findAll('span',class_="jdgm-rev__author-wrapper")
for x in auth:
    print(x.find('span').text)
    print()

print("Rating List")
print()
rat = soup.findAll('span',class_="jdgm-rev__rating")
#print(rat.find('data-score').attrs)
    

print("Product")
print()

print("Title")
print()

rev = soup.findAll('div',class_="jdgm-rev__content")
print("Reviews List")
print()
for x in rev:
    print(x.find('p').text)
    print()
    
