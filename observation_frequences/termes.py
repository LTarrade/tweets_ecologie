# coding: utf-8
from scipy.signal import argrelmax, argrelmin
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime


# Observation du taux de croissance des termes année par année
df = pd.read_csv("./matches_anonymise.csv", index_col=0, sep=";")

matches = [m for m in set(df.match.tolist())]


# on récupère dans matchUniq2 pour chaque mot ses variantes possibles 
sort = []
hashtags = []
for e in sorted(matches) : 
    if e.startswith("#") : 
        hashtags.append(e)
    else : 
        sort.append(e)
sort+=hashtags

matchesUniq = {}
notAdd = []
for i,m in enumerate(sort) : 
    if m not in notAdd : 
        if m.startswith("cop") or m.startswith("#cop"):
            if "cop" not in matchesUniq :
                matchesUniq["cop"]=[]
            matchesUniq["cop"].append(m)
        else : 
            matchesUniq[m]=[]
            matchesUniq[m].append(m)
            mEmpty = m.replace("#","")
            mEmpty = mEmpty.replace(" ","")
            mEmpty = mEmpty.replace("s","")
            for j,m2 in enumerate(sort) : 
                if i!=j :
                    m2Empty = m2.replace("#","")
                    m2Empty = m2Empty.replace(" ","")
                    m2Empty = m2Empty.replace("s","")
                    if mEmpty == m2Empty :
                        notAdd.append(m2)
                        matchesUniq[m].append(m2)
                        
matchUniq2 = {}
notAdd2 = []
for m in matchesUniq : 
    if m=="ecocitoyen" or m=="ecologique" or m=="ecolabel" or m=="environnement" or m=="polluant" : 
        matchUniq2[m]=matchesUniq[m]
        for m2 in matchesUniq : 
            if m2.startswith(m) : 
                matchUniq2[m]+=matchesUniq[m2]
                notAdd2.append(m2)
    else : 
        if m not in notAdd2 : 
            matchUniq2[m]=matchesUniq[m]


# Récupération du nombre de tweets total de chaque année
years = ["2013", "2014", "2015", "2016", "2017", "2018"]
days = sorted(set([d for d in df.date.tolist() if d[:4] in years]))

totalTweetsByYear = {}
for d in days : 
    sousDf = df[df.date==d]
    if d[:4] not in totalTweetsByYear :
        totalTweetsByYear[d[:4]]=0
    totalTweetsByYear[d[:4]]+=sousDf.nbTweetsTot_Date.tolist()[0]


# récupération pour chaque terme du lexique du pourcentage de tweet le contenant 
percentByTerm = {}
for y in years : 
    sousDf = df[df.date.str.startswith(y)]
    for m in matchUniq2 :
        sousDfMatch = sousDf[sousDf.match.isin(matchUniq2[m])]
        rate = (len(set(sousDfMatch.tweetId.tolist()))/totalTweetsByYear[y])*100
        if y not in percentByTerm : 
            percentByTerm[y] = {}
        percentByTerm[y][m]=rate


# on récupère les termes qui sont présents sur l'ensemble des années
termsAllYears = []
for term in percentByTerm["2013"] : 
    if percentByTerm["2013"][term]!=0 and percentByTerm["2014"][term]!=0 and percentByTerm["2015"][term]!=0 and percentByTerm["2016"][term]!=0 and percentByTerm["2017"][term]!=0 and percentByTerm["2018"][term]!=0 :
        termsAllYears.append(term)


# on calcule le taux de croissance entre chaque année 
croissanceByYearByTerm = {}
for term in termsAllYears : 
    croissanceByYearByTerm[term] = {}
    croissanceByYearByTerm[term]["2013-2014"] = ((percentByTerm["2014"][term]-percentByTerm["2013"][term])/percentByTerm["2013"][term])*100
    croissanceByYearByTerm[term]["2014-2015"] = ((percentByTerm["2015"][term]-percentByTerm["2014"][term])/percentByTerm["2014"][term])*100
    croissanceByYearByTerm[term]["2015-2016"] = ((percentByTerm["2016"][term]-percentByTerm["2015"][term])/percentByTerm["2015"][term])*100
    croissanceByYearByTerm[term]["2016-2017"] = ((percentByTerm["2017"][term]-percentByTerm["2016"][term])/percentByTerm["2016"][term])*100
    croissanceByYearByTerm[term]["2017-2018"] = ((percentByTerm["2018"][term]-percentByTerm["2017"][term])/percentByTerm["2017"][term])*100


# termes qui ont connu un taux de croissance systématiquement positif sur l'ensemble de la période couverte
terms = []
for term in croissanceByYearByTerm : 
    croissance = True
    for y in croissanceByYearByTerm[term] : 
        if croissanceByYearByTerm[term][y]<=0 :
            croissance = False
    if croissance : 
        terms.append(term)
print("\n"+str(len(terms))+"/"+str(len(croissanceByYearByTerm))+" termes ont connu une croissance continue de 2013 à 2018 : "+str(terms))

# termes qui ont connu un taux de croissance positif depuis 2015
terms = []
notLook = ["2013-2014", "2014-2015"]
for term in croissanceByYearByTerm : 
    croissance = True
    for y in croissanceByYearByTerm[term] : 
        if y not in notLook :
            if croissanceByYearByTerm[term][y]<=0 :
                croissance = False
    if croissance : 
        terms.append(term)
print("\n"+str(len(terms))+"/"+str(len(croissanceByYearByTerm))+" termes ont connu une croissance continue depuis 2015 : "+str(terms))

