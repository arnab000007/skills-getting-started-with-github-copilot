def test_get_activities_returns_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert payload


def test_get_activities_has_expected_fields(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()

    for details in payload.values():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)
