# coding: utf-8
from scipy.stats import hypergeom
import pandas as pd
import numpy as np
import sys

df = pd.read_csv("./freqByUser.csv", sep=";", index_col=0)

# "nettoyage du dataframe (on remet en str, on supprime les doublons, et on met les nan à 0)"
df.index = df.index.map(str)
df = df.loc[~df.index.duplicated(keep='first')]
df = df.fillna(0)


def specificities(lexicalTable):

    # nombre total de lemmes
    M=lexicalTable.sum().sum()

    # nombre total de lemmes pour chaque utilisateur 
    lengths=pd.DataFrame(lexicalTable.sum())

    # nombre total de chaque lemme 
    freq=pd.DataFrame(lexicalTable.sum(axis=1))

    # nombre "attendu" pour chaque lemme/utilisateur
    expectedCounts=(freq.dot(lengths.transpose()))/M

    specif=lexicalTable.copy()

    # calcul des spécificités pour chaque lemme/utilisateur
    for i,part in enumerate(lexicalTable.columns):
        sys.stdout.write("\rCalcul des spécificités pour l'utilisateur "+str(part)+" ("+str(i+1)+"/1008)")
        for word in lexicalTable.index:
            if (lexicalTable.loc[word,part]<expectedCounts.loc[word,part]) :
                specif.loc[word,part]=hypergeom.cdf(lexicalTable.loc[word,part],M, freq.loc[word], lengths.loc[part])
            else:
                specif.loc[word,part]=1-hypergeom.cdf(lexicalTable.loc[word,part]-1,M, freq.loc[word], lengths.loc[part])
    specif=np.log10(specif)
    specif[lexicalTable>=expectedCounts]=-specif[lexicalTable>=expectedCounts]

    return specif

specif = specificities(df)

print("\nEnregistrement des specifs dans specif.csv")
specif.to_csv("specif.csv", sep=";")
