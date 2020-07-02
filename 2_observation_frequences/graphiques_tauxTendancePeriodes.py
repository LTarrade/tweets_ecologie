# coding: utf-8
import matplotlib.pyplot as plt
import scipy.fftpack
import pandas as pd
import scipy as sp
import numpy as np
import datetime

# récupération de chaque occurence du lexique identifiée dans le corpus et des informations associées 
df = pd.read_csv("./matches_anonymise.csv", index_col=0, sep=";")

exceptions = ["2007", "2008", "2009", "2010", "2011"]
dates = [d for d in sorted(set(df.date)) if d[:4] not in exceptions]


# Récupération des semaines
daysByWeek = {}
for d in dates : 
    dForm = datetime.datetime.strptime(d,"%Y-%m-%d")
    dWeek = dForm.isocalendar()
    week = str(dWeek[0])+"-"+str(dWeek[1])
    if not week.startswith("2011") :
        if week not in daysByWeek :
            daysByWeek[week] = {"nbTweetsWithMatch":0, "nbTotalTweets":0}
        sousDf = df[df.date==d]
        daysByWeek[week]["nbTweetsWithMatch"]+=len(set(sousDf.tweetId.tolist()))
        daysByWeek[week]["nbTotalTweets"]+=sousDf.nbTweetsTot_Date.tolist()[0]


# Récupération du pourcentage de tweets au sujet de l'écologie par semaines de 2013 à 2018 et application du produit de convolution
rates = []
for week in daysByWeek : 
    rate = (daysByWeek[week]["nbTweetsWithMatch"]/daysByWeek[week]["nbTotalTweets"])*100
    rates.append((week,rate))

df_byWeek = pd.DataFrame(rates,columns=["weeks","rates"])
df_byWeek["convolve"]=np.convolve(df_byWeek.rates, np.ones(15), "same")/15
df_byWeek = df_byWeek[(~df_byWeek.weeks.str.startswith("2012")) & (~df_byWeek.weeks.str.startswith("2019"))]


# Graphique correspondant au pourcentage de tweets liés à l'écologie par semaine
plt.figure(figsize=[16,4])

plt.plot(df_byWeek.weeks,df_byWeek.rates,color='#ffbb00',linewidth=2, label="pourcentage de tweets")
plt.fill_between(df_byWeek.weeks, df_byWeek.rates, facecolor='#ffbb00')

plt.xticks(rotation = 90)
plt.xlim(["2013-1","2018-52"])
plt.gca().axes.xaxis.set_ticks(range(0,len(df_byWeek.rates),4))
plt.grid(axis="x")
plt.title("Pourcentage de tweets concernant l'écologie par semaine pour les années 2013 à 2018")
plt.ylabel("%")
plt.legend()
plt.show()


# Application de la transformée de Fourier sur les données
fft=np.fft.fft(np.array(df_byWeek.rates))

# on récupère la valeur absolue puisqu'en résultat de la fft on a des nombres complexes (on prend la moitié car c'est totalement symétrique)
# on ne prend pas le premier élément car il représente tout ce qui n'a pas été capturé 
y=np.abs(fft)[1:156]

# on récupère la période en prenant l'inverse de la fréquence (qui est égale à 1/période)
x=1/np.fft.fftfreq(313)[1:156]


# Graphique des intensités de chaque période
plt.figure(figsize=(14,4))
plt.xticks(labels=[round(e,2) for i,e in enumerate(x) if i%2!=0], ticks=range(1,len(x),2))
plt.title("Intensité de chacune des périodes")
plt.grid(axis="x")
plt.xticks(rotation = 90)
plt.xlim(0,156)
plt.xlabel("Période (en nombre de semaine)")
plt.ylabel("Intensité")
plt.plot(y)

print("périodes les plus représentatives de la courbe et intensité correspondante :", sorted(list(zip(x,y)), key=lambda x:x[1], reverse=True)[:5])


# Affichage de la tendance (fft vs produit de convolution)
plt.figure(figsize=[16,4])

fft=scipy.fftpack.fft(np.array(df_byWeek.rates))
fft2 = np.abs(fft)

# on donne une intensité de 0 à toutes les périodes qui ne nous intéressent pas (toutes sauf les trois premières) pour qu'elles ne soient pas prise en compte lors de la reconstition de la courbe initiale
cutoff_idx = fft2 < 11
w2 = fft.copy()
w2[cutoff_idx] = 0

plt.plot(df_byWeek.weeks,np.fft.ifft(w2),color='#FEA800', linewidth=4, label="fft inversée")
plt.plot(df_byWeek.weeks,df_byWeek.convolve,color='#232528', linewidth=4, label="produit de convolution")

plt.xticks(rotation = 90)
plt.xlim(["2013-1","2018-52"])
plt.gca().axes.xaxis.set_ticks(range(0,len(df_byWeek.rates),4))
plt.title("Tendance, transoformée de Fourier inversée vs produit de convolution (fenêtre de 15)")
plt.ylabel("%")
plt.legend()
plt.show()


# Visualisation des périodes
def afficherCourbe(intensiteAgarder, dureePeriode, debutPeriode) :

    plt.figure(figsize=[16,4])

    fft=scipy.fftpack.fft(np.array(df_byWeek.rates))
    fft2 = np.abs(fft)

    # on donne une "intensité" de 0 à toutes les périodes qui ne nous intéresse pas pour qu'elles ne soient pas prise en compte lors de la reconstition de la courbe initiale
    cutoff_idx = fft2 < intensiteAgarder-0.001
    cutoff_idx2 = fft2 > intensiteAgarder+0.001
    w2 = fft.copy()
    w2[cutoff_idx] = 0
    w2[cutoff_idx2] = 0

    plt.plot(df_byWeek.weeks,df_byWeek.rates,color='#FFEEDB',linewidth=2, label="pourcentage de tweets")
    
    plt.axvspan(0, debutPeriode-dureePeriode, color='#345995')
    plt.axvspan(debutPeriode-dureePeriode, debutPeriode, color='#17BEBB')
    x = debutPeriode
    i=0
    while x<=313 :    
        if i%2==0 : 
            plt.axvspan(x, x+dureePeriode, color='#345995')
        else : 
            plt.axvspan(x, x+dureePeriode, color='#17BEBB')
        x+=dureePeriode
        i+=1
    
    plt.plot(df_byWeek.weeks,np.fft.ifft(w2),color='#ffbb00', linewidth=4, label="période "+str(dureePeriode))
        
    plt.xticks(rotation = 90)
    plt.xlim(["2013-1","2018-52"])
    plt.gca().axes.xaxis.set_ticks(range(0,len(df_byWeek.rates),4))
    plt.title("Pourcentage de tweets concernant l'écologie par semaine pour les années 2013 à 2018 et période observée")
    plt.ylabel("%")
    plt.xlim(["2013-1","2018-52"])
    plt.legend()
    plt.show()

# période 156
afficherCourbe(14.966,156.5,165.39)
# période 78
afficherCourbe(11.932,78.25,85.820)
# période 26
afficherCourbe(8.983,26.08,20.977)
# période 52
afficherCourbe(8.893,52.17,60.64)
