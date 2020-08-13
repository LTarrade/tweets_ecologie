from gensim.models import Word2Vec
from multiprocessing import Pool
import unidecode
import logging
import inspect
import string
import ujson
import spacy
import sys
import re


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('./'+inspect.getfile(inspect.currentframe()).split('/')[-1].split('.')[0]+'.log')
handler.setFormatter(logging.Formatter("%(asctime)s; %(levelname)s; %(message)s"))
logger.addHandler(handler)

 
# chemin vers le fichier contenant les tweets (un tweet par ligne) que l'on veut prétraiter
file = open("./chemin/fichier.data")

nlp = spacy.load("fr_core_news_md")

logger.info("récupération des lignes")
lines = [l.rstrip() for i,l in enumerate(file)]
logger.info("récupération des lignes terminée - "+str(len(lines)))

punctuations = list(string.punctuation)
punctuations.append("\n")

def f(line) :
    logger.info("...")
    text = ujson.loads(line).replace("\n"," ").lower()
    textNLP = nlp(text)
    s = []
    for token in textNLP :
        if not str(token).startswith("@") and not str(token).startswith("http") and str(token) not in punctuations and not re.match("[^\w]+",str(token)) : 
            s.append(str(token))
    return s

try :
    pool = Pool(processes=None)
    result = pool.map(f, lines)
finally:
    pool.close()
    pool.join()

# chemin vers le fichier contenant les tweets (un tweet par ligne) que l'on veut prétraiter
out = open("./chemin/fichierPrétraité.data", "w")
for r in result :
     out.write(" ".join(r)+"\n")
out.close()

logger.info("Prétraitement des tweets terminé")

