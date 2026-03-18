"""Tests for signup endpoint (POST /activities/{activity_name}/signup)"""


def test_signup_new_student_successful(client):
    """Test successful signup for new student
    
    AAA Pattern:
    - Arrange: New student email, activity name
    - Act: POST signup request
    - Assert: Verify 200 response and participant added
    """
    # Arrange
    new_email = "newstudent@mergington.edu"
    activity_name = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    
    # Verify participant was actually added
    activities_response = client.get("/activities")
    assert new_email in activities_response.json()[activity_name]["participants"]


def test_signup_duplicate_student_returns_400(client):
    """Test that duplicate signup is rejected
    
    AAA Pattern:
    - Arrange: Student already signed up (use existing participant)
    - Act: Attempt to signup same student again
    - Assert: Verify 400 error
    """
    # Arrange
    existing_email = "michael@mergington.edu"  # Already in Chess Club
    activity_name = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_activity_not_found_returns_404(client):
    """Test signup to non-existent activity
    
    AAA Pattern:
    - Arrange: Non-existent activity name
    - Act: POST signup request
    - Assert: Verify 404 error
    """
    # Arrange
    email = "student@mergington.edu"
    fake_activity = "Fake Activity"
    
    # Act
    response = client.post(
        f"/activities/{fake_activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_multiple_students_different_activities(client):
    """Test multiple students signing up for different activities
    
    AAA Pattern:
    - Arrange: Two emails and two activities
    - Act: Register each student for each activity
    - Assert: Verify all registrations successful
    """
    # Arrange
    student1 = "student1@mergington.edu"
    student2 = "student2@mergington.edu"
    activity1 = "Chess Club"
    activity2 = "Programming Class"
    
    # Act
    response1 = client.post(
        f"/activities/{activity1}/signup",
        params={"email": student1}
    )
    response2 = client.post(
        f"/activities/{activity2}/signup",
        params={"email": student2}
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert student1 in activities[activity1]["participants"]
    assert student2 in activities[activity2]["participants"]
