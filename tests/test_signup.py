from src.app import activities


def test_signup_success_adds_normalized_email(client):
    response = client.post("/activities/Chess Club/signup?email=NewStudent@Mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up newstudent@mergington.edu for Chess Club"
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_rejects_duplicate_email_case_insensitive(client):
    first = client.post("/activities/Chess Club/signup?email=Duplicate@Mergington.edu")
    second = client.post("/activities/Chess Club/signup?email=duplicate@mergington.edu")

    assert first.status_code == 200
    assert second.status_code == 409
    assert "already signed up" in second.json()["detail"]


def test_signup_unknown_activity_returns_not_found(client):
    response = client.post("/activities/Unknown Club/signup?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_when_activity_is_full(client):
    activity_name = "Chess Club"
    max_participants = activities[activity_name]["max_participants"]

    while len(activities[activity_name]["participants"]) < max_participants:
        next_index = len(activities[activity_name]["participants"]) + 1
        activities[activity_name]["participants"].append(f"fill{next_index}@mergington.edu")

    response = client.post(f"/activities/{activity_name}/signup?email=lastspot@mergington.edu")

    assert response.status_code == 409
    assert response.json()["detail"] == f"{activity_name} is already full"
