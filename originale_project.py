from flask import Flask, render_template


app = Flask(__name__)


import requests 
import json 
from datetime import datetime  



def get3(tems):
  tem3 = []
  for i in range(0,len(tems),3):
    tem3.append(tems[i])
  return tem3

def hours():
    hour = []
    for i in range(0,22,3):
        hour.append(i)
    return hour

def just3(list):
  list3 = []
  for i in range(0,len(list),3):
    list3.append(list[i])
  return list3



hour = hours()


dateLyouma=datetime.today().strftime("%Y-%m-%d") 

url=" https://api.open-meteo.com/v1/forecast?latitude=31,51&longitude=9,77&hourly=temperature_2m&start_date="+dateLyouma+"&end_date="+dateLyouma+"&daily=sunrise"+"&daily=sunset"
response=requests.get(url) 
response=requests.get(url).content.decode('utf-8') 
data = json.loads(response) 
tem = data[0]["hourly"]["temperature_2m"]
tem3 = get3(tem)


nomLyouma=datetime.today().strftime("%A") 


jours={'Monday':'Lundi','Tuesday':'Mardi', 'Wednesday':'Mercredi', 
'Thursday':'jeudi', 'Friday':'Vendredi', 'Saturday':''} 
nomlyouma = jours[nomLyouma]



url2=" https://api.open-meteo.com/v1/forecast?latitude=31,51&longitude=9,77&hourly=cloud_cover&start_date="+dateLyouma+"&end_date="+dateLyouma+"&daily=sunrise"+"&daily=sunset"
response=requests.get(url2) 
response=requests.get(url2).content.decode('utf-8') 
data = json.loads(response) 
perces = data[0]["hourly"]["cloud_cover"]
perces3 = just3(perces)



url3=" https://api.open-meteo.com/v1/forecast?latitude=31,51&longitude=9,77&hourly=precipitation&start_date="+dateLyouma+"&end_date="+dateLyouma+"&daily=sunrise"+"&daily=sunset"
preci=requests.get(url3) 
preci=requests.get(url3).content.decode('utf-8') 
data = json.loads(preci) 
preci = data[0]["hourly"]["precipitation"]
preci3 = just3(preci)


url4=" https://api.open-meteo.com/v1/forecast?latitude=31,51&longitude=9,77&hourly=wind_speed_80m&start_date="+dateLyouma+"&end_date="+dateLyouma+"&daily=sunrise"+"&daily=sunset"
speed=requests.get(url4) 
speed=requests.get(url4).content.decode('utf-8') 
data = json.loads(speed) 
speed = data[0]["hourly"]["wind_speed_80m"]
speed3 = just3(speed)


url5=" https://api.open-meteo.com/v1/forecast?latitude=31,51&longitude=9,77&hourly=relative_humidity_2m&start_date="+dateLyouma+"&end_date="+dateLyouma+"&daily=sunrise"+"&daily=sunset"
humidity=requests.get(url5) 
humidity=requests.get(url5).content.decode('utf-8') 
data = json.loads(humidity) 
humidity = data[0]["hourly"]["relative_humidity_2m"]
humidity3 = just3(humidity)



@app.route('/')
def start():
    return"hello start page"

@app.route("/home")
def home():
    return render_template('home.html',tem=tem3,jour=nomlyouma,hours=hour,pers=perces3,precipitation=preci3,speed=speed3,humidity=humidity3,dateLyouma=dateLyouma )











