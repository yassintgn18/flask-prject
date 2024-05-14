from flask import Flask, render_template, request
import requests 
import json 
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import redirect

current_time = datetime.now()

current_hour = current_time.hour

hfds = str(current_hour)

app = Flask(__name__)

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
heurs = ["00:00","03:00","06:00", "09:00","12:00","15:00","18:00","21:00"]

hlfds = []
for i in heurs:
  hlfds.append(i[1:2])

id = 0
for i in hlfds:
  if i < hfds:
    id += 1



print(id)



hoursforbonne = []

for h in heurs:
  h = h[:2]
  if h[0]  == '0':
    h = h[1]
  h =int(h)
  hoursforbonne.append(h)
    
dateLyouma=datetime.today().strftime("%Y-%m-%d") 

url=" https://api.open-meteo.com/v1/forecast?latitude=31,51&longitude=9,77&hourly=temperature_2m&start_date="+dateLyouma+"&end_date="+dateLyouma+"&daily=sunrise"+"&daily=sunset"
response=requests.get(url) 
response=requests.get(url).content.decode('utf-8') 
data = json.loads(response) 
tem = data[0]["hourly"]["temperature_2m"]
tem3 = get3(tem)

nomLyouma=datetime.today().strftime("%A") 

jours={'Monday':'Lundi','Tuesday':'Mardi', 'Wednesday':'Mercredi', 'Thursday':'jeudi', 'Friday':'Vendredi', 'Saturday':'Samedi', 'Sunday':'dimanche'}

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

listsunset = data[0]["daily"]["sunset"]
listsunrise = data[0]["daily"]["sunrise"]

suns =int(listsunset[0][11:13])
sunr = int(listsunrise[0][11:13])

listdict =[]
for i in range(8):
  dicttow={}
  dicttow["temperature"] =tem3[i]
  
  if i >= 4 :
    dicttow["temps"] = "{}:00".format(i*3)
  else:
    dicttow["temps"] = "0{}:00".format(i*3)

  dicttow["precipitation"] = preci3[i]
  dicttow["cloud_cover"] = perces3[i]
  dicttow["wind_speed_80m"] = speed3[i]

  listdict.append(dicttow)

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
         listdict[j]["image"]="images/soliel_choud.png"
      else :
       listdict[j]["image"]="images/moon.png"
    
    else :
      if sunr <= heur and suns >= heur  :
        listdict[j]["image"]="images/soliel_choud.png"
      else:
         listdict[j]["image"]="images/moon.png"

  return listdict 

infos = getImagesSoliel(tem3,perces3,preci3,listdict)

from flask import Flask, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_states.db'  # Nom de la base de données SQLite
db.init_app(app)

statues_list_for_html1 = []

@app.route('/')
def start():
  with app.app_context():

    all_user_states1 = users_states.query.with_entities(users_states.id).all()
    for state in all_user_states1:
      statues_list_for_html1.append(state)
    return render_template('state.html',
      statues_list_for_html1 = statues_list_for_html1)
  

@app.route('/home/<action>', methods=['POST', 'GET'])
def statue(action = 2):
  with app.app_context():
    new_user_state = users_states(userstate=str(action))
    db.session.add(new_user_state)
    db.session.commit()
  return render_template('home2.html', 
                          tem=tem3,
                          jour=nomlyouma,
                          hours=hour,
                          pers=perces3,
                          precipitation=preci3,
                          speed=speed3,
                          humidity=humidity3,
                          dateLyouma=dateLyouma,
                          infos=infos, 
                          current_hour=current_hour, 
                          statue = action,
                          hoursforbonne=hoursforbonne)


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UsersStates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userstate = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<UsersStates %r>' % self.id


"""print(len(infos))

statues_list_for_html1 = []
statues_list_for_html2 = []
statues_list_for_html3 = []
statues_list_for_html4 = []


from flask import Flask, render_template
from models import db, users_states11




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_states11.db'  # Nom de la base de données SQLite
db.init_app(app)




@app.route('/')
def start():
  with app.app_context():

    all_user_states1 = users_states11.query.with_entities(users_states11.id).all()
    all_user_states2 = users_states11.query.with_entities(users_states11.date_created).all()
    all_user_states3 = users_states11.query.with_entities(users_states11.temperature).all()
    all_user_states4 = users_states11.query.with_entities(users_states11.cloud_cover).all()
    for state in all_user_states1:
      statues_list_for_html1.append(state)
    for state in all_user_states2:
      statues_list_for_html2.append(state)
    for state in all_user_states3:
      statues_list_for_html3.append(state)
    for state in all_user_states4:
      statues_list_for_html4.append(state)
  return render_template('state.html',
    statues_list_for_html1 = statues_list_for_html1,
    statues_list_for_html2 = statues_list_for_html2,
    statues_list_for_html3 = statues_list_for_html3,
    statues_list_for_html4 = statues_list_for_html4,)



@app.route('/home')
def home1():
    return render_template('home2.html',
                           tem=tem3,
                           jour=nomlyouma,
                           hours=hour,
                           pers=perces3,
                           precipitation=preci3,
                           speed=speed3,
                           humidity=humidity3,
                           dateLyouma=dateLyouma,
                           infos=infos, 
                           current_hour=current_hour, 
                           hoursforbonne=hoursforbonne
                           )"""


"""@app.route('/home/<action>', methods=['POST', 'GET'])
def statue(action = 2):
  with app.app_context():
    new_user_state = users_states(userstate=str(action))
    db.session.add(new_user_state)
    db.session.commit()
  return render_template('home2.html', 
                          tem=tem3,
                          jour=nomlyouma,
                          hours=hour,
                          pers=perces3,
                          precipitation=preci3,
                          speed=speed3,
                          humidity=humidity3,
                          dateLyouma=dateLyouma,
                          infos=infos, 
                          current_hour=current_hour, 
                          statue = action,
                          hoursforbonne=hoursforbonne)"""



"""@app.route('/home/<action>', methods=['POST', 'GET'])
def statue(action = 2):
  global id
  id = id - 1
  with app.app_context():
    temperature = users_states11(temperature = infos[id]['temperature'])
    db.session.add(temperature)

    cloud_cover = users_states11(cloud_cover = infos[id]['cloud_cover'])
    db.session.add(cloud_cover)

    wind_speed = users_states11(wind_speed = infos[id]['wind_speed_80m'])
    db.session.add(wind_speed)

    precipitation = users_states11(precipitation = infos[id]['precipitation'])
    db.session.add(precipitation)

    if action == 'bonne':
      good_condition = users_states11(good_condition = True)
      db.session.add(good_condition)
      bad_condition = users_states11(bad_condition = False)
      db.session.add(bad_condition)
    else:
      bad_condition = users_states11(bad_condition = True)
      db.session.add(bad_condition)
      good_condition = users_states11(good_condition = False)
      db.session.add(good_condition)
    db.session.commit()

  return render_template('home2.html', 
                          tem=tem3,
                          jour=nomlyouma,
                          hours=hour,
                          pers=perces3,
                          precipitation=preci3,
                          speed=speed3,
                          humidity=humidity3,
                          dateLyouma=dateLyouma,
                          infos=infos, 
                          current_hour=current_hour, 
                          statue = action,
                          hoursforbonne=hoursforbonne)







print(float(infos[0]['temperature']))
print(float(infos[0]['cloud_cover']))
print(float(infos[0]['wind_speed_80m']))
print(float(infos[0]['temperature']))

#this line is for creat the data  base:
from my_prejet import app, db
# Create an application context
with app.app_context():
    # Create the database tables
    db.create_all"""