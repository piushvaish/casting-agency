import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import setup_db, Movie, Actor, db
from auth import AuthError, requires_auth


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app, resources={r"/api/": {"origins": "*"}})
  setup_db(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
    return response


  # Setup home route
  @app.route('/')
  def index():
    return "Capstone project - Casting Agency"
    
  # Get all movies and actors
  @app.route('/movies', methods=['GET'])
  @requires_auth('view:movies')
  def get_movies(token):
    movies = Movie.query.all()
    data = [movie.format() for movie in movies]
    if len(data) == 0:
      abort(404)
    return jsonify({
          'success': True,
          'movies':  data         
    }), 200

  @app.route('/actors', methods=['GET'])  
  @requires_auth('view:actors')
  def get_actors(token):
      
    actors = Actor.query.all()
    data = [actor.format() for actor in actors]
    if len(data) == 0:
      abort(404)
    return jsonify({
          'success': True,
          'actors':  data         
    }), 200
      
  # Get a specific movie or actor
  @app.route('/movies/<int:id>', methods=['GET'])
  @requires_auth('view:movies')
  def get_movie_by_id(token, id):
    movie = Movie.query.get(id)
    data = [movie.format()]
    if len(data) == 0:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'movie': data,
        }), 200

  @app.route('/actors/<int:id>', methods=['GET'])
  @requires_auth('view:movies')
  def get_actor_by_id(token, id):
    actor = Actor.query.get(id)
    data = [actor.format()]
    if len(data) == 0:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'actor': data,
        }), 200

  # Post a movie or actor
  @app.route('/movies', methods=['POST']) 
  @requires_auth('post:movies')  
  def post_movie(token):
    data = request.get_json()
    title = data.get('title', None)
    release_date = data.get('release_date', None)

    if title is None or release_date is None:
        abort(400)

    movie = Movie(title=title, release_date=release_date)
    try:
        movie.insert()
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200
    except Exception:
        abort(500)
      
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def post_actor(token):
    data = request.get_json()
    name = data.get('name', None)
    age = data.get('age', None)
    gender = data.get('gender', None)
    movie_id = data.get('movie_id', None)

    actor = Actor(name=name, age=age, gender=gender, movie_id = movie_id)

    if name is None or age is None or gender is None:
        abort(400)

    try:
        actor.insert()
        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200
    except Exception:
        abort(500)

  # PATCH a movie or actor
  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def patch_movie(token, id):        

    data = request.get_json()
    title = data.get('title', None)
    release_date = data.get('release_date', None)

    movie = Movie.query.get(id)

    if movie is None:
        abort(404)

    if title is None or release_date is None:
        abort(400)

    movie.title = title
    movie.release_date = release_date

    try:
        movie.update()
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200
    except Exception:
        abort(500)

  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def patch_actor(token, id):

    data = request.get_json()
    name = data.get('name', None)
    age = data.get('age', None)
    gender = data.get('gender', None)
    movie_id = data.get('movie_id', None)

    actor = Actor.query.get(id)

    if actor is None:
        abort(404)

    if name is None or age is None or gender is None or movie_id is None:
        abort(400)

    actor.name = name
    actor.age = age
    actor.gender = gender
    actor.movie_id = movie_id

    try:
        actor.update()
        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200
    except Exception:
        abort(500)

  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(token, id):
    try:
      movie = Movie.query.get(id)
      if movie is None:
          abort(404)
      else:
          movie.delete()
          
      return jsonify({
        'success': True,
        'deleted movie id': movie.id,
        'deleted movie title': movie.title
      }), 200
    except Exception:
      abort(404)

  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(token, id):
    try:
      actor = Actor.query.get(id)
      if actor is None:
          abort(404)
      else:
          actor.delete()
          
      return jsonify({
        'success': True,
        'deleted actor id': actor.id,
        'deleted actor name': actor.name
      }), 200
    except Exception:
      abort(404)
  
  # Error Handling

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad Request"
      }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Resource Not Found"
      }), 404  

  @app.errorhandler(422)
  def unprocessable_entity(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable"
      }), 422
  
  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          'success': False,
          'error': 500,
          'message': "An error has occured, please try again"
      }), 500

  @app.errorhandler(AuthError)
  def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)