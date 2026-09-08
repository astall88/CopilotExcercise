def test_remove_deletes_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Removed {email} from {activity}"
    }
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_remove_rejects_unknown_activity(client):
    # Arrange
    activity = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_rejects_unknown_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "not.registered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Student is not signed up for this activity"
    )


def test_remove_requires_email(client):
    # Arrange
    activity = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity}/signup")

    # Assert
    assert response.status_code == 422
