# coding: utf-8

import matplotlib.pyplot as plt
import pandas as pd
import sys


df_matches = pd.read_csv("../observation_frequences/matches_anonymise.csv", sep=";", index_col=0)
df_users = pd.read_csv("./df_users_anonymise.csv", sep=";", index_col=0)
df_percent = pd.read_csv("./df_percent_anonymise.csv", sep=";", index_col=0)
df_nbTweetsTotByYearByUser = pd.read_csv("./df_nbTweetsTotByYearByUser_anonymise.csv", sep=";", index_col=0)


years = ["2013", "2014", "2015", "2016", "2017", "2018"]


usersByYear = {}

y_croissTweetsMoy_Ecol = []
y_croissUser_Ecol = []

y_croissTweetsMoy_Glob = []
y_croissUser_Glob = []

for y in years : 
    sousDf = df_matches[df_matches.date.str.startswith(y)]
    usersByYear[y]=set(sousDf.userId.tolist())
    
    # Récupération du nombre moyen de tweets par utilisateur pour les tweets liés à l'écologie
    nbTweets = len(set(sousDf.tweetId.tolist()))
    nbUser = len(usersByYear[y])
    moy = nbTweets/nbUser
    
    # Récupération du nombre moyen de tweets par utilisateur pour l'ensemble des tweets
    sousDf_global = df_nbTweetsTotByYearByUser[~df_nbTweetsTotByYearByUser[y].isna()]
    nbUser_global = len(sousDf_global)
    nbTweets_global = sousDf_global[y].sum()
    moy_global = nbTweets_global/nbUser_global
    
    percentUser = round((nbUser/nbUser_global)*100,2)
    print(y,"pourcentage des utilisateurs qui twittent sur l'écologie : "+str(percentUser)+"%")
        
    if y!="2013" :

        # Calcul de la croissance du nombre moyen de tweets par utilisateurs chaque année pour les tweets liés à l'écologie et pour l'ensemble des tweets
        croiss = ((moy-prec)/prec)*100
        croiss_global = ((moy_global-prec_global)/prec_global)*100
        y_croissTweetsMoy_Ecol.append(croiss)
        y_croissTweetsMoy_Glob.append(croiss_global)
        
        # Calcul de la croissance du nombre d'utilisateur chaque année pour les tweets liés à l'écologie et pour l'ensemble des tweets
        croissUser = ((nbUser-precUser)/precUser)*100
        croissUser_global = ((nbUser_global-precUser_global)/precUser_global)*100
        y_croissUser_Ecol.append(croissUser)
        y_croissUser_Glob.append(croissUser_global)
        
        # croissance du pourcentage des utilisateurs qui twittent sur l'écologie
        croissPercentUser = ((percentUser-percentUser_prec)/percentUser_prec)*100
        print("croissance par rapport à "+str(int(y)-1)+" : "+str(round(croissPercentUser,2))+"%\n")
    
    prec = moy
    precUser = nbUser

    prec_global = moy_global
    precUser_global = nbUser_global

    percentUser_prec = percentUser    


# visualistation des résultats
plt.figure(figsize=[16,8])

barWidth = 0.3
r1 = [-0.5,1.5,3.5,5.5,7.5]
r2 = [x + barWidth for x in r1]
r3 = [x + 0.4 for x in r2]
r4 = [x + barWidth for x in r3]


plt.bar(r1, y_croissTweetsMoy_Glob, width = barWidth, label="croissance du nombre moyen de tweets par utilisateur dans l'ensemble des tweets", color="#7D4F50")
plt.bar(r2, y_croissUser_Glob, width = barWidth, label="croissance du nombre d'utilisateurs dans l'ensemble des tweets", color="#CC8B86")

plt.bar(r3, y_croissTweetsMoy_Ecol, width = barWidth, label="croissance du nombre moyen de tweets par utilisateur dans les tweets liés à l'écologie", color="#19647E")
plt.bar(r4, y_croissUser_Ecol, width = barWidth, label="croissance du nombre d'utilisateurs dans les tweets liés à l'écologie", color="#119DA4")

