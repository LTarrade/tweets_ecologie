# coding: utf-8
from multiprocessing import Pool
import pandas as pd
import subprocess
import unidecode
import logging
import inspect
import ujson
import glob
import re
import os

# log
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('./'+inspect.getfile(inspect.currentframe()).split('/')[-1].split('.')[0]+'.log')
handler.setFormatter(logging.Formatter("%(asctime)s; %(levelname)s; %(message)s"))
logger.addHandler(handler)


# Récupération des fichiers à traiter (indiquer le chemin vers le corpus des tweets au format json)
files = glob.glob("corpus/*data")

logger.info("%i fichiers à traiter"%len(files))


# Récupération de la liste des mots ou groupes de mots du champ lexical de l'écologie
sortedWords = []
words = {}

wordsFile = open("./listeMots.txt", encoding="utf-8")
for line in wordsFile : 
    word = unidecode.unidecode(line.rstrip()).lower()
    words[word]=len(word)
words = sorted(words.items(), key=lambda x: x[1], reverse=True)
for w in words : 
    sortedWords.append(w[0])
wordsRe = re.compile("|".join(sortedWords))


# Récupération des fréquences de chacun des mots ou groupes de mots pour chaque jour 
# pour chaque correspondance on récupérera un dictionnaire du type {"match":match, "date":date, "tweetId":tweetId, "userId":userId}
def extractFreq(file) :
    
    matches = []
        
    fileName = os.path.splitext(os.path.basename(file))[0]
    day = re.match("(\d{4}-\d{2}-\d{2})T\d{2}",fileName).group(1)

    logger.info("Traitement du fichier "+str(fileName))
            
    file = open(file)
    
    for line in file : 
                            
        infosTweet = ujson.loads(line.rstrip())
        
        tweet = infosTweet["tweet"]
        tweet = unidecode.unidecode(tweet).lower()
        
        userId = str(infosTweet["user"]["id"])
        
        tweetId = str(infosTweet["id"])
        
        match = re.findall(wordsRe,tweet)
        
        if len(match)!=0 : 
            for e in match :
                if not re.match(r"#?(la|ta|ma|sa|une|leur|votre|notre|les|des|mes|tes|ces|nos|vos|leurs|ses) ?bios?", e) and not re.match(r"#?(meme|autre)s? ?planetes?", e) : 
                     matches.append({"match":str(e), "date":str(day), "tweetId":tweetId, "userId":userId})
        
    return(matches)


try :
    pool = Pool(processes=None)
    results = pool.map(extractFreq, files)
finally:
    pool.close()
    pool.join()

# Concaténation des résultats dans une même liste
matches = []
for r in results : 
    matches+=r


# Récupération du nombre de tweets total par jour
logger.info("Récupération du nombre de tweets total par jour")
tweetsByDay = {}

for file in files : 
    
    fileName = os.path.splitext(os.path.basename(file))[0]
    day = re.match("(\d{4}-\d{2}-\d{2})T\d{2}",fileName).group(1)
    
    nblines = subprocess.check_output(["wc","-l",file])
    nblines = nblines.decode("utf-8")

    nbTweets = int(re.match("\s*(\d+) "+file,nblines).group(1))
    
    if day not in tweetsByDay : 
        tweetsByDay[day]=0 

    tweetsByDay[day]+=nbTweets

# ajout des résultats
for match in matches : 
    day = match["date"]
    match["nbTweetsTot_Date"]=tweetsByDay[day]


# Enregistrement des correspondances trouvées dans un fichier "matches.csv"
logger.info('Enregistrement des correspondances trouvées dans un fichier "matches.csv"')
df = pd.DataFrame(matches)
df.to_csv("matches.csv", sep=";")

