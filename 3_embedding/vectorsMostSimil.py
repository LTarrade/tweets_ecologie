from gensim.models import Word2Vec
from adjustText import adjust_text
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import umap


years = ["2014", "2015", "2016", "2017", "2018"]

# Chargement des modèles pour chaque année : 
model14 = Word2Vec.load("/chemin/vers/model/2014")
model15 = Word2Vec.load("/chemin/vers/model/2015")
model16 = Word2Vec.load("/chemin/vers/model/2016")
model17 = Word2Vec.load("/chemin/vers/model/2017")
model18 = Word2Vec.load("/chemin/vers/model/2018")

models = {"2014":model14, "2015":model15, "2016":model16, "2017":model17, "2018":model18}

# Ici la liste des mots pour lesquelles on souhaite récupérer les 100 mots les plus similaires chaque année
targetsWords = ['biodiversité', 'biologique', 'écolo', 'écolos', 'écologie', 'écologique', 'écologiste', 'écologistes', 'écosystème', 'effondrement', 'nucléaire', 'ogm', 'pesticides', 'pollution', 'réchauffement', 'bio', 'charbon', 'co2', 'diesel', 'éoliennes', 'pac', 'pétrole', 'planète', 'recyclage', 'recycler', 'zad', 'climat', "ia", "agriculture","macron","trump","papers","cop21"]

for targetWord in targetsWords :
    # recupération des 100 mots les plus proches pour chaque année
    words = []
    for y in models :
        model = models[y]
        mostSimilar = [e for e in model.wv.most_similar(targetWord, topn=100)]

        mostSimilar_withVector = {}

        vectors_ecol = model.wv[targetWord].tolist()
        mostSimilar_withVector[targetWord]=vectors_ecol+[1]

        for e in mostSimilar :
            vectors = model.wv[e[0]].tolist()
            mostSimilar_withVector[e[0]]=vectors+[e[1]]

        df = pd.DataFrame.from_dict(mostSimilar_withVector, orient="index", columns=[i+1 for i in range(100)]+["simil_"+targetWord])

        words+=df.index.tolist()[1:]

    wordsTop100 = set(words)

    # recupération des vecteurs correspondant à chaque mot et pour chaque année
    words = wordsTop100

    vectorsByWordByYear = {}

    for i,word in enumerate(words) :
        vectorsByWordByYear[word]={}
        for y in models :
            try :
                vector = models[y].wv[word]
                vectorsByWordByYear[word][y]=vector
            except Exception as e :
                print(word+" - "+y+" - "+str(e))

    # création d'un nouveau vecteur pour chaque mot, correspondant à la moyenne sur l'ensemble des années pour chacune de ses dimensions
    dic = {}
    for w in vectorsByWordByYear :
        vectors = np.array([vectorsByWordByYear[w][v] for v in vectorsByWordByYear[w]])
        meanVectors = np.mean(vectors,0)
        dic[w]=meanVectors


    # récupération des vecteurs du mot cible pour chaque année
    for y in models :
        try :
            vector = models[y].wv[targetWord]
            dic[targetWord+"_"+y]=vector
        except Exception as e :
            print(targetWord+" - "+y+" - "+str(e))

    df_all = pd.DataFrame.from_dict(dic, columns=[i+1 for i in range(100)], orient="index")

    df_all.to_csv("./"+targetWord+"_skipgram.csv", sep=";")


# Fonction permettant de visualiser la position des vecteurs les uns par rapport aux autres dans un espace en 2D 
def visualize(word) :
            
    # récupération de l'ensemble des mots dans les tops100 (moy)
    df = pd.read_csv("./data_example/"+word+"_skipGram.csv", sep=";", index_col=0)

    # réduction des dimensions au nombre de 2
    reducer = umap.UMAP(random_state=0)
    embedding = reducer.fit_transform(df)
    
    # si l'on souhaite faire des clusters
    kmeans = KMeans(n_clusters=3, random_state=22).fit(df.iloc[:-5,:])
    
    # récupération des axes, des labels et des clusters
    x = embedding[:, 0]
    y = embedding[:, 1]
    labels = df.index.tolist()[:]
    clusters = kmeans.labels_.tolist()+[None,None,None,None,None]
    
    colors = ["#9B5DE5","#F15BB5",'#FEE440','#00BBF9','#00F5D4','#FF595E']

    plt.figure(figsize=[12,11])

    texts = []
    
    for xx,yy,label,cluster in zip(x, y, labels, clusters):
        if label.startswith(word+"_") :
            plt.scatter(xx,yy,color="black")
            plt.text(xx,yy,label,weight='bold') 
        else :
            plt.scatter(xx,yy,color="white")
            texts.append(plt.text(xx, yy, label, color=colors[cluster]))

    # si on veut "ajuster" le texte pour éviter les chevauchements (prend plusieurs minutes)
    #adjust_text(texts, force_points=0.2, force_text=0.2, expand_points=(1, 1), expand_text=(1, 1))

    plt.gca().set_aspect('equal', 'datalim')
    plt.title(word)

    plt.show()

visualize("papers")