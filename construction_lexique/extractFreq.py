# coding: utf-8

from multiprocessing import Pool
import pandas as pd
import numpy as np
import logging
import inspect
import spacy
import ujson
import glob
import sys
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('./'+inspect.getfile(inspect.currentframe()).split('/')[-1].split('.')[0]+'.log')
handler.setFormatter(logging.Formatter("%(asctime)s; %(levelname)s; %(message)s"))
logger.addHandler(handler)

nlp = spacy.load("fr_core_news_md")

# chemin vers les tweets (1 fichier = tweets d'un compte écologiste) des comptes écologistes 
filesEcolo = glob.glob(".tweetsEcol/*json")
# chemin vers les tweets (1 fichier = tweets d'un utilisateur) d'autres comptes Twitter divers
filesEchant = glob.glob(".tweetsByUser/*json")

allFiles = filesEcolo+filesEchant

def freqTok(file) : 

    tokensByUser = {}
    totalFreq = 0
    
    fileName = os.path.splitext(os.path.basename(file))[0]

    file = open(file)
    
    tokensByUser[fileName]={}
    
    for line in file : 
        
        tweetInfos = ujson.loads(line.rstrip())
        
        if "full_text" in tweetInfos :
            tweet = tweetInfos["full_text"].lower()
        else : 
            tweet = tweetInfos["tweet"].lower()
            
        tokens = [t for t in nlp(tweet)]
        
        for token in tokens : 
            token=str(token.lemma_)
            
            if not token.startswith("http") and not token.startswith("@") : 
                
                totalFreq+=1
                
                if token in tokensByUser[fileName] : 
                    tokensByUser[fileName][token]+=1
                else : 
                    tokensByUser[fileName][token]=1

    logger.info("Traitement du fichier %s terminé, nbTotal de tokens (sans @ et url) : %i"%(fileName,totalFreq))
    return tokensByUser

try :
    pool = Pool(processes=None)
    result = pool.map(freqTok, allFiles)
finally:
    pool.close()
    pool.join()

dic = {}
for r in result : 
    dic.update(r)

df = pd.DataFrame.from_dict(dic).fillna(0)

df.to_csv("freqByUser.csv", sep=";")


