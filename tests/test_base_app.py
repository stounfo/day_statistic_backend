def test_bass_app(client):
    response = client.get(f"/")
    assert response.status_code == 200
