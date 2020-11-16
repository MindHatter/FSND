import os
import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from app import create_app

from models import setup_db, Actors, Movies
from auth import AuthError, requires_auth

assistant_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBNaFZqTzk3NTVRbERiN1hseXBLWSJ9.eyJpc3MiOiJodHRwczovL2Rldi1taC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYzNTI5NzQzOGQxYTIwMDZkMjExMDYxIiwiYXVkIjoiaHR0cHM6Ly9sb2NhbGhvc3Q6NTAwMSIsImlhdCI6MTYwNTUxMjE5MiwiZXhwIjoxNjA1NTk4NTkyLCJhenAiOiJqQldDZGwzb040OW1BOFVYMWpWNHJ2TlFaMEl5aU42byIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.PKb2R4VfXVTG4jGQ46ttdTd7WrLQdtuR1WSC8hwP1lX06_GuSmS08U0SuBMjXZ83ijw0oLXpWLoJOs2vJ4XoIzr5Z2MOB9jg3UIzN2KOUHJjNr2RqRmUJoWy1jjN9s_oltC6qCwakxGHLzQ839ZQJkCB8DM0UxHtJnVN4oBOrwTwT__y4ZR-DNOErGb72jMN9_tvBmQrGIfCdXsY4jU5Pq-9ee_JlqK1X27PehrDVGd__frEUDjF_rz12VzTqQ9WNtZJ24qGxcmsn3PtfKME7uwWjQ05HpH4ZsWK2NKWAfVpsWpKh8jCAjjDr8ME7zAgZfXY8-4MVSSX6chF5SPr2w"

director_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBNaFZqTzk3NTVRbERiN1hseXBLWSJ9.eyJpc3MiOiJodHRwczovL2Rldi1taC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTc4MDE0MzMzOTQ2NjEyMzYzNjAiLCJhdWQiOlsiaHR0cHM6Ly9sb2NhbGhvc3Q6NTAwMSIsImh0dHBzOi8vZGV2LW1oLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MDU1MTIxNDEsImV4cCI6MTYwNTU5ODU0MSwiYXpwIjoiakJXQ2RsM29ONDltQThVWDFqVjRydk5RWjBJeWlONm8iLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.BOQV5BA6IoZOSbJUlOwB0PJTMoGQDiWGDqv70i3xjCnXd5v2Uz8g-EIjBYjtROhX6kMT3LRHZP-pCBPi75GzEP2IMCurf73hk_x4siFn5M22hbMkkEllipr_-w1nz3G8YOI6B0yg7DzNyxYAYvvOCpiaJnDFXYpLWoKkupUetj0hSjHK0-JXSSKCdEchqtG7mhBfwYvcFWHRZpYei4gFUPYP28F0jVLZd9Cf2aU7QHJvMJenlzyFFvtXJZUeodVkpRvVp_D9MN4_DyBvpPhBeJIH1uRKQM4hBvGpZVpOWA4kkf5HXYlPzxjP4ylxaw2cp78gY3LXN0a3HRlYhvzoxg"


class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path = "sqlite:///capstone_test.db"
        self.db = setup_db(self.app, self.database_path)

        self.cur_actor = {
            'id': 1,
            'name': 'Aleks',
            'age': 30,
            'gender': 'male'
        }

        self.cur_movie = {
            'id': 1,
            'title': 'Rocky 14',
            'releasedate': '11-06-2020'
        }

        self.cur_actor = Actors(name='Aleks', age=30, gender='male')
        self.cur_actor.insert()

        self.cur_movie= Movies(title='Rocky 14', releasedate='11-06-2020')
        self.cur_movie.insert()

        self.new_actor = {
            'name': 'lithika',
            'age': 10,
            'gender': 'female'
        }

        self.new_movie = {
            'title': 'Frozen II',
            'releasedate': '12-06-2019'
        }

        self.update_actor = {
            'name': 'Sam'
        }

        self.update_movie = {
            'title': 'Cars'
        }

        # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        self.db.session.remove()
        self.db.drop_all()

    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    # def test_get_actor_by_id(self):
    #     res = self.client().get(f'/actors/{self.cur_actor.id}', headers={'Authorization': f'Bearer {assistant_token}'})
    #     data = res.data
    #     print(data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(data['actors']))

    # def test_get_movies_by_id(self):

    #     res = self.client().get('/movies/1', headers={'Authorization': f'Bearer {assistant_token}'})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(len(data['movies']))

    def test_404_get_actors_by_id(self):

        res = self.client().get('/actors/100', headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource Not Found')

    def test_404_get_movies_by_id(self):

        res = self.client().get('/movies/100', headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource Not Found')

    def test_delete_actors(self):
        res = self.client().delete(f'/actors/{self.cur_actor.id}', headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_actor_id'], self.cur_actor.id)

    def test_create_actors(self):

        res = self.client().post('/actors', json=self.new_actor, headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_create_actors_not_allowed(self):
        res = self.client().post('/actors', json=self.new_actor, headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue(data['code'], 'invalid permission')

    def test_delete_movies(self):
        res = self.client().delete(f'/movies/{self.cur_movie.id}', headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_movie_id'], self.cur_movie.id)

    def test_create_movies(self):

        res = self.client().post('/movies', json=self.new_movie, headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_create_movies_not_allowed(self):

        res = self.client().post('/movies', json=self.new_movie, headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_permissions')

    def test_update_actors(self):

        res = self.client().patch(f'/actors/{self.cur_actor.id}', json=self.update_actor, headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_update_actors(self):

        res = self.client().patch('/actors/100', json=self.update_actor, headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource Not Found')

    def test_update_movies(self):

        res = self.client().patch(f'/movies/{self.cur_movie.id}', json=self.update_movie, headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_update_movies(self):

        res = self.client().patch('/movies/100', json=self.update_movie, headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource Not Found')

    def test_401_bad_header(self):

        res = self.client().patch('/movies/100', json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)   


if __name__ == "__main__":
    unittest.main()