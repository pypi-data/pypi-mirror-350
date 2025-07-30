import requests
from typing import Dict, Any, List, Optional
from .exceptions import APIError, ConfigurationError

class UserManagement:
    def __init__(self, api_url: str, api_key: str, verify: bool = True, timeout: int = 60):
        """
        Initialize the User Management client.
        
        Args:
            api_url: API base URL
            api_key: API key for authentication
            verify: Verify SSL certificates
            timeout: Request timeout in seconds
        """
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.verify = verify
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        })

    def get_user_by_id(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve user info by user ID.
        
        Args:
            user_id: User ID to retrieve
        
        Returns:
            User information as a dictionary
            
        Raises:
            APIError: If the API request fails
        """
        endpoint = f"{self.api_url}/admin/users/{user_id}"
        try:
            response = self.session.get(
                endpoint, 
                timeout=self.timeout, 
                verify=self.verify
            )
            if not response.ok:
                raise APIError(f"API request failed: {response.status_code} {response.reason}")
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def get_user_by_email(self, email: str) -> Dict[str, Any]:
        """
        Retrieve user info by email.
        
        Args:
            email: User email to retrieve
            
        Returns:
            User information as a dictionary
            
        Raises:
            APIError: If the API request fails
        """

        endpoint = f"{self.api_url}/admin/users/email/{email}"
        try:
            response = self.session.get(
                endpoint, 
                timeout=self.timeout, 
                verify=self.verify
            )
            if not response.ok:
                raise APIError(f"API request failed: {response.status_code} {response.reason}")
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def edit_user(
        self,
        user_id: str,
        uid: Optional[str] = None,
        email: Optional[str] = None,
        role: Optional[str] = None,
        apiKey: Optional[str] = None,
        groups: Optional[List[str]] = None,
        quota: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Edit user info. Only provided fields will be updated.
        
        Args:
            user_id: User ID (required)
            uid: New user ID (optional)
            email: New user email (optional)
            role: New user role (optional)
            apiKey: New API key (optional)
            groups: New list of groups (optional)
            quota: New quota value (optional)
            
        Returns:
            Updated user information
            
        Raises:
            APIError: If the API request fails
        """
        endpoint = f"{self.api_url}/admin/users"
        payload = {"uid": user_id}

        if uid is not None:
            payload["uid"] = uid
        if email is not None:
            payload["email"] = email
        if role is not None:
            payload["role"] = role
        if apiKey is not None:
            payload["apiKey"] = apiKey
        if groups is not None:
            payload["groups"] = groups
        if quota is not None:
            payload["quota"] = quota

        try:
            response = self.session.patch(
                endpoint,
                json=payload,
                timeout=self.timeout,
                verify=self.verify
            )
            if not response.ok:
                raise APIError(f"API request failed: {response.status_code} {response.reason}")
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def list_users(self, substring: Optional[str] = None, uid: bool = False) -> List[Dict[str, Any]]:
        """
        List users, optionally filtering by a substring.
        
        Args:
            substring: Optional substring to filter users
            uid: If True, includes the user ID in the response (default: False)
        
        Returns:
            List of users
            
        Raises:
            APIError: If the API request fails
        """
        # Use the base API URL instead of hardcoding
        endpoint = "https://terrakio-server-lark-573248941006.australia-southeast1.run.app/admin/users"

        params = {}
        if substring:
            params["substring"] = substring
        if uid:
            params["uid"] = "true"

        try:
            response = self.session.get(
                endpoint,
                params=params,
                timeout=self.timeout,
                verify=self.verify
            )
            if not response.ok:
                raise APIError(f"API request failed: {response.status_code} {response.reason}")
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def reset_quota(self, email: str, quota: Optional[int] = None) -> Dict[str, Any]:
        """
        Reset the quota for a user by email.
        
        Args:
            email: The user's email (required)
            quota: The new quota value (optional)
            
        Returns:
            API response as a dictionary
            
        Raises:
            APIError: If the API request fails
        """
        endpoint = f"{self.api_url}/admin/users/reset_quota/{email}"
        payload = {"email": email}
        if quota is not None:
            payload["quota"] = quota
        try:
            response = self.session.patch(
                endpoint,
                json=payload,
                timeout=self.timeout,
                verify=self.verify
            )
            if not response.ok:
                raise APIError(f"API request failed: {response.status_code} {response.reason}")
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def delete_user(self, uid: str) -> Dict[str, Any]:
        """
        Delete a user by UID.
        
        Args:
            uid: The user's UID (required)
            
        Returns:
            API response as a dictionary
            
        Raises:
            APIError: If the API request fails
        """
        endpoint = f"{self.api_url}/admin/users/{uid}"
        try:
            response = self.session.delete(
                endpoint,
                timeout=self.timeout,
                verify=self.verify
            )
            if not response.ok:
                raise APIError(f"API request failed: {response.status_code} {response.reason}")
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")