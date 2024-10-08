import json

import requests
from paths import json_schema_file
from jsonschema import validate


def test_get_users_list_pagination(base_url):
    url = base_url + '/api/users'

    response = requests.get(url, params = {'page': '2'})

    assert response.status_code == 200
    assert response.json()['page'] == 2


def test_get_user_by_id(base_url):
    url = base_url + '/api/users/2'

    response = requests.get(url)
    body_json = response.json()

    assert response.status_code == 200
    with open(json_schema_file('one_user_schema.json')) as file:
        schema = json.loads(file.read())
        validate(body_json, schema)


def test_get_list_of_users_schema_validation(base_url):
    url = base_url + '/api/users'

    response = requests.get(url, data = {'page': 1})
    body_json = response.json()

    assert response.status_code == 200
    with open(json_schema_file('users_schema.json')) as file:
        schema = json.loads(file.read())
        validate(body_json, schema)


def test_create_user(base_url):
    url = base_url + '/api/users'
    name = 'John Doe'
    job = 'Tester'

    body = {
        "name": name,
        "job": job
    }

    response = requests.post(url, json = body)
    body_json = response.json()

    assert response.status_code == 201
    with open(json_schema_file('created_user_schema.json')) as file:
        schema = json.loads(file.read())
        validate(body_json, schema)
    assert body_json['name'] == name
    assert body_json['job'] == job


def test_register_user(base_url):
    url = base_url + '/api/register'
    email = 'eve.holt@reqres.in'
    password = 'pistol'

    body = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json = body)
    body_json = response.json()

    assert response.status_code == 200
    with open(json_schema_file('complete_registration_schema.json')) as file:
        schema = json.loads(file.read())
        validate(body_json, schema)


def test_negative_get_user_with_incorrect_id(base_url):
    url = base_url + '/api/users/boss'

    response = requests.get(url)

    assert response.status_code == 404
    assert response.json() == {}


def test_negative_login_without_password(base_url):
    url = base_url + '/api/login'
    email = 'eve.holt@reqres.in'

    body = {
        "email": email
    }
    response = requests.post(url, json = body)
    body_json = response.json()

    assert response.status_code == 400
    assert body_json['error'] == 'Missing password'


def test_negative_login_without_email(base_url):
    url = base_url + '/api/login'
    password = '1234'

    body = {
        "password": password
    }
    response = requests.post(url, json = body)
    body_json = response.json()

    assert response.status_code == 400
    assert body_json['error'] == 'Missing email or username'


def test_create_and_update_user_flow(base_url):
    url = base_url + '/api/users'
    name = 'Johny Doe'
    job = 'qa engineer'
    new_job = 'Automation Tester'

    response = requests.post(url, json = {"name": name, "job": job})
    user_id = response.json()['id']

    body = {
        "name": name,
        "job": new_job
    }

    response = requests.put(url + f'/{user_id}', json = body)
    body_json = response.json()

    assert response.status_code == 200
    with open(json_schema_file('update_user_schema.json')) as file:
        schema = json.loads(file.read())
        validate(body_json, schema)
    assert body_json['name'] == name
    assert body_json['job'] == new_job


def test_negative_create_user_and_delete_and_patch_deleted_user(base_url):
    url = base_url + '/api/users'
    name = 'Johny Doe'
    job = 'qa engineer'
    new_job = 'Automation Tester'

    response = requests.post(url, json = {"name": name, "job": job})
    user_id = response.json()['id']

    body = {
        "name": name,
        "job": new_job
    }

    response = requests.delete(url + f'/{user_id}', json = body)
    assert response.status_code == 204

    response = requests.patch(url + f'/{user_id}', json = body)
    body_json = response.json()

    assert response.status_code == 200
    with open(json_schema_file('update_user_schema.json')) as file:
        schema = json.loads(file.read())
        validate(body_json, schema)
    assert body_json['name'] == name
    assert body_json['job'] == new_job


def test_create_and_delete_user_flow(base_url):
    url = base_url + '/api/users'
    name = 'Johny Doe'
    job = 'Tester'

    response = requests.post(url, json = {"name": name, "job": job})
    user_id = response.json()['id']

    response = requests.delete(f'https://reqres.in/api/users/{user_id}')

    assert response.status_code == 204
