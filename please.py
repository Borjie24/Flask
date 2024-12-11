from src.setup_db_example.models.m_operation_information import OperationInformationDb
from src.setup_db_example.schemas.s_operation_information import OperationInformationSchema
from flask import Blueprint
import traceback

operation_information_router = Blueprint("a_operation_", __name__)

@operation_information_router.route("/api/get-coordinates", methods=["GET"])
def get_coordinates():
    """Fetch all the coordinates.

    Returns:
        dict: API response.
    """
    try:
        # Query all operation information records
        process = OperationInformationDb.query.all()

        # Serialize the ORM objects to dictionaries
        schema = OperationInformationSchema(many=True)
        serialized_data = schema.dump(process)

        # Construct the desired response structure
        operation_data = []
        for data in serialized_data:
            coordinates = data.get("coordinates")
            operation_data_dict = {
                "process_id": data.get("process_id"),
                "operation_status": data.get("operation_status"),
                "x": coordinates.get("x_position") if coordinates else None,
                "y": coordinates.get("y_position") if coordinates else None,
                "width": coordinates.get("width") if coordinates else None,
                "height": coordinates.get("height") if coordinates else None,
            }
            operation_data.append(operation_data_dict)

        return {
            "success": True,
            "message_response": "COORDINATES FETCHED SUCCESSFULLY",
            "message_content": "COORDINATES fetched successfully",
            "data": operation_data,
        }, 200

    except Exception as e:
        traceback.print_exc()
        return {
            "success": False,
            "message_response": "FAILED TO FETCH COORDINATES",
            "message_content": str(e),
        }, 500
