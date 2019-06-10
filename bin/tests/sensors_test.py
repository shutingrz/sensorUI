import unittest
import os,sys
import json
from flask import Flask
import subprocess
import app as sensors_app
app = sensors_app.create_app()


class TestSensorsAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

        #ここなんとかしたい・・・
        db_name = os.path.basename(app.config['SQLALCHEMY_DATABASE_URI'])
        result = subprocess.run(["/bin/bash", "-c", "../scripts/init.sh %s" % db_name])
        print(result)

        

    def test_health(self):
        rv = self.app.get("/api/")
        print(rv.data)

if __name__ == '__main__':
    unittest.main()