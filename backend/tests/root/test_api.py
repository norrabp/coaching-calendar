
def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['components']['database'] == 'connected'
    assert response.json['components']['redis'] == 'connected'
    assert response.json['status'] == 'healthy'

def test_get_users_unauthorized(client):
    response = client.get('/api/users')
    assert response.status_code == 401

def test_get_users_authorized(client, student_auth_headers, test_student):
    response = client.get('/api/users', headers=student_auth_headers)
    assert response.status_code == 200
    assert 'has_next_page' in response.json
    users = response.json['users']
    assert isinstance(users, list)
    assert len(users) > 0
    assert test_student.username in [user['username'] for user in users]
    assert test_student.email in [user['email'] for user in users]

def test_auth_header_missing(client):
    response = client.get('/api/users')
    assert response.status_code == 401

def test_auth_header_invalid(client):
    headers = {'Authorization': 'Bearer invalid-token'}
    response = client.get('/api/users', headers=headers)
    assert response.status_code == 401
