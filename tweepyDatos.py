# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 13:22:52 2020

@author: Personal
"""

"""
Instalar tweepy en anaconda
conda install -c conda-forge tweepy
"""

import tweepy
#import json

import numpy as np
import pandas as pd
import statistics as st
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import os

from flask import Flask
#from flask_restful import Resource#, Api
from flask import request
from flask import render_template

api_key="PEyKaQRso7DANXqsdPlII9PZt"
api_secret="NkctVaSlHTjCPNVJoJcBkYvLdN4wN5K8x2zkUxBbIjznPfK9tw"
access_token="1227702001561153537-K5igSJwVl6FncvWL1eWlkKPtl3WFRE"
access_token_secret="Xx6FIcKpsSmpmPHciWw5zu9tYEQI0Mb9qEVeJPryeRn66"

autentica = tweepy.OAuthHandler(api_key,api_secret)
autentica.set_access_token(access_token,access_token_secret)
api = tweepy.API(autentica,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

app=Flask(__name__)

def listado_tweets():
    comentarios=tweepy.Cursor(api.search,q="mcdonalds",tweet_mode="extended",lang='es').items(100)
    
    arreglo=[]
    
    indices=['screen_name','friends_count','followers_count','full_text','retweet_count']
    datos=pd.DataFrame(columns=indices)
    
    #datos['screen_name']=[tuit.author._json['screen_name'] for tuit in comentarios]
    #datos['friends_count']=[tuit.author._json['friends_count'] for tuit in comentarios]
    #datos['followers_count']=[tuit.author._json['followers_count'] for tuit in comentarios]
    #datos['full_text']=[tuit._json['full_text'] for tuit in comentarios]
    #datos['retweet_count']=[tuit._json['retweet_count'] for tuit in comentarios]
    a=[]
    b=[]
    c=[]
    d=[]
    e=[]
    
    for tuit in comentarios:
        #print(tuit)
        #friends_count : Número de personas a las que sigo
        #followers_count: Número de seguidores que tengo
        #screen_name: Nombre con el que se anuncia en link
        #retweet_count: número de retweets de una publicación
        #print(tuit._json["author"][])
        a.append(str(tuit.author._json["screen_name"]))
        b.append(int(tuit.author._json["friends_count"]))
        c.append(int(tuit.author._json["followers_count"]))
        d.append(str(tuit._json['full_text']))
        e.append(int(tuit._json['retweet_count']))
        #datos[i].append(tuit.author._json["screen_name"])
        #print(tuit._json["full_text"])
        #print(tuit._json["retweet_count"])
        #arreglo[i]=tuit._json[i]
        arreglo.append(tuit)
    
    datos['screen_name']=a
    datos['friends_count']=b
    datos['followers_count']=c
    datos['full_text']=d
    datos['retweet_count']=e
    
    return datos

datos=listado_tweets()

@app.route("/")
@app.route("/index.html")
def envioDatos():
    
    return render_template("index.html",gener=general,grande=grandote,pequeno=pequeno)

#Se mira la media
mediau=datos['retweet_count'].mean()
#Se mira la mediana (y la moda). Se ve que el dato central es muy bajo en comparación con la media
#separar retweets grandes y pequeños
mediana=datos['retweet_count'].median()
moda=datos['retweet_count'].mode()
#varianza=st.variance(datos['retweet_count'])
desvia=np.std(datos['retweet_count'])
rango=max(datos['retweet_count'])-min(datos['retweet_count'])
#print(rango)
general=[mediau,mediana,moda[0],desvia,rango]

def torta():
    labels=['Publicaciones con menos \nde 1000 retweets','Publicaciones con más \nde 1000 retweets']
    porcent=[datos['retweet_count'][datos['retweet_count']<1000].count()*100/datos.size, datos['retweet_count'][datos['retweet_count']>=1000].count()*100/datos.size]
    #print(porcent)
    #fig=Figure()
    #esca=fig.add_subplot(1,1,1)
    fig, esca=plt.subplots()
    esca.pie(porcent,labels=labels,autopct='%1.1f%%')
    plt.savefig(os.getcwd()+"/static/imagen/Pie.png")
    #return fig

#torta()
#------------------------------------------------------------------------------

grandes=datos[datos['retweet_count']>=1000]
pequenos=datos[datos['retweet_count']<1000]

#Sacar info de ambos
media_g=grandes['retweet_count'].mean()
mediana_g=grandes['retweet_count'].median()
#varianza_g=st.variance(grandes['retweet_count'])
desvia_g=np.std(grandes['retweet_count'])
moda_g=grandes['retweet_count'].mode()

grandote=[media_g,mediana_g,moda_g[0],desvia_g]


media_p=pequenos['retweet_count'].mean()
mediana_p=pequenos['retweet_count'].median()
#varianza_p=st.variance(pequenos['retweet_count'])
desvia_p=np.std(pequenos['retweet_count'])
moda_p=pequenos['retweet_count'].mode()

pequeno=[media_p,mediana_p,moda_p[0],desvia_p]


#fig, esca=plt.subplots()
#esca.scatter(pequenos['retweet_count'][pequenos['followers_count']<5000],pequenos['followers_count'][pequenos['followers_count']<5000])
#plt.show()

"""comen_gra=[]
for x in range(1,10;1):
    comen_gra.append()"""
#print(moda)

if __name__ == '__main__':
    torta()
    app.run(port=5000)
