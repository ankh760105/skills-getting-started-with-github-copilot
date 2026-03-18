"""Tests for unregister endpoint (DELETE /activities/{activity_name}/unregister)"""


def test_unregister_student_successful(client):
    """Test successful student unregistration
    
    AAA Pattern:
    - Arrange: Get participant count before, student to remove
    - Act: DELETE unregister request
    - Assert: Verify 200 response and participant removed
    """
    # Arrange
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    
    # Get initial count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    
    # Verify participant was actually removed
    final_response = client.get("/activities")
    final_count = len(final_response.json()[activity_name]["participants"])
    assert final_count == initial_count - 1
    assert email not in final_response.json()[activity_name]["participants"]


def test_unregister_not_signed_up_returns_400(client):
    """Test unregister of student not signed up
    
    AAA Pattern:
    - Arrange: Student not in activity participants
    - Act: DELETE unregister request
    - Assert: Verify 400 error
    """
    # Arrange
    email = "notstudent@mergington.edu"
    activity_name = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"].lower()


def test_unregister_activity_not_found_returns_404(client):
    """Test unregister from non-existent activity
    
    AAA Pattern:
    - Arrange: Non-existent activity name
    - Act: DELETE unregister request
    - Assert: Verify 404 error
    """
    # Arrange
    email = "student@mergington.edu"
    fake_activity = "Fake Activity"
    
    # Act
    response = client.delete(
        f"/activities/{fake_activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_then_unregister_cycle(client):
    """Test signup followed by unregister
    
    AAA Pattern:
    - Arrange: New student, activity
    - Act: Sign up, then unregister
    - Assert: Verify both operations succeed
    """
    # Arrange
    email = "cycletest@mergington.edu"
    activity_name = "Chess Club"
    
    # Act - Sign up
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Act - Unregister
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    
    # Verify not in activities
    final_response = client.get("/activities")
    assert email not in final_response.json()[activity_name]["participants"]
