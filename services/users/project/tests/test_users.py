# services/users/project/tests/test_users.py

from project import db
from project.api.models import User

import json
import unittest

from project.tests.base import BaseTestCase

def add_book(titulo, autor, añodepublicacion, editorial, generoliterario):
    user = User(titulo=titulo, autor=autor, añodepublicacion=añodepublicacion, editorial=editorial, generoliterario=generoliterario)
    db.session.add(user)
    db.session.commit()
    return user

class TestUserService(BaseTestCase):
    """Prueba para el servicio users."""

    def test_users(self):
        """Asegurando que la ruta /ping se comporta correctamente."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Asegurando de que se pueda agregar un nuevo usuario a la base de datos."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'titulo': 'Mil caeran',
                    'autor': 'Susi',
                    'añodepublicacion': '1990',
                    'editorial': 'Ni idea',
                    'generoliterario': 'Accion'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('Mil caeran ha sido agregado!', data['mensaje'])
            self.assertIn('satisfactorio', data['estado'])

    def test_add_user_invalid_json(self):
        """Asegurando de que se arroje un error si el objeto json esta vacio."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Datos no validos.', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_add_user_invalid_json_keys(self):
        """
        Asegurando de que se produce un error si el objeto JSON no tiene
        un key de nombre de usuario.
        """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'titulo': 'Mil caeran'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Datos no validos.', data['mensaje'])
            self.assertIn('fallo', data['estado'])


    def test_add_user_duplicate_book(self):
        """Asegurando de que se produce un error si el libro ya existe."""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'libro': 'Mil caeran',
                    'autor': 'Susi',
                    'añodepublicacion': '1990',
                    'editorial': 'Ni idea',
                    'generoliterario': 'Accion'
                  
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'libro': 'Mil caeran',
                    'autor': 'Susi',
                    'añodepublicacion': '1990',
                    'editorial': 'Ni idea',
                    'generoliterario': 'Accion'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Datos no validos.', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_single_user(self):
        """Asegurando de que el usuario individual se comporte correctamente."""
        #user = User(username='abel', email='abel.huanca@upeu.edu.pe')
        #db.session.add(user)
        #db.session.commit()
        user = add_book('Mil caeran', 'Susi', '1990', 'Ni idea', 'Accion')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Mil caeran', data['data']['titulo'])
            self.assertIn('Susi', data['data']['autor'])
            self.assertIn('1990', data['data']['añodepublicacion'])
            self.assertIn('Ni idea', data['data']['editorial'])
            self.assertIn('Accion', data['data']['generoliterario'])
            self.assertIn('satisfactorio', data['estado'])

    def test_single_user_no_id(self):
        """Asegurando de que se lanze un error si no se proporciona un id."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Libro no existe', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_single_user_incorrect_id(self):
        """Asegurando de que se lanze un error si el id no existe."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Libro no existe', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_all_users(self):
        """ Asegurando de que todos los usuarios se comporten correctamente."""
        add_book('Mil caeran', 'Susi', '1990', 'Ni idea', 'Accion')
        add_book('La casa verde', 'Mario', '1966', 'Six Barral', 'Ficcion')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('Mil caeran', data['data']['users'][0]['titulo'])
            self.assertIn('Susi', data['data']['users'][0]['autor'])
            self.assertIn('1990', data['data']['users'][0]['añodepublicacion'])
            self.assertIn('Ni idea', data['data']['users'][0]['editorial'])
            self.assertIn('Accion', data['data']['users'][0]['generoliterario'])
            self.assertIn('La casa verde', data['data']['users'][1]['titulo'])
            self.assertIn('Mario', data['data']['users'][1]['autor'])
            self.assertIn('1966', data['data']['users'][1]['añodepublicacion'])
            self.assertIn('Six Barral', data['data']['users'][1]['editorial'])
            self.assertIn('Ficcion', data['data']['users'][1]['generoliterario'])
            self.assertIn('satisfactorio', data['estado'])

if __name__ == '__main__':
    unittest.main()