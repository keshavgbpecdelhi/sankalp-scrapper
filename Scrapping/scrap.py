import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re
import csv
import re

#csv_file = open('Web-D-questions-answers.csv', 'a')
#csv_writer = csv.writer(csv_file)
#csv_writer.writerow(['ALL IN ONE'])

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
url="https://www.sanfoundry.com/html-questions-answers-web-browsers/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html, 'html.parser')
soup = BeautifulSoup(str(soup).replace('<p>','</p><p>'),'html.parser')
#soup = BeautifulSoup(str(soup).replace("advertisment",""),'html.parser')
a=soup.find("p")
a.find(re.compile("<p>[\d]+.+"))
questions= soup.find('div', class_='inside-article')

print(questions)
#for i in a:
    #print(i.text)
    #csv_writer.writerow([i.text])

#csv_file.close()