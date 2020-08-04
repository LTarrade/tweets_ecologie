Tweets et Écologie
=


*1_construction_lexique*
-

1. **recuperationTweets.py** : récupère les 3200 derniers tweets d'une liste de compte Twitter (nécessite d'avoir un compte Twitter Developer)

2. **extractFreq.py** : construit un dataframe *freqByUser.csv* contenant en colonne les noms des comptes twitter et en ligne chacun des tokens présent dans l'ensemble des tweets de tous les utilisateurs. Pour chaque token nous y trouvons le nombre d'occurrence par utilisateur.  


	| tokens/comptes|user1|user2|user3|user4|user5|user6|user7|user8|
	| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
	| banque|4.0|6.0|8.0|6.0|0.0|23.0|8.0|9.0|
	| environnement|104.0|73.0|58.0|66.0|67.0|63.0|50.0|123.0|
	| aussi|100.0|85.0|83.0|108.0|65.0|50.0|75.0|138.0|
	| longtemps|6.0|6.0|11.0|6.0|2.0|7.0|2.0|1.0|
	| que|597.0|424.0|620.0|703.0|436.0|466.0|517.0|643.0|


	nécessite en entrée les tweets de chaque compte Twitter au format json, regroupés par utilisateurs (1 fichier = l'ensemble des tweets d'un utilisateur), les fichiers étant nommés par l'identifiant ou le screen_name de l'utilisateur (ex. "screenName.json")

3. **calculSpec.py** : construit un dataframe *specif.csv* à partir de *freqByUser.csv* contenant au lieu du nombre d'occurrences le score de spécifité de chacun des token pour chaque compte Twitter. 


*2_observation_frequences*
-

1. **extractionFreq.py** : à partir de *listeMots.txt*, parcourt l'ensemble du corpus de tweets au format json et récupère chaque occurrence de chaque mot du lexique (mots et tweets mis en minuscules et sans signes diacritiques) pour la stocker dans un dataframe *matches.csv* (cf. ci-dessous). En parallèle, pour alimenter le dataframe, récupère le nombre de tweets total de chaque jour.
	Nécessite *listeMots.txt*, ainsi que le corpus de tweets au format *json*, chaque fichier contenant l'ensemble des tweets d'une journée et nommé par la date et l'heure de cette journée (ex. 2019-03-14T05.data) 

2. **listeMots.txt** : fichier contenant une expression régulière par ligne représentant chacune les mots liés à l'écologie du lexique et les cas à exclure.

3. **matches_anonymise.csv** : dataframe (anonymisé) contenant pour chaque occurrence d'un mot du lexique le mot en question, la date du tweet dans lequel il apparaît (format aaaa-mm-jj), l'identifiant du tweet auquel il appartient, l'identifiant de l'utilisateur qui a écrit le tweet, et le nombre total de tweets à cette date dans notre corpus.

	| match|date|tweetId|userId|nbTweetsTot_Date|
	| :-: | :-: | :-: | :-: | :-: |
	| pollution|2016-08-30|tweet83270|user3472|61372|
	| climat|2016-08-30|tweet88519|user2094|61372|
	| ecologistes|2016-08-30|tweet105505|user12032|61372|
	| developpement durable|2016-05-04|tweet287324|user42187|52272|
	| climat|2012-02-09|tweet218436|user42106|3499|
	| rechauffement climatique|2013-12-19|tweet309701|user46608|32397|

4. **graphiques_tauxTendancePeriodes.py** : à partir de *matches_anonymise.csv*, permet de : 
	- visualiser le pourcentage de tweets liés à l'écologie par semaines de 2013 à 2018
	- visualiser la tendance de la courbe 
	- visualiser les périodes de forte intensité


5. **termes.py** : à partir de *matches_anonymise.csv* permet d'observer le taux de croissance des mots du lexique d'année en année, mais également de connaître leur répartition pour une période donnée et de connaître la répartition du pourcentage de tweets lors des pics hauts et bas par jour de la semaine. 


*3_embedding*
-

1. **preprocessing.py** : effectue un prétraitement de tweets fournis en entrée (le fichier doit contenir un tweet par ligne). Le prétraitement est le suivant :
	- mise en minuscule
	- suppression des mentions
	- suppression des url
	- suppression des ponctuations
	- suppression des emojis et émoticônes

2. **buildModels.py** : permet d'entraîner les modèles correspondant à chaque année. Le premier modèle est construit à partir de l'architecture Skip-gram, mais le reste des paramètres est laissé par défaut. Les poids neuronaux du modèle suivant sont initialisés à partir de ceux de l'année précédante. 
	Nécessite un fichier contenant l'ensemble des tweets prétraités de l'année (un tweet par ligne)

