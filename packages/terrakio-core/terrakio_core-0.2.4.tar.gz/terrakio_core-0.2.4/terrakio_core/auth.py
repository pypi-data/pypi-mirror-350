import requests
from typing import Optional, Dict, Any
from .exceptions import APIError, ConfigurationError

class AuthClient:
    def __init__(self, base_url: str = "https://dev-au.terrak.io", 
                 verify: bool = True, timeout: int = 60):
        """
        Initialize the Authentication Client for Terrakio API.
        
        Args:
            base_url: Authentication API base URL
            verify: Verify SSL certificates
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.verify = verify
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
        self.token = None
        self.api_key = None
    
    def signup(self, email: str, password: str) -> Dict[str, Any]:
        """
        Register a new user account.
        
        Args:
            email: User email address
            password: User password
        
        Returns:
            API response data
        
        Raises:
            APIError: If signup fails
        """
        endpoint = f"{self.base_url}/users/signup"
        
        payload = {
            "email": email,
            "password": password
        }
        print("the payload is ", payload)
        print("the endpoint is ", endpoint)
        try:
            response = self.session.post(
                endpoint, 
                json=payload,
                verify=self.verify,
                timeout=self.timeout
            )
            print("the response is ", response)
            if not response.ok:
                error_msg = f"Signup failed: {response.status_code} {response.reason}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg += f" - {error_data['detail']}"
                except:
                    pass
                raise APIError(error_msg)
            
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Signup request failed: {str(e)}")
    
    def login(self, email: str, password: str) -> str:
        """
        Log in and obtain authentication token.
        
        Args:
            email: User email address
            password: User password
        
        Returns:
            Authentication token
        
        Raises:
            APIError: If login fails
        """
        endpoint = f"{self.base_url}/users/login"
        
        payload = {
            "email": email,
            "password": password
        }
        
        try:
            response = self.session.post(
                endpoint, 
                json=payload,
                verify=self.verify,
                timeout=self.timeout
            )
            
            if not response.ok:
                error_msg = f"Login failed: {response.status_code} {response.reason}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg += f" - {error_data['detail']}"
                except:
                    pass
                raise APIError(error_msg)
            
            result = response.json()
            self.token = result.get("token")
            
            # Update session with authorization header
            if self.token:
                self.session.headers.update({
                    "Authorization": self.token
                })
            
            return self.token
        except requests.RequestException as e:
            raise APIError(f"Login request failed: {str(e)}")
    
    def refresh_api_key(self) -> str:
        """
        Generate or refresh API key.
        
        Returns:
            API key
        
        Raises:
            ConfigurationError: If not authenticated
            APIError: If refresh fails
        """
        if not self.token:
            raise ConfigurationError("Not authenticated. Call login() first.")
        
        endpoint = f"{self.base_url}/users/refresh_key"
        
        try:
            # Use session with updated headers from login
            response = self.session.post(
                endpoint,
                verify=self.verify,
                timeout=self.timeout
            )
            
            if not response.ok:
                error_msg = f"API key generation failed: {response.status_code} {response.reason}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg += f" - {error_data['detail']}"
                except:
                    pass
                raise APIError(error_msg)
            
            result = response.json()
            self.api_key = result.get("apiKey")
            return self.api_key
        except requests.RequestException as e:
            raise APIError(f"API key refresh request failed: {str(e)}")
    
    def view_api_key(self) -> str:
        """
        Retrieve current API key.
        
        Returns:
            API key
        
        Raises:
            ConfigurationError: If not authenticated
            APIError: If retrieval fails
        """
        if not self.token:
            raise ConfigurationError("Not authenticated. Call login() first.")
        
        endpoint = f"{self.base_url}/users/key"
        
        try:
            # Use session with updated headers from login
            response = self.session.get(
                endpoint,
                verify=self.verify,
                timeout=self.timeout
            )
            
            if not response.ok:
                error_msg = f"Failed to retrieve API key: {response.status_code} {response.reason}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg += f" - {error_data['detail']}"
                except:
                    pass
                raise APIError(error_msg)
            
            result = response.json()
            self.api_key = result.get("apiKey")
            return self.api_key
        except requests.RequestException as e:
            raise APIError(f"API key retrieval request failed: {str(e)}")
    
    def get_user_info(self) -> Dict[str, Any]:
        """
        Retrieve the current user's information.
        
        Returns:
            User information data
        
        Raises:
            ConfigurationError: If not authenticated
            APIError: If retrieval fails
        """
        if not self.token:
            raise ConfigurationError("Not authenticated. Call login() first.")
        
        endpoint = f"{self.base_url}/users/info"
        
        try:
            # Use session with updated headers from login
            response = self.session.get(
                endpoint,
                verify=self.verify,
                timeout=self.timeout
            )
            
            if not response.ok:
                error_msg = f"Failed to retrieve user info: {response.status_code} {response.reason}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg += f" - {error_data['detail']}"
                except:
                    pass
                raise APIError(error_msg)
            
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"User info retrieval request failed: {str(e)}")