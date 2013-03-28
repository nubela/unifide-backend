import unittest
from flask import Flask
from unifide_backend.unifide import app, get_app

class TestBase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True
        self.app.config['SERVER_NAME'] = '0.0.0.0:5000'
        self.client = app.test_client()


    def tearDown(self):
        pass