"""Tests for activities listing endpoint (GET /activities)"""


def test_get_activities_returns_all_activities(client):
    """Test retrieving all activities
    
    AAA Pattern:
    - Arrange: Client is ready (via fixture)
    - Act: Make GET request to /activities
    - Assert: Verify response contains all activities with correct structure
    """
    # Arrange
    # (activities already loaded by reset_activities fixture)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
    assert "Chess Club" in activities
    assert "Programming Class" in activities


def test_get_activities_has_correct_structure(client):
    """Test that each activity has required fields
    
    AAA Pattern:
    - Arrange: Client ready, define required fields
    - Act: Fetch activities
    - Assert: Verify each activity has required fields
    """
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data, dict)
        assert required_fields.issubset(activity_data.keys())
        assert isinstance(activity_data["participants"], list)
        assert isinstance(activity_data["max_participants"], int)


def test_get_activities_participant_count_matches(client):
    """Test that participant count is accurate
    
    AAA Pattern:
    - Arrange: Know that Chess Club has 2 participants initially
    - Act: Get activities
    - Assert: Verify participant count matches
    """
    # Arrange
    expected_chess_participants = 2
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert len(activities["Chess Club"]["participants"]) == expected_chess_participants
