from copy import deepcopy

from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    original_activities = deepcopy(activities)

    try:
        signup_response = client.post(
            "/activities/Chess%20Club/signup?email=teststudent@example.com"
        )
        assert signup_response.status_code == 200

        unregister_response = client.delete(
            "/activities/Chess%20Club/unregister?email=teststudent@example.com"
        )

        assert unregister_response.status_code == 200
        assert "teststudent@example.com" not in activities["Chess Club"]["participants"]
    finally:
        activities.clear()
        activities.update(deepcopy(original_activities))
