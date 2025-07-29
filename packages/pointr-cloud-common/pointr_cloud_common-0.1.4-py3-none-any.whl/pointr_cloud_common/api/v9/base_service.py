from typing import Dict, Any, Optional
import logging


class V9ApiError(Exception):
    """Exception raised for V9 API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response_text: Optional[str] = None):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(message)


class BaseApiService:
    """Base class for all V9 API services."""
    
    def __init__(self, api_service):
        """
        Initialize the base API service.
        
        Args:
            api_service: The parent V9ApiService instance
        """
        self.api_service = api_service
        self.base_url = api_service.base_url
        self.client_id = api_service.client_id
        self.user_email = api_service.user_email
        self.token = api_service.token
        self.logger = logging.getLogger(__name__)
        
    def _make_request(self, method: str, endpoint: str, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a request to the V9 API.
        
        Args:
            method: The HTTP method to use
            endpoint: The API endpoint to call
            json_data: Optional JSON data to send
            
        Returns:
            The JSON response from the API
        """
        return self.api_service._make_request(method, endpoint, json_data)
