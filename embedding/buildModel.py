from gensim.models import Word2Vec
import logging
import inspect

# ici indiquer si il s'agit du premier modèle que l'on entraîne ou non (si non, le modèle sera initialisé avec celui de yearPrec)
firstModel = False

# yearPrec correspond à l'année du modèle qui sera utilisé pour l'initialisation de l'année year
yearPrec = "2013"
year = "2014"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('./log/'+inspect.getfile(inspect.currentframe()).split('/')[-1].split('.')[0]+'_'+year+'.log')
handler.setFormatter(logging.Formatter("%(asctime)s; %(levelname)s; %(message)s"))
logger.addHandler(handler)

logger.info("construction du modèle pour l'année "+year)

# chemin vers les tweets prétraités de l'année sur laquelle on souhaite former un modèle (un fichier = les tweets d'une année, un tweet par ligne)
file = open("./chemin/tweets_preprocessed_"+year+".data")

result = [l.rstrip().split(" ") for l in file]

logger.info("récupération des lignes terminée - "+str(len(result)))

logger.info("construction du modèle")

if firstModel :
	model = Word2Vec(result, workers=16, sg=1)
else : 
	# chargement du modèle précédent
	model = Word2Vec.load("./chemin/model_"+yearPrec)
	# mise à jour du vocabulaire du modèle précédent avec celui que l'on veut former
	model.build_vocab(result, update=True)
	# mise à jour des poids neuronaux du modèle précédent
	model.train(result, total_examples=model.corpus_count, epochs=model.iter)

logger.info("construction du modèle terminée")

model.save('./chemin/model_'+year)
