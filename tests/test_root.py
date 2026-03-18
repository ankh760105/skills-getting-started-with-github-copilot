"""Tests for root endpoint (GET /)"""


def test_root_redirects_to_index(client):
    """Test root endpoint redirects to static index
    
    AAA Pattern:
    - Arrange: Client ready, expect redirect
    - Act: GET / request (follow_redirects=False to see the redirect)
    - Assert: Verify 307 redirect to /static/index.html
    """
    # Arrange
    expected_redirect_url = "/static/index.html"
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_redirect_url
