import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie, db
import datetime



class CastingTestCase(unittest.TestCase):

    def setUp(self):
        '''define test variables and initialize app'''

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)
        db.create_all()

        self.new_movie = {
            'title': 'The Platform',
            'release_date' : datetime.date(2020, 4, 20),
        }

        self.new_actor = {
            'name': 'Postman',
            'age': 32,
            'gender': 'M',
            'movie_id': 7
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            #self.db.create_all()
    
    def tearDown(self):
        pass

    def test_get_all_movies(self):
        response = self.client().get('/movies')
        self.assertEqual(response.status_code, 200)

    def test_get_all_movies_fail(self):
        response = self.client().get('/moviesfail')
        self.assertEqual(response.status_code, 404)

    def test_get_all_actors(self):
        response = self.client().get('/actors')
        self.assertEqual(response.status_code, 200)

    def test_get_all_actors_fail(self):
        response = self.client().get('/actorsfail')
        self.assertEqual(response.status_code, 404)

    def test_create_movie(self):
        response = self.client().post('/movies', json=self.new_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actor(self):
        response = self.client().post('/actors', json=self.new_actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
       
    def test_patch_movie(self):
        response = self.client().patch('/movies/7', json=self.new_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_patch_movie_fail(self):
        response = self.client().patch('/movies/2000', json=self.new_movie)
        self.assertEqual(response.status_code, 404)

    
    def test_patch_actor(self):
        response = self.client().patch('/actors/4', json=self.new_actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_patch_actor_fail(self):
        response = self.client().patch('/actors/patch/2000', json=self.new_actor)
        self.assertEqual(response.status_code, 404)

    def test_delete_movie(self):
        response = self.client().delete('/movies/7')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_delete_movie_fail(self):
        response = self.client().delete('/movies/1000')
        self.assertEqual(response.status_code, 404)
    
    def test_delete_actor(self):
        response = self.client().delete('/actors/4')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_delete_actor_fail(self):
        response = self.client().delete('/actors/1000')
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
