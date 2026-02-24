"""AAA-pattern tests for src/app.py endpoints.

These tests use FastAPI's TestClient and the `client` fixture from conftest.
"""


def test_get_activities_returns_expected_structure(client):
    # Arrange: client fixture

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    sample = data["Chess Club"]
    assert all(k in sample for k in ("description", "schedule", "max_participants", "participants"))


def test_signup_success_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "pytest-new@example.com"
    assert email not in client.get("/activities").json()[activity]["participants"]

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]
    assert "Signed up" in resp.json().get("message", "")


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity = "Chess Club"
    existing = client.get("/activities").json()[activity]["participants"][0]

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": existing})

    # Assert
    assert resp.status_code == 400
    assert resp.json().get("detail") == "Student already signed up for this activity"


def test_signup_nonexistent_activity_returns_404(client):
    # Arrange
    activity = "NoSuchActivity"
    email = "user@example.com"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Activity not found"


def test_unregister_existing_removes_participant(client):
    # Arrange
    activity = "Basketball Team"
    email = "to-remove@example.com"
    # Ensure presence
    signup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert signup.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # Act
    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]
    assert "Removed" in resp.json().get("message", "")


def test_unregister_nonexistent_participant_returns_404(client):
    # Arrange
    activity = "Chess Club"
    email = "not-in-list@example.com"

    # Act
    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Student not found in activity"


def test_unregister_activity_not_found_returns_404(client):
    # Arrange
    activity = "NoActivity"
    email = "user@example.com"

    # Act
    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Activity not found"
