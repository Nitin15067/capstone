
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, db, Actor, Movie, db_drop_and_create_all
from constants import assistant_token, director_token, producer_token

assistant_auth_header = {
    'Authorization': "Bearer " + assistant_token,
    'Content-Type': "application/json"
}

director_auth_header = {
    'Authorization': "Bearer " + director_token,
    'Content-Type': "application/json"
}

producer_auth_header = {
    'Authorization': "Bearer " + producer_token,
    'Content-Type': "application/json"
}

movie = {
    'title': "new movie",
    "release_date": "12/12/2020"
}

actor = {
    "name": "Nitin",
    "age": 24,
    "gender": "male"
}


class testClass(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        db.session.close()
        db.session.remove()
        db_drop_and_create_all()

        newMovie = Movie(title="new Movie", release_date="12/12/12")
        newMovie.insert()

        newActor = Actor(name="new Actor", age=24, gender="male")
        newActor.insert()

    def tearDown(self):
        """Executed after each test"""
        pass

    #  * ----- TESTING  ----- *

    # endpoint get movies success
    # using assistant auth token
    def test_200_get_movies(self):
        res = self.client().get('/movies', headers=assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # endpoint get movies error
    # no token is used
    def test_401_get_movies_without_header(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unauthorized")

    # endpoint post movie success
    # using producer auth token
    def test_200_add_movie(self):
        res = self.client().post(
            '/movies',
            data=json.dumps(movie),
            headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie added successfully')

    # endpoint post movie error
    # using director auth token
    def test_403_add_movie(self):
        res = self.client().post(
            '/movies',
            data=json.dumps(movie),
            headers=director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    # endpoint get movie by id success
    # using producer auth token
    def test_200_get_movie_by_id(self):
        res = self.client().get('/movies/1', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # endpoint get movie by id error
    # using producer auth token
    def test_404_get_movie_by_id(self):
        res = self.client().get('/movies/-1', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    # endpoint patch movie by id success
    # using assistant auth token
    def test_200_patch_movie_details_by_id(self):
        data = {"title": "updated", "release_date": "12/12/2020"}
        res = self.client().patch(
            '/movies/1',
            data=json.dumps(data),
            headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie details updated successfully')

    # endpoint patch movie by id failure
    # using assistant auth token
    def test_404_patch_movie_details_by_id(self):
        data = {"title": "updated", "release_date": "12/12/2020"}
        res = self.client().patch(
            '/movies/1',
            data=json.dumps(data),
            headers=assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    # endpoint delete movie by id success
    # using producer auth token
    def test_200_delete_movie(self):
        res = self.client().delete('/movies/1', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie deleted successfully')

    # endpoint delete movie by id failure
    # using assistant auth token
    def test_403_delete_movie(self):
        res = self.client().delete('/movies/1', headers=assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    # endpoint get actors success
    # using assistant auth token
    def test_200_get_actors(self):
        res = self.client().get('/actors', headers=assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # endpoint get actors error
    # no token is used
    def test_401_get_actors_without_header(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unauthorized")

    # endpoint post actor success
    # using producer auth token
    def test_200_add_actor(self):
        res = self.client().post(
            '/actors',
            data=json.dumps(actor),
            headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor added successfully')

    # endpoint post actor error
    # using director auth token
    def test_403_add_actor(self):
        res = self.client().post(
            '/actors',
            data=json.dumps(actor),
            headers=assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    # endpoint get actor by id success
    # using producer auth token
    def test_200_get_actor_by_id(self):
        res = self.client().get('/actors/1', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # endpoint get actor by id error
    # using producer auth token
    def test_404_get_actor_by_id(self):
        res = self.client().get('/actors/-1', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    # endpoint patch actor by id success
    # using assistant auth token
    def test_200_patch_actor_details_by_id(self):
        data = {"name": "updated", "age": 25, "gender": "female"}
        res = self.client().patch(
            '/actors/1',
            data=json.dumps(data),
            headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor details updated successfully')

    # endpoint patch actor by id failure
    # using assistant auth token
    def test_404_patch_actor_details_by_id(self):
        data = {"title": "updated", "release_date": "12/12/2020"}
        res = self.client().patch(
            '/actors/1',
            data=json.dumps(data),
            headers=assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    # endpoint delete actor by id success
    # using producer auth token
    def test_200_delete_actor(self):
        res = self.client().delete('/actors/1', headers=producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor deleted successfully')

    # endpoint delete actor by id failure
    # using assistant auth token
    def test_403_delete_actor(self):
        res = self.client().delete('/actors/1', headers=assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')


# #  Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