3. **vectorsMostSimil.py** : permet de récupérer pour une liste de mots donnée, l'ensemble des vecteurs de ce mots des différentes années, mais aussi la moyenne sur ces années de ceux de leurs 100 mots les plus similaires communs à celles-ci. 
	Nécessite les différents modèles initialisés à chaque fois avec celui de l'année précédente, ainsi qu'une liste de mots pour lesquels récupérer les vecteurs.
	Fournit en sortie un dataframe pour chacun des mots de la liste, contenant les vecteurs moyens des 100 mots les plus similaires de chaque année (et communs à l'ensemble des années) ainsi que les vecteurs du mot pour chacune d'entre elles. Chaque vecteur possède 100 dimensions.

	| mot|dim_1|dim_2|dim_3|...dim_100|
	| :-: | :-: | :-: | :-: | :-: |
	| chat_2014|0.093132|0.281426|-0.096384|0.122889|
	| chat_2015|0.100094|0.168750|-0.062519|0.143034|
	| lapinou|0.111665|0.196129|0.184149|0.034941|
	| chihuahua|-0.077142|0.418391|-0.039803|0.214153|
	| oiseau|0.090136|0.443442|-0.209377|0.018408|
	| sphynx|-0.095792|0.372330|0.360945|0.064614|
	| miaule|-0.170994|0.029766|-0.212292|0.339495|

	Fournit également une fonction pour visualiser les projections. Peut-être tester à partir des exemples fournis dans le dossuer *data_example*

4. **data_example** : dossier contenant des dataframes générés à partir de la méthode décrite ci-dessus et pouvant être utilisés pour créer des visualisations. Le mot concerné constitue le nom du dataframe. 


*4_utilisateurs*
-

1. **socioDem.py** : permet d'obsever la croissance du nombre moyen de tweets par utilisateur dans l'ensemble des tweets et dans les tweets liés à l'écologie, ainsi que l'évolution du pourcentage d'utilisateurs dans ces deux ensembles. Fournit également une fonction pour comparer les moyennes de certaines variables sociodémographiques de l'ensemble des utilisateurs et des utilisateurs ayant twitté sur l'écologie d'année en année, et une autre pour observer les moyennes de ces variables pour les utilisateurs dont les tweets liés à l'écologie ont connus une baisse ou une hausse d'une année sur l'autre. 

	Nécessite 4 dataframes :

	- *matches.csv*, déjà décrit ci-dessus (dans *2_observation_frequences*)
	- *df_users* : un fichier *.csv* contenant pour chaque utilisateur (en index) les informations sociodémographiques qui lui sont associées ainsi que son nombre de tweets total (en colonne)
	- *df_percent* : fichier *.csv* contenant pour chaque utilisateur (en index) son pourcentage de tweets liés à l'écologie par année (en colonne)
	- *df_nbTweetsTotByYearByUser* : fichier *.csv* contenant pour chaque utilisateur (en index) son nombre total de tweets dans le corpus par année (en colonne)

2. **localisation.ipynb** : notebook jupyter permettant de visualiser sur une carte le pourcentage d'utilisateurs twittant à propos d'écologie dans chaque département à une année donnée et le pourcentage de voix obtenu par EELV, ainsi que de calculer le coefficient de Pearson entre ces deux variables et de visualiser l'autocorrélation spatiale globale et locale pour chacune d'entre elles et ainsi identifier les clusters.
Nécessite en entrée le fichier geojson *infosParDep.geojson*. 

3. **infosParDep.geojson** : fichier geojson contenant pour chaque département : 
	- le code du département 
	- le nom du département
	- le résultat en pourcentage de voix exprimées obtenu par EELV aux élections européennes de 2014 et 2019 (récupérés respectivement sur *https://www.data.gouv.fr/fr/datasets/elections-europeennes-2014-resulta-2/* et *https://www.data.gouv.fr/fr/datasets/resultats-des-elections-europeennes-2019/*)
	- le pourcentage d'utilisateurs twittant à propos d'écologie pour chaque année de 2014 à 2015 (un utilisateur est considéré comme tel s'il a plus d'un tweet en lien avec l'écologie et si plus de 1% de ses tweets sont relatifs à l'écologie)
	- les coordonnées géographiques délimitant les contours du département (récupérées sur *https://github.com/gregoiredavid/france-geojson*) 
