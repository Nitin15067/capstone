import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth.auth import AuthError, requires_auth

from werkzeug.exceptions import HTTPException, NotFound


def formatActors(actors):
    response = []
    for actor in actors:
        c = actor.format()
        response.append(c)
    return response


def formatMovies(movies):
    response = []
    for movie in movies:
        c = movie.format()
        response.append(c)
    return response


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # Actor api's.
    # Get all actors.
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        return jsonify({
            "success": True,
            "actors": formatActors(actors)
        })

    # # Get a actor using actor id.

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor(payload, actor_id):
        actor = Actor.query.filter_by(id=actor_id).one_or_none()

        if actor is None:
            abort(404)

        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    # Add a new actor.
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        try:
            data = request.get_json()
            actor = Actor(
                name=data.get('name', None),
                age=data.get('age', None),
                gender=data.get('gender', None)
            )

            actor.insert()
            actors = Actor.query.all()
            return jsonify({
                "success": True,
                "message": "Actor added successfully",
                "actors": formatActors(actors)
            })

        except Exception:
            abort(422)

    # Delete an actor.
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        try:
            actor = Actor.query.filter_by(id=actor_id).one_or_none()

            if actor is None:
                raise NotFound()

            actor.delete()

            return jsonify({
                'success': True,
                'message': 'Actor deleted successfully'
            })

        except NotFound as e:
            abort(404)
        except Exception:
            abort(422)

    # Update actor details
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor_details(payload, actor_id):
        try:
            data = request.get_json()
            actor = Actor.query.filter_by(id=actor_id).one_or_none()

            if actor is None:
                raise NotFound()

            actor.name = data.get("name")
            actor.age = data.get("age")
            actor.gender = data.get("gender")

            actor.update()
            actors = Actor.query.all()
            return jsonify({
                'success': True,
                'message': 'Actor details updated successfully',
                'actors': formatActors(actors)
            })

        except NotFound as e:
            abort(404)
        except Exception:
            abort(422)

    # Movie api's.
    # Get all movies.

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        return jsonify({
            "success": True,
            "movies": formatMovies(movies)
        })

    # Get a movie using movie id.
    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie(payload, movie_id):
        movie = Movie.query.filter_by(id=movie_id).one_or_none()

        if movie is None:
            abort(404)

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    # Add a new movie.
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        try:

            data = request.get_json()
            movie = Movie(
                title=data.get('title', None),
                release_date=data.get('release_date', None),
            )
            movie.insert()
            movies = Movie.query.all()
            return jsonify({
                "success": True,
                "message": "Movie added successfully",
                "movies": formatMovies(movies)
            })
        except Exception:
            abort(422)

    # Delete a movie.
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        try:
            movie = Movie.query.filter_by(id=movie_id).one_or_none()

            if movie is None:
                raise NotFound()

            movie.delete()

            return jsonify({
                'success': True,
                'message': 'Movie deleted successfully'
            })

        except NotFound as e:
            abort(404)
        except Exception:
            abort(422)

    # Update movie details
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie_details(payload, movie_id):
        try:
            data = request.get_json()
            movie = Movie.query.filter_by(id=movie_id).one_or_none()

            if movie is None:
                raise NotFound()

            movie.title = data.get("title", None)
            movie.release_date = data.get("release_date", None)

            movie.update()

            movies = Movie.query.all()
            return jsonify({
                'success': True,
                'message': 'Movie details updated successfully',
                "movies": formatMovies(movies)
            })

        except NotFound as e:
            abort(404)
        except Exception:
            abort(422)

    # Error Handlers

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found'
        }), 404

    @app.errorhandler(403)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': 'Permission not found'
        }), 403

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorized'
        }), 401

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'server error'
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
