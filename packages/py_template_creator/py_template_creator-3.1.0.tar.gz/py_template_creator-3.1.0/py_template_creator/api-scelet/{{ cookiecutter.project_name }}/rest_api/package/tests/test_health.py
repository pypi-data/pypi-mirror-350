async def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200


async def test_root(client):
    response = client.get("/api")
    assert response.status_code == 200
