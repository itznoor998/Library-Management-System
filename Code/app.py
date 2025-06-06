from flask import Flask,render_template,request,redirect
import time,jinja2
from flask_sqlalchemy import SQLAlchemy

from routes import *



app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.sqlite3"

db.init_app(app)

app.app_context().push()



if __name__ == "__main__" :
    app.run(debug=True,port=8000)