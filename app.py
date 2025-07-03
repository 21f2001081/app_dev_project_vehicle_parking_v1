from flask import Flask, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from applications.models import * 


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecret'
db.init_app(app)
with app.app_context():
    db.create_all()
app.app_context().push()

from applications.routes import *
if __name__ == "__main__":
    app.debug=True
    app.run()