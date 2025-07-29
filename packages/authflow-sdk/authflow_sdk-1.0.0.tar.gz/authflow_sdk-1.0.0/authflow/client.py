import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any, Union


class AuthFlowClient:
    """Official AuthFlow Python SDK client for the AuthFlow API."""

    def __init__(self, api_key: str, base_url: str = "https://api.authflow.com"):
        """
        Initialize the AuthFlow client.

        Args:
            api_key: Your AuthFlow API key
            base_url: The base URL for AuthFlow API (defaults to production)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'AuthFlow-Python-SDK/1.0.0'
        })

    def authenticate_user(self, application_id: int, email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate a user with email and password.

        Args:
            application_id: The ID of the application
            email: User's email
            password: User's password

        Returns:
            Dict containing authentication token and user details
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/authenticate",
                json={
                    "applicationId": application_id,
                    "email": email,
                    "password": password
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error("Failed to authenticate user", e)

    def register_user(self, application_id: int, email: str, password: str, 
                    user_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Register a new user.

        Args:
            application_id: The ID of the application
            email: User's email
            password: User's password
            user_data: Optional additional user data

        Returns:
            Dict containing the created user details
        """
        payload = {
            "applicationId": application_id,
            "email": email,
            "password": password
        }
        
        if user_data:
            payload.update(user_data)
            
        try:
            response = self.session.post(
                f"{self.base_url}/api/register",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error("Failed to register user", e)

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Get user by ID.

        Args:
            user_id: The ID of the user

        Returns:
            Dict containing the user details
        """
        try:
            response = self.session.get(f"{self.base_url}/api/users/{user_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error(f"Failed to get user {user_id}", e)

    def get_application(self, application_id: int) -> Dict[str, Any]:
        """
        Get application by ID.

        Args:
            application_id: The ID of the application

        Returns:
            Dict containing the application details
        """
        try:
            response = self.session.get(f"{self.base_url}/api/applications/{application_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error(f"Failed to get application {application_id}", e)

    def get_applications(self) -> List[Dict[str, Any]]:
        """
        Get all applications.

        Returns:
            List of applications
        """
        try:
            response = self.session.get(f"{self.base_url}/api/applications")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error("Failed to get applications", e)

    def create_application(self, name: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new application.

        Args:
            name: The name of the application
            options: Optional application configuration

        Returns:
            Dict containing the created application details
        """
        payload = {"name": name}
        if options:
            payload.update(options)
            
        try:
            response = self.session.post(
                f"{self.base_url}/api/applications",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error("Failed to create application", e)

    def update_application(self, application_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an application.

        Args:
            application_id: The ID of the application
            updates: The fields to update

        Returns:
            Dict containing the updated application details
        """
        try:
            response = self.session.patch(
                f"{self.base_url}/api/applications/{application_id}",
                json=updates
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error(f"Failed to update application {application_id}", e)

    def delete_application(self, application_id: int) -> None:
        """
        Delete an application.

        Args:
            application_id: The ID of the application
        """
        try:
            response = self.session.delete(f"{self.base_url}/api/applications/{application_id}")
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self._handle_error(f"Failed to delete application {application_id}", e)

    def get_api_keys(self) -> List[Dict[str, Any]]:
        """
        Get all API keys.

        Returns:
            List of API keys
        """
        try:
            response = self.session.get(f"{self.base_url}/api/api-keys")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error("Failed to get API keys", e)

    def create_api_key(self, name: str, application_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Create a new API key.

        Args:
            name: The name of the API key
            application_id: Optional application ID to associate with the key

        Returns:
            Dict containing the created API key details
        """
        payload = {"name": name}
        if application_id:
            payload["applicationId"] = application_id
            
        try:
            response = self.session.post(
                f"{self.base_url}/api/api-keys",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error("Failed to create API key", e)

    def delete_api_key(self, api_key_id: int) -> None:
        """
        Delete an API key.

        Args:
            api_key_id: The ID of the API key
        """
        try:
            response = self.session.delete(f"{self.base_url}/api/api-keys/{api_key_id}")
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self._handle_error(f"Failed to delete API key {api_key_id}", e)

    def get_analytics(self, start_date: Optional[datetime] = None, 
                     end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Get analytics data.

        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering

        Returns:
            List of usage statistics
        """
        params = {}
        if start_date:
            params['startDate'] = start_date.isoformat()
        if end_date:
            params['endDate'] = end_date.isoformat()
            
        try:
            response = self.session.get(
                f"{self.base_url}/api/analytics",
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error("Failed to get analytics data", e)

    def get_auth_events(self, application_id: Optional[int] = None, 
                       limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get authentication events.

        Args:
            application_id: Optional application ID for filtering
            limit: Maximum number of events to return
            offset: Offset for pagination

        Returns:
            List of authentication events
        """
        params = {'limit': limit, 'offset': offset}
        if application_id:
            params['applicationId'] = application_id
            
        try:
            response = self.session.get(
                f"{self.base_url}/api/auth-events",
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self._handle_error("Failed to get authentication events", e)

    def _handle_error(self, message: str, error: requests.exceptions.RequestException) -> None:
        """
        Handle errors gracefully.

        Args:
            message: Error context message
            error: The exception that was raised
        """
        if hasattr(error, 'response') and error.response is not None:
            status_code = error.response.status_code
            try:
                response_data = error.response.json()
            except ValueError:
                response_data = error.response.text
                
            error_message = f"{message}: {status_code} - {json.dumps(response_data)}"
        else:
            error_message = f"{message}: {str(error)}"
            
        print(error_message)
        raise error