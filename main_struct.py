from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.probability import FreqDist
from collections import defaultdict
from heapq import nlargest
import re

def getPage(url):

	link = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	page = urlopen(link).read().decode('utf-8', 'ignore')
	
	return page

def getTextPage(page):

	soup = BeautifulSoup(page, 'html.parser')
	text = ' '.join(map(lambda p: p.text, soup.find_all('p')))

	'''
	soup = BeautifulSoup(page, 'lxml')
	text = soup.find_all('p')

	article_text = ""

	for p in text:
	    article_text += p.text

	return article_text
	'''

	return text

def getTextPageList(page):
	
	soup = BeautifulSoup(page, 'html.parser')
	text = soup.find_all(text=True)

	return text

def removeTags(text):

	output = ''
	blacklist = [
		'[document]',
		'noscript',
		'header',
		'html',
		'meta',
		'head', 
		'input',
		'script',
		'ul',
		'li',
		'style',
		'label', 
		'h4', 
		'ol', 
		'[document]', 
		'a', 
		'h1', 
		'noscript', 
		'span', 
		'header', 
		'ul', 
		'html', 
		'section', 
		'article', 
		'em', 
		'meta', 
		'title', 
		'body', 
		'aside', 
		'footer', 
		'div', 
		'form', 
		'nav', 
		'p', 
		'head', 
		'link', 
		'strong', 
		'h6', 
		'br', 
		'li', 
		'h3', 
		'h5', 
		'input', 
		'blockquote', 
		'main', 
		'script', 
		'figure',
		# there may be more elements you don't want, such as "style", etc.
	]

	for t in text:
		if t.parent.name not in blacklist:
			output += '{} '.format(t)

	return output

def processText(text):

	sentencas = sent_tokenize(text)
	palavras = word_tokenize(text.lower())

	stopwords_arr = set(stopwords.words('portuguese') + list(punctuation))
	palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stopwords_arr]

	frequencia = FreqDist(palavras_sem_stopwords)

	sentencas_importantes = defaultdict(int)

	for i, sentenca in enumerate(sentencas):
	    for palavra in word_tokenize(sentenca.lower()):
	        if palavra in frequencia:
	            sentencas_importantes[i] += frequencia[palavra]

	idx_sentencas_importantes = nlargest(4, sentencas_importantes, sentencas_importantes.get)

	final = []
	for i in sorted(idx_sentencas_importantes):
         final.append(re.sub(r"[0-9]{2}[\/,:][0-9]{2}[\/,:][0-9]{2,4}","",sentencas[i]))

	return final

text = processText(getTextPage(getPage('https://g1.globo.com/sp/campinas-regiao/noticia/2019/10/10/hospital-de-campinas-recebe-aula-gratuita-sobre-pratica-chinesa-que-reduz-estresse-e-dores-no-corpo.ghtml')))
#text = processText(removeTags(getTextPageList(getPage('https://g1.globo.com/sp/campinas-regiao/noticia/2019/10/10/hospital-de-campinas-recebe-aula-gratuita-sobre-pratica-chinesa-que-reduz-estresse-e-dores-no-corpo.ghtml'))))
for line in text:
	print(line)