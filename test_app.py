
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, db, Actor, Movie, db_drop_and_create_all

assistant_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJpR0JwMFVXZktSOV8ya3JXSC1FYiJ9.eyJpc3MiOiJodHRwczovL25pdGluMTUwNjcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNTMwMjkwMGY5MmJiMDA2OWMwNjE4OCIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjE2NjI1NjI3LCJleHAiOjE2MTY3MTIwMjcsImF6cCI6IjhOZVlWUGZSTGZVVFhiZVdnRFBQVFVSWVJkdXZmN2NxIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.AHIGQV5axaoHS-_ibIly3JP_0oYlWHNNyDMXDKvq4YVPC3YiIYz02yKPB2d27tG5NcAHE5CEdGUdRDQAYpVNeLsznX-1T9IftZ8lfr6BVZh7lhP4gBKXNdfBZw3HOca50UJI_v8C382VSHlze4SklCtMW_fp_QL7o78OtX3SzJoTRZu0aDurya1IXgLcw-l4Wh_5qPRJ1AU7_UOyxtaHjFuMcAurh2Z64hjf4vAX3yZE8i6bo7z3_w5oyJz9DlWLRWBc8GhyMXapvSJjcX_uURtwdJyPlFb5_C13T-RRUVPIgIf8GdeNK_82i8mKnXn7aiCwcR9lI3EoEp2AM7OKuw"
director_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJpR0JwMFVXZktSOV8ya3JXSC1FYiJ9.eyJpc3MiOiJodHRwczovL25pdGluMTUwNjcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNTMwMmNkMGY5MmJiMDA2OWMwNjE5NCIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjE2NjI1MDgwLCJleHAiOjE2MTY3MTE0ODAsImF6cCI6IjhOZVlWUGZSTGZVVFhiZVdnRFBQVFVSWVJkdXZmN2NxIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.IRzPfNAvSr1uto--VwUhz96PQL5l3SvXdr2UUxPTHRt3XW9bt1pLN86wlw-NEtSSLHbsIdkYAFb9VZq3AJiqzRv7IDuIsniWslpeeoSRsHFrgNUXJiBzJRY_35cQmURU7rI0tEw3nQWVDmWcZHE4X1NY53Sq0RkzwKSWDuqely8QtZ_WvM9OWGVeJWCig_g9B2l2q-tgpN1_AC8DKiXW4v9JQf4ZaXqQyYd7hZj657mWiwy5YNnMIdRi2FgLa9zsNnD4RF8uZUlN3H49wJZqWIk_2ydp7lAM9SAQCMRM_URIXOn-BydHsLo9wSc4avA8oMZkRZJDo8zcyxj8mJdVZQ"
producer_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJpR0JwMFVXZktSOV8ya3JXSC1FYiJ9.eyJpc3MiOiJodHRwczovL25pdGluMTUwNjcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNTMwMmY1ODk1ZGEwMDA2N2EzNzYwNiIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjE2NjI1MTE4LCJleHAiOjE2MTY3MTE1MTgsImF6cCI6IjhOZVlWUGZSTGZVVFhiZVdnRFBQVFVSWVJkdXZmN2NxIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.qjCf0zwGcTSwOARWVg9_4XWtvUk9mv_buGmDAD_Ql-mChQjfWQoGBWLW0Ltkx7qITEhD_9bf-0YfuZOT13dUnWU_NN8gL_grs-PV6usRF0YBrEhPjCf_QzUippccHiJM9CVA6wlqdffvaHTedsIbrycUd6nR4Op3C_k-VWhEDSniTEhWcAvzWUp1cMbNA9_kf8DDD-FGJl_tgzxW-TVssJKNekFOgIPsI2yVqhzPcmGM-IjR1MTlnoNjJpqDPAxNsaz6BWzmcVDtL-1dKrO-XpOXgq7kNda9k4abrMLwvOzqeLfSlubrnKroiU80LtwgfyZoTpKrO8U5HAg6pmQzzw"

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
