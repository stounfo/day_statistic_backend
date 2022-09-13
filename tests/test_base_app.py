def test_bass_app(client):
    response = client.get("/")
    assert response.status_code == 200
