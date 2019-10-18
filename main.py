from urllib.request import Request, urlopen

link = Request('https://g1.globo.com/sp/campinas-regiao/noticia/2019/10/10/hospital-de-campinas-recebe-aula-gratuita-sobre-pratica-chinesa-que-reduz-estresse-e-dores-no-corpo.ghtml',
               headers={'User-Agent': 'Mozilla/5.0'})
pagina = urlopen(link).read().decode('utf-8', 'ignore')

from bs4 import BeautifulSoup

soup = BeautifulSoup(pagina, 'html.parser')
texto = ' '.join(map(lambda p: p.text, soup.find_all('p')))

'''
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
	# there may be more elements you don't want, such as "style", etc.
]

for t in texto:
	if t.parent.name not in blacklist:
		output += '{} '.format(t)

'''

from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

sentencas = sent_tokenize(texto)
palavras = word_tokenize(texto.lower())

from nltk.corpus import stopwords
from string import punctuation

stopwords = set(stopwords.words('portuguese') + list(punctuation))
palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stopwords]

from nltk.probability import FreqDist

frequencia = FreqDist(palavras_sem_stopwords)

from collections import defaultdict

sentencas_importantes = defaultdict(int)

for i, sentenca in enumerate(sentencas):
    for palavra in word_tokenize(sentenca.lower()):
        if palavra in frequencia:
            sentencas_importantes[i] += frequencia[palavra]

from heapq import nlargest

idx_sentencas_importantes = nlargest(4, sentencas_importantes, sentencas_importantes.get)

for i in sorted(idx_sentencas_importantes):
    print(sentencas[i])