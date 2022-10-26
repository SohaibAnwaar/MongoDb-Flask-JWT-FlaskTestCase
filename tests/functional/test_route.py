


import json
from flask import Flask
from main import app


def test_flask():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app =  app


    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
       
def test_registration():
    flask_app =  app


    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        data = {
            "username":"test1",
            "password":"1234"
        }
        response = test_client.post('/api/v1/users', data=json.dumps(data), headers={"Content-Type": "application/json"})
        assert response.status_code == 201 or response.status_code == 409

def test_login():
    flask_app =  app


    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        data = {
            "username":"test1",
            "password":"1234"
        }
        response = test_client.post('/api/v1/login', data=json.dumps(data), headers={"Content-Type": "application/json"})
        assert response.status_code == 200