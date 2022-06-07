from app import app
from db import db

db.init_app(app)

@app.before_first_request #force create all tables specified on Models unless they exist already
def create_tables():
    db.create_all()