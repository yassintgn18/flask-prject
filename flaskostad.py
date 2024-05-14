from flask import Flask,render_template
from datetime import datetime
import requests
import json

#------copy----------------------------------------------------------------------*
  #-------pour time
  

gpsdict = {"essaouira":(),"safi":(),"ouajda":(),"titouan":(),"jagora":()}


dateLyouma=datetime.today().strftime("%Y-%m-%d")
lyouma = dateLyouma
nomLyouma=datetime.today().strftime("%A")
jours={'Monday':'Lundi','Tuesday':'Mardi', 'Wednesday':'Mercredi',
'Thursday':'jeudi', 'Friday':'Vendredi', 'Saturday':'Samedi','Sunday':'dimanche'}
nhar= jours[nomLyouma]
maintenant = datetime.now()
#-------------------list des heurs----------------
heurs = ["0:00","3:00","9:00","12:00","15:00","18:00","21:00","24:00"]



url="https://api.open-meteo.com/v1/forecast?"
url=url+"latitude=31,51&longitude=-9,77"
url=url+"&hourly=temperature_2m"
url=url+"&hourly=wind_speed_10m"
url=url+"&hourly=cloud_cover"
url=url+"&daily=sunrise"
url=url+"&daily=sunset"
url=url+"&hourly=rain"
url=url+"&start_date="+lyouma
url=url+"&end_date="+lyouma

response=requests.get(url)
response=requests.get(url).content.decode('utf-8')
data = json.loads(response)
#--------les  fonctions
def ri3valeur(listy):
  li=[]
  for i in range(0,len(listy),3):
    li.append(listy[i])
  return (li)


  #-----pour les valeur de metio

listrain = ri3valeur(data[0]["hourly"]["rain"])
listeTemp = ri3valeur(data[0]["hourly"]["temperature_2m"])
listwind = ri3valeur(data[0]["hourly"]["wind_speed_10m"])
listecloud = ri3valeur(data[0]["hourly"]["cloud_cover"])
windlist = data[0]["hourly"]["wind_speed_10m"]



#-------------------new time---------------------------
from datetime import datetime
dateLyouma=datetime.today().strftime("%d-%m-%Y")
newlyouma = dateLyouma

#---------------function----pour---metre----les--images-----------------
heurs = ["00:00","03:00","09:00","12:00","15:00","18:00","21:00","24:00"]


listsunset = data[0]["daily"]["sunset"]
listsunrise = data[0]["daily"]["sunrise"]

suns =int(listsunset[0][11:13])
sunr = int(listsunrise[0][11:13])


listdict =[]
for i in range(8):
  dicttow={}
  dicttow["temperature"] =listeTemp[i]
  if i >= 4 :
    dicttow["temps"] = "{}:00".format(i*3)
  else:
    dicttow["temps"] = "0{}:00".format(i*3)
  dicttow["rain"] = listrain[i]
  dicttow["wind"] =str(max([windlist[0+i*3] ,windlist[1+i*3],windlist[2+i*3]]))+"-"+str(min([windlist[0+i*3] ,windlist[1+i*3],windlist[2+i*3]]))
  dicttow["cloud"] = listecloud[i]
  listdict.append(dicttow)


#---------------function----pour---metre----les--images-----------------
def getImagesSoliel (listeTemp,listecloud,listrain,listdict):
  for j,i  in enumerate(listeTemp) :
    heur =int(heurs[j][0:2])
    if i < 10 and listecloud[j] != 0 and listrain[j] == 0 :
      if sunr <= heur and suns >= heur:
        listdict[j]["image"]="images/sunCloudy.png"
      else :
        listdict[j]["image"]="images/moon_cloudy.png"

    elif  i < 10 and listrain[j] != 0 :
      if sunr <= heur and suns >= heur:
        listdict[j]["image"]="images/sunRain.png"
      else :
        listdict[j]["image"]="images/moon_rain.png"

    elif i < 20 and  listrain[j] != 0 :
      if sunr <= heur and suns >= heur and i < 20 :
          listdict[j]["image"]="images/sunRain.png"
      else:
        listdict[j]["image"]="images/moon_rain.png"
        
    elif i <20 and listecloud[j] != 0 and  listrain[j] == 0 :
      if sunr <= heur and suns >= heur and i <20:
         listdict[j]["image"]="images/sunCloudy.png"
      else :
       listdict[j]["image"]="images/moon_cloudy.png"
    elif i <20   :
      if sunr <= heur and suns >= heur and i <20:
         listdict[j]["image"]="images/1.png"
      else :
       listdict[j]["image"]="images/moon.png"
    
    else :
      if sunr <= heur and suns >= heur  :
        listdict[j]["image"]="images/soliel_choud.png"
      else:
         listdict[j]["image"]="images/moon.png"

  return listdict 


listdict = getImagesSoliel(listeTemp,listecloud,listrain,listdict)

