import boto3
from decimal import Decimal


class BaseDDBClient:
    """Base client for DynamoDB operations.

    This class provides common functionality for DynamoDB operations.
    """

    def __init__(self, table_name: str, region: str = "us-east-1"):
        """Initialize the DDB client with a table name.

        Args:
            table_name: The name of the DynamoDB table
            region: AWS region for the DynamoDB table
        """
        self.dynamodb = boto3.resource("dynamodb", region_name=region)
        self.table = self.dynamodb.Table(table_name)

    def sanitize_for_dynamodb(self, data):
        """
        Recursively sanitize data for DynamoDB by converting Pydantic models to dicts
        and floats to Decimal.
        """
        # Handle None
        if data is None:
            return None

        # Handle Pydantic models
        if hasattr(data, "model_dump"):
            print(f"Converting Pydantic model to dict: {type(data)}")
            return self.sanitize_for_dynamodb(data.model_dump())

        # Handle float values - convert to Decimal for DynamoDB
        if isinstance(data, float):
            return Decimal(str(data))

        # Handle lists and tuples
        if isinstance(data, (list, tuple)):
            return [self.sanitize_for_dynamodb(item) for item in data]

        # Handle dictionaries
        if isinstance(data, dict):
            return {
                key: self.sanitize_for_dynamodb(value) for key, value in data.items()
            }

        # Return other data types as is
        return data

    def sanitize_from_dynamodb(self, data):
        """
        Recursively convert data from DynamoDB format to JSON-serializable format.
        Mainly converts Decimal back to float.
        """
        # Handle None
        if data is None:
            return None

        # Handle Decimal values - convert back to float for JSON compatibility
        if isinstance(data, Decimal):
            return float(data)

        # Handle lists and tuples
        if isinstance(data, (list, tuple)):
            return [self.sanitize_from_dynamodb(item) for item in data]

        # Handle dictionaries
        if isinstance(data, dict):
            return {
                key: self.sanitize_from_dynamodb(value) for key, value in data.items()
            }

        # Return other data types as is
        return data
