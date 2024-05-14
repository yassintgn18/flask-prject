from flask import Flask, render_template
from models import db, WeatherForecast


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'  # Nom de la base de données SQLite
db.init_app(app)