plt.xticks([r*2 for r in range(len(y_croissTweetsMoy_Glob))], ["2013-2014", "2014-2015", "2015-2016", "2016-2017", "2017-2018"])

plt.grid(axis="x")

plt.ylim([-20,60])
plt.axhline(y=0, color="black")

plt.text(x=-0.40, y=57, s="229.31%")
plt.text(x=0.30, y=57, s="144.59%")
plt.text(x=-0.70, y=-18, s="-25.72%")

plt.legend()


# Fonction permettant d'afficher pour une variable (par ex. "income") la comparaison de la moyenne pour l'ensemble des utilisateurs et pour les utilisateurs twittant à propos d'écologie ainsi que le graphique correspondant. Indique aussi l'écart entre les deux et l'évolution de celui pour chaque année. 
def compareMeans(var) : 
    
    moyEcol = []
    moyGlob = []

    for y in usersByYear : 
        # Récupération de la moyenne de la variable observé pour les utilisateurs twittant sur l'écologie
        sousDf = df_users[df_users.index.isin(usersByYear[y])]
        moy = sousDf[var].mean()
        print("\n"+str(y))
        print("moyenne des utilisateurs twittant à propos d'écologie - "+var+": "+str(round(moy,2)))
        moyEcol.append(moy)

        # Récupération de la moyenne de la variable observé pour l'ensemble des utilisateurs
        allUsersInYear = df_nbTweetsTotByYearByUser[~df_nbTweetsTotByYearByUser[y].isna()].index.tolist()
        sousDf_global = df_users[df_users.index.isin(allUsersInYear)]
        moy_global = sousDf_global[var].mean()
        print("moyenne globale - "+var+": "+str(round(moy_global,2)))
        moyGlob.append(moy_global)

        ecartMoy = moy-moy_global
        print("écart avec moyenne globale : "+str(round(ecartMoy,2)))

        # Calcul de la croissance de l'écart d'une année sur l'autre
        if y!="2013" :
            croissMoy = ((ecartMoy-ecartMoy_prec)/ecartMoy_prec)*100 
            print("croissance de l'écart avec la moyenne globale : "+str(round(croissMoy,2))+"%")

        ecartMoy_prec = ecartMoy

    # Visualisation graphique de la moyenne chaque année pour les deux populations
    plt.figure(figsize=[14,6])
    plt.plot(years, moyGlob, label="moyenne globale - "+var)
    plt.plot(years, moyEcol, label="moyenne des utilisateurs twittant à propos d'écologie - "+var)
    plt.legend()
    plt.grid(axis="y")
    plt.show()

compareMeans("income")


# Fonction permettant d'obtenir pour chaque année la moyenne du revenu annuel et de la densité de population des utilisateurs dont les tweets liés à l'écologie sont en hausse et inversement 
def meanCroissAndDec(y1,y2) :
    
    # Récupération du pourcentage de tweets liés à l'écologie ; seuls les utilisateurs qui ont produit des tweets pendant ces deux années sont pris en compte
    usersWithTweets = df_percent[(~df_percent[y1].isna()) & (~df_percent[y2].isna())].index.tolist()
    usersWithTweets_dict = {}
    for u in usersWithTweets : 
        usersWithTweets_dict[u]=""
    
    decr = []
    croi = []

    # Récupération des utilisateurs dont les tweets liés à l'écologie sont en hausse et de ceux pour qui ils sont en baisse
    for user,row in df_percent.iterrows() :
        if user in usersWithTweets_dict and row[y2]>row[y1] :
            croi.append(user)
        if user in usersWithTweets_dict and row[y2]<row[y1] :
            decr.append(user)
    print("\n%s => %s\n"%(y1,y2))

    print("moyenne revenus croissance : "+str(round(df_users[df_users.index.isin(croi)]["income"].mean(),2)))
    print("moyenne revenus décroissance : "+str(round(df_users[df_users.index.isin(decr)]["income"].mean(),2)))

    print("\nmoyenne population_density croissance : "+str(round(df_users[df_users.index.isin(croi)]["population_density"].mean(),2)))
    print("moyenne population_density décroissance : "+str(round(df_users[df_users.index.isin(decr)]["population_density"].mean(),2)))

meanCroissAndDec("2017", "2018")