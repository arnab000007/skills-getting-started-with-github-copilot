from src.app import activities


def test_unregister_success_removes_participant(client):
    response = client.delete("/activities/Chess Club/participants?email=michael@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_unknown_activity_returns_not_found(client):
    response = client.delete("/activities/Unknown Club/participants?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_not_found(client):
    response = client.delete("/activities/Chess Club/participants?email=notfound@mergington.edu")

    assert response.status_code == 404
    assert "is not signed up" in response.json()["detail"]


def test_unregister_is_case_insensitive(client):
    response = client.delete("/activities/Chess Club/participants?email=MICHAEL@MERGINGTON.EDU")

    assert response.status_code == 200
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
