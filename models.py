
from flask_sqlalchemy import SQLAlchemy
import os
db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    #db.create_all() -- required to create tables in Heroku and then commented out
# One to many relationship of Movie table with Actors table 
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.Date)
    actors = db.relationship('Actor', backref='movies', lazy='dynamic')

    def __init__(self, title, release_date):
        """initialize with name."""
        self.title = title
        self.release_date = release_date
    
    def __repr__(self):
        return "Movie(%s, %s, %s)" % (self.id, self.title,self.release_date)

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date       
        }
    
    
class Actor(db.Model):
    __tablename__ = 'actors' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    def __init__(self, name, age, gender, movie_id):
        """initialize with name."""
        self.name = name
        self.age = age
        self.gender = gender
        self.movie_id = movie_id
    
    def __repr__(self):
        return "Actor(%s, %s, %s, %s, %s)" % (self.id, self.name,self.age, self.gender, self.movie_id)

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movie_id': self.movie_id
        }

    

    