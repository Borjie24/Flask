import pytest
from unittest.mock import patch
from flask import Flask
from src.setup_db_example.models.m_operation_information import OperationInformationDb
from src.operation_information import operation_information_router

@pytest.fixture
def app():
    """Create a test app."""
    app = Flask(__name__)
    app.register_blueprint(operation_information_router)
    return app

def test_get_coordinates_success(client, mocker):
    """Test get_coordinates with valid data."""
    # Mocking database query result
    mock_data = [
        OperationInformationDb(
            process_id=1,
            process_name="Test Process",
            operation_status=1,
            product_number=100,
            facility_cycle_time=10.5,
            coordinates=type(
                "Coordinates", 
                (object,), 
                {"x_position": 10, "y_position": 20, "width": 30, "height": 40}
            )()
        ),
    ]
    
    mocker.patch(
        "src.setup_db_example.models.m_operation_information.OperationInformationDb.query.all",
        return_value=mock_data
    )
    
    # Call the API
    response = client.get("/api/get-coordinates")
    
    # Verify the response
    assert response.status_code == 200
    data = response.json
    assert data["success"] is True
    assert data["message_response"] == "COORDINATES FETCHED SUCCESSFULLY"
    assert len(data["data"]) == 1
    assert data["data"][0]["process_id"] == 1
    assert data["data"][0]["x"] == 10
    assert data["data"][0]["y"] == 20
    assert data["data"][0]["width"] == 30
    assert data["data"][0]["height"] == 40

def test_get_coordinates_failure(client, mocker):
    """Test get_coordinates with database error."""
    # Mock database query to raise an exception
    mocker.patch(
        "src.setup_db_example.models.m_operation_information.OperationInformationDb.query.all",
        side_effect=Exception("Database error")
    )
    
    # Call the API
    response = client.get("/api/get-coordinates")
    
    # Verify the response
    assert response.status_code == 500
    data = response.json
    assert data["success"] is False
    assert data["message_response"] == "FAILED TO FETCH COORDINATES"
    assert "Database error" in data["message_content"]
