import requests


def test_login_positive():
    API_ENDPOINT = "http://127.0.0.1:5000/login_action"
    data = {'username': 'user1',
            'password': 'abc123'}

    res = requests.post(url=API_ENDPOINT, data=data)

    assert res.status_code == 200


def test_login_negative():
    API_ENDPOINT = "http://127.0.0.1:5000/login_action"
    data = {'username': 'incorrect',
            'password': 'incorrect'}

    res = requests.post(url=API_ENDPOINT, data=data)

    assert res.status_code != 200
