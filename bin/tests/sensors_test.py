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

        #login
        rv = self.app.get("/api/login", query_string=dict(
            username=testuser_data["name"],
            password=testuser_data["password"]
        ))
        json_data = rv.get_json()
        assert json_data["header"]["status"] == "success"


    def test_auth_test(self):

        testuser_data = {"name": "test_auth_test", "password": "testtest"}

        #access login required page without session
        rv = self.app.get("/api/account/status")
        assert rv.status_code == 401

        #register
        rv = self.app.get("/api/register/user", query_string=dict(
            username=testuser_data["name"],
            password=testuser_data["password"]
        ))
        json_data = rv.get_json()
        assert json_data["header"]["status"] == "success"

        #login
        rv = self.app.get("/api/login", query_string=dict(
            username=testuser_data["name"],
            password=testuser_data["password"]
        ))
        json_data = rv.get_json()
        assert json_data["header"]["status"] == "success"

        session = rv.headers["Set-Cookie"]
        assert "session" in session

        #access login required page with session
        rv = self.app.get("/api/account/status", headers={"Cookie": session})
        assert rv.status_code == 200

        json_data = rv.get_json()
        assert json_data["header"]["status"] == "success"



class TestAccountControl(unittest.TestCase):

    testuser_data = {"name": "test_account_control", "password": "testtest"}
    session = None

    def setUp(self):        
        self.app = app.test_client()

        #register
        rv = self.app.get("/api/register/user", query_string=dict(
            username=self.testuser_data["name"],
            password=self.testuser_data["password"]
        ))
        json_data = rv.get_json()
        assert json_data["header"]["status"] == "success"

        #login
        rv = self.app.get("/api/login", query_string=dict(
            username=self.testuser_data["name"],
            password=self.testuser_data["password"]
        ))
        json_data = rv.get_json()
        assert json_data["header"]["status"] == "success"

        self.session = rv.headers["Set-Cookie"]


    def test_device_register(self):
        testdevice_data = {"device_name": "testdev", "sensor_type": "1"}

        rv = self.app.get("/api/register/device", headers={"Cookie": self.session}, query_string=dict(
                            device_name=testdevice_data["device_name"],
                            sensor_type=testdevice_data["sensor_type"]
            ))
        
        json_data = rv.get_json()
        assert json_data["header"]["status"] == "success"


        #get device list
        rv = self.app.get("/api/account/status", headers={"Cookie": self.session})
        assert rv.status_code == 200

        json_data = rv.get_json()
        print(json_data)
        assert json_data["header"]["status"] == "success"
                    
        

    


if __name__ == '__main__':
    unittest.main()