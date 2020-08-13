# coding: utf-8

import tweepy
import ujson
import time

consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# noms des comptes pour lesquels on souhaite récupérer les tweets
sources = ["FNEasso", "amisdelaterre", "greenpeacefr", "WWFFrance", "EELV", "Reporterre", "APEnvironnement", "FondationNH"]

for source in sources :      
    
    max_id = None

    user = api.get_user(source)
    id_user = user.id_str
    
    out = open("./data/"+source+".json", "a")

    nbTweets = 0

    while nbTweets<=20000 : 
        
        nbTweets+=200
        
        try : 
            
            for i,status in enumerate(api.user_timeline(user_id=id_user, count=200, include_rts=True, max_id=max_id, tweet_mode="extended")) :

                if max_id!=None and i==0 :
                    continue
                    
                tweetInfos = ujson.dumps(status._json)
                out.write(tweetInfos+"\n")
                                
                max_id = status._json["id"]
                    
        except Exception as e : 
            
            print(e)
            time.sleep(900)

    out.close()


