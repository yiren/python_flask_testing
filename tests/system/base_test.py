from unittest import TestCase
from app import app

class TestBase(TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client