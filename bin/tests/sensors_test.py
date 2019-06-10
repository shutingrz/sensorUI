import unittest
import json
from flask import Flask

import app as sensors_app
app = sensors_app.create_app()


class TestSensorsAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_health(self):
        rv = self.app.get("/api/")
        print(rv.data)

if __name__ == '__main__':
    unittest.main()