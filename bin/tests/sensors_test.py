import unittest
import os,sys
import json
from flask import Flask
import subprocess
import app as sensors_app
import time

#ここなんとかしたい・・・
dburl = "sqlite:///../sensors.db"
db_name = os.path.basename(dburl)
result = subprocess.run(["/bin/bash", "-c", "../scripts/init.sh %s" % db_name])        
time.sleep(1)


app = sensors_app.create_app()

class TestUserControl(unittest.TestCase):

    def setUp(self):        
        self.app = app.test_client()


    def test_health(self):
        rv = self.app.get("/api/")
        assert b"Sensors" in rv.data
    
    def test_user_isexist(self):
        testuser_data = {"name": "test_user_isexist", "password": "testtest"}

        rv = self.app.get("/api/user/%s/isexist" % testuser_data["name"])
        json_data = rv.get_json()
        assert json_data["header"]["status"] == "success"


    def test_user_register(self):
        testuser_data = {"name": "test_user_register", "password": "testtest"}

        #register
        rv = self.app.get("/api/register/user", query_string=dict(
            username=testuser_data["name"],
            password=testuser_data["password"]
        ))
        json_data = rv.get_json()
        assert json_data["header"]["status"] == "success"

        #isexist
        rv = self.app.get("/api/user/%s/isexist" % testuser_data["name"])
        json_data = rv.get_json()
        assert json_data["response"] == True
        
        #delete
        rv = self.app.get("/api/admin/user/delete/%s" % testuser_data["name"])
        json_data = rv.get_json()

        #isexist
        rv = self.app.get("/api/user/%s/isexist" % testuser_data["name"])
        json_data = rv.get_json()
        assert json_data["response"] == False


    def test_admin_user_delete(self):
        testuser_data = {"name": "test_admin_user_delete", "password": "testtest"}

        #register
        rv = self.app.get("/api/register/user", query_string=dict(
            username=testuser_data["name"],
            password=testuser_data["password"]
        ))
        json_data = rv.get_json()
        assert json_data["header"]["status"] == "success"

        #isexist
        rv = self.app.get("/api/user/%s/isexist" % testuser_data["name"])
        json_data = rv.get_json()
        assert json_data["response"] == True
        
        #delete
        rv = self.app.get("/api/admin/user/delete/%s" % testuser_data["name"])
        json_data = rv.get_json()

        #isexist
        rv = self.app.get("/api/user/%s/isexist" % testuser_data["name"])
        json_data = rv.get_json()
        assert json_data["response"] == False
        

    def test_user_login(self):
        testuser_data = {"name": "test_user_login", "password": "testtest"}

        #register
        rv = self.app.get("/api/register/user", query_string=dict(
            username=testuser_data["name"],
            password=testuser_data["password"]
        ))
        json_data = rv.get_json()
        assert json_data["header"]["status"] == "success"

        rv = self.app.get("/api/login", query_string=dict(
            username=testuser_data["name"],
            password=testuser_data["password"]
        ))
        json_data = rv.get_json()
        assert json_data["header"]["status"] == "success"

    def test_auth_test(self):

        rv = self.app.get("/api/account/status")
        print(rv)




class TestAccountControl(unittest.TestCase):

    def setUp(self):        
        self.app = app.test_client()


    def test_health(self):
        rv = self.app.get("/api/")
        assert b"Sensors" in rv.data
    
    


if __name__ == '__main__':
    unittest.main()