# termes qui ont connu un taux de croissance positif depuis 2016
terms = []
notLook = ["2013-2014", "2014-2015", "2015-2016"]
for term in croissanceByYearByTerm : 
    croissance = True
    for y in croissanceByYearByTerm[term] : 
        if y not in notLook :
            if croissanceByYearByTerm[term][y]<=0 :
                croissance = False
    if croissance : 
        terms.append(term)
print("\n"+str(len(terms))+"/"+str(len(croissanceByYearByTerm))+" termes ont connu une croissance continue depuis 2016 : "+str(terms))

# termes dont le taux de croissance est supérieur en 2017 et 2018 par rapport à 2014
terms = [] 
for term in croissanceByYearByTerm : 
    if croissanceByYearByTerm[term]["2016-2017"]>croissanceByYearByTerm[term]["2013-2014"] and croissanceByYearByTerm[term]["2017-2018"]>croissanceByYearByTerm[term]["2013-2014"] :
        terms.append(term)
print("\n"+str(len(terms))+"/"+str(len(croissanceByYearByTerm))+" termes ont un taux de croissance plus élevé en 2017 et 2018 que celui de 2014 : "+str(terms))


# Fonction permettant d'obtenir un camembert donnant la répartition des termes pour une période donnée
def repartition(begin, end) : 
    
    plt.figure(figsize=[8,8])
    
    date = datetime.datetime.strptime(begin, "%Y-%m-%d")    
    endDate = datetime.datetime.strptime(end, "%Y-%m-%d")

    datesTotreat = []
    while date<=endDate :
        datesTotreat.append(date)
        date += datetime.timedelta(days=1)
        
    datesTotreat_str = [datetime.datetime.strftime(d, "%Y-%m-%d") for d in datesTotreat]
        
    sousDf = df[df.date.isin(datesTotreat_str)]
    matches = sousDf.groupby(sousDf.match)
    
    total = sum([len(e[1]) for e in matches])

    nbMatches = {}
    for e in matches :
        match = e[0]
        freq = len(e[1])
        rate = freq/total
        nbMatches[match]=rate*100
        
    nbMatches = sorted(nbMatches.items(), key=lambda t: t[1], reverse=True)    
    
    labels = [label for label,rate in nbMatches]
    rates = [rate for label,rate in nbMatches]
    
    for j,r in enumerate(rates) : 
        if r<2 : 
            break
    
    k = 0
    for r in rates[j:] :
        k+=r
    
    rates = rates[:j]
    rates.append(k)
    labels = labels[:j]
    labels.append("inf 2%")

    explode = []
    lmax = max(rates)
    for l in rates : 
        if l==lmax : 
            explode.append(0.06)
        else : 
            explode.append(0)

    colors = ["#fcc419","#94d82d","#22b8cf","#ff6b6b","#20c997","#5c7cfa","#ff922b","#51cf66","#f06595"]
    
    plt.title("Répartition des termes du lexique pour la période du "+str(begin)+" au "+str(end))
    plt.pie(rates, labels=labels, autopct='%1.1f%%', startangle=-90, explode=explode, colors=colors, rotatelabels=1)


repartition("2013-01-01", "2018-12-31")
repartition("2014-03-10", "2014-03-16")


# Calcul de la répartition des tweest lors des pics hauts et bas sur les différents jours de la semaine

# Récupération du pourcentage de tweets lié à l'écologie pour chaque jour
byDay = []

i = 0
for d in days : 
    
    sousDf = df[df.date==d]
    
    tweetsWithMatch = len(set(sousDf.tweetId.tolist()))
    totalTweets = sousDf.nbTweetsTot_Date.tolist()[0]
    i+=totalTweets
    
    rate = (tweetsWithMatch/totalTweets)*100
    
    byDay.append((d,rate))


dates = [d for d,rate in byDay]
rates = np.array([rate for d,rate in byDay])


# Récupération des indices puis des dates correspondant aux pics hauts et bas 
maxPics = argrelmax(rates)[0]
minPics = argrelmin(rates)[0]
datesMaxPics = [dates[i] for i in maxPics]
datesMinPics = [dates[i] for i in minPics]


# Pour chaque date à laquelle un pic bas a été repéré, on récupère le jour de la semaine auquel il correspond, de 0 (lundi) à 6 (dimanche)
daysOfWeek = {}
for d in datesMinPics : 
    date = datetime.datetime.strptime(d, "%Y-%m-%d")
    day = date.weekday()
    if day not in daysOfWeek : 
        daysOfWeek[day]=0
    daysOfWeek[day]+=1
minDays = sorted(daysOfWeek.items(), key=lambda t: t[1], reverse=True)

# de même pour les pics hauts 
daysOfWeek = {}
for d in datesMaxPics : 
    date = datetime.datetime.strptime(d, "%Y-%m-%d")
    day = date.weekday()
    if day not in daysOfWeek : 
        daysOfWeek[day]=0
    daysOfWeek[day]+=1
maxDays = sorted(daysOfWeek.items(), key=lambda t: t[1], reverse=True)

corres = {0:"lundi", 1:"mardi", 2:"mercredi", 3:"jeudi", 4:"vendredi", 5:"samedi", 6:"dimanche"}


# Répartition des pics hauts puis bas sur les jours de la semaine
print("\nrépartition des pics hauts sur les jours de semaine :\n")
for e in maxDays : 
    pourcent = (e[1]/len(datesMaxPics))*100
    print(corres[e[0]]+" --> "+str(pourcent))

print("\nrépartition des pics bas sur les jours de semaine :\n")
for e in minDays : 
    pourcent = (e[1]/len(datesMaxPics))*100
    print(corres[e[0]]+" --> "+str(pourcent))
