import os
import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from app import create_app

from models import setup_db, Actors, Movies
from auth import AuthError, requires_auth

assistant_token = os.environ.get('ASSISTANT')
director_token = os.environ.get('DIRECTOR')


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

        self.cur_movie = Movies(title='Rocky 14', releasedate='11-06-2020')
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

    def tearDown(self):
        """Executed after each test"""
        self.db.session.remove()
        self.db.drop_all()

    def test_get_actors(self):
        res = self.client().get(
            '/actors', headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)

    def test_get_movies(self):
        res = self.client().get(
            '/movies', headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    def test_404_get_actors_by_id(self):

        res = self.client().get(
            '/actors/100', headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource Not Found')

    def test_404_get_movies_by_id(self):

        res = self.client().get(
            '/movies/100', headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource Not Found')

    def test_delete_actors(self):
        res = self.client().delete(
            f'/actors/{self.cur_actor.id}', headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_actor_id'], self.cur_actor.id)

    def test_create_actors(self):

        res = self.client().post(
            '/actors', json=self.new_actor,
            headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_create_actors_not_allowed(self):
        res = self.client().post(
            '/actors', json=self.new_actor,
            headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue(data['code'], 'invalid permission')

    def test_delete_movies(self):
        res = self.client().delete(
            f'/movies/{self.cur_movie.id}', headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_movie_id'], self.cur_movie.id)

    def test_create_movies(self):

        res = self.client().post(
            '/movies', json=self.new_movie,
            headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_create_movies_not_allowed(self):

        res = self.client().post(
            '/movies', json=self.new_movie,
            headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_permissions')

    def test_update_actors(self):

        res = self.client().patch(f'/actors/{self.cur_actor.id}', json=self.update_actor, headers={
            'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_update_actors(self):

        res = self.client().patch(
            '/actors/100', json=self.update_actor,
            headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource Not Found')

    def test_update_movies(self):

        res = self.client().patch(f'/movies/{self.cur_movie.id}', json=self.update_movie, headers={
            'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_update_movies(self):

        res = self.client().patch(
            '/movies/100', json=self.update_movie,
            headers={'Authorization': f'Bearer {director_token}'})
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
