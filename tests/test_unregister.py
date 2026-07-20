from copy import deepcopy

from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    original_activities = deepcopy(activities)
    activity_name = "Chess Club"
    encoded_activity_name = "Chess%20Club"
    email = "teststudent@example.com"

    try:
        # Act
        signup_response = client.post(
            f"/activities/{encoded_activity_name}/signup?email={email}"
        )
        unregister_response = client.delete(
            f"/activities/{encoded_activity_name}/unregister?email={email}"
        )

        # Assert
        assert signup_response.status_code == 200
        assert unregister_response.status_code == 200
        assert email not in activities[activity_name]["participants"]
    finally:
        # Cleanup
        activities.clear()
        activities.update(deepcopy(original_activities))
