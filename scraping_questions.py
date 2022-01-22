#!/c/Users/sankalp/anaconda3/python

import urllib.request,urllib.error,urllib.parse
from bs4 import BeautifulSoup,NavigableString,Tag
import ssl
import re
import csv
import io


def parser(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html,'html.parser')
    return soup


def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s


def question_getter(soup):
    questions = list()
    for i in soup.find_all('b')[1:]:
        try:
            questions.append(re.search(r'<b>\w+.\)(.*)<\/b>',str(i))[1])
        except:
            continue
    return questions


def options_getter(soup):
    options = list()
    for br in soup.find_all('br'):
        next_tag = br.next_sibling
        if not (next_tag and isinstance(next_tag,NavigableString)):
            continue
        next_tag2 = next_tag.next_sibling
        if next_tag2 and isinstance(next_tag2,Tag) and next_tag2.name == 'br':
            text = str(next_tag).strip()
            options.append(text)
    return options


def modify_options(options):
    dic = {}
    option_a = []
    option_b = []
    option_c = []
    option_d = []
    count = 0
    for i in options:
        if i.startswith('a'):
            count+=1
        dic[count] = dic.get(count,[]) + [i]
    for values in dic.values():
        for i in range(1,5):
            if i == 1:
                try:
                    option_a.append(values[i-1])
                except:
                    option_a.append("blank")
            if i == 2:
                try:
                    option_b.append(values[i-1])
                except:
                    option_b.append("blank")
            if i == 3:
                try:
                    option_c.append(values[i-1])
                except:
                    option_c.append("blank")
            if i == 4:
                try:
                    option_d.append(values[i-1])
                except:
                    option_d.append("blank")
    return option_a,option_b,option_c,option_d
            


def answers_getter(soup):
    answers = list()
    for i in range(1,11):
        try:
            a = str(soup.find(id = "a{}".format(i)))
            ans = re.search(r'<div id="a\w+"><br\/><p><strong>ANSWER: [a-z].\)(.*)<\/strong>',a)[1]
            ans = html_decode(ans)
            answers.append(ans)
        except:
            continue
    return answers


def main():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = "https://www.careerride.com/post/web-programming-placement-papers-model-questions-733.aspx"
    soup = parser(url)

    all_urls = list()

    tags = soup('a')
    for tag in tags:
        links = str(tag.get('href',None))
        if links.startswith('/view'):
            all_urls.append("".join(["https://www.careerride.com",links]))

    f = io.open('questions.csv','a',encoding="utf-8")        
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['QUESTION','OPTION 1','OPTION 2','OPTION 3','OPTION 4','ANSWERS'])
    
    for url in all_urls:
        soup = parser(url)
        questions = question_getter(soup)
        options = options_getter(soup)
        option_a,option_b,option_c,option_d = modify_options(options)
        answers = answers_getter(soup)
        ls = [questions,option_a,option_b,option_c,option_d, answers]
        for i in list(zip(*ls)):
            writer.writerow(list(i))
    f.close()
    
if __name__ == '__main__':
    main()