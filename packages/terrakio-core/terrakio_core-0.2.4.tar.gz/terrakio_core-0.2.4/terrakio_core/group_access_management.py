import requests
from typing import Dict, Any, List
from .exceptions import APIError

class GroupAccessManagement:
    def __init__(self, api_url: str, api_key: str, verify: bool = True, timeout: int = 60):
        """
        Initialize the Group Access Management client.
        
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

    def get_group_users_and_datasets(self, group_name: str) -> Dict[str, Any]:
        """
        Get users and datasets of a group.
        
        Args:
            group_name: Name of the group
        
        Returns:
            Dictionary containing lists of users and datasets associated with the group
            {
                "users": [UID, ...],
                "datasets": [DATASET_NAME, ...]
            }
            
        Raises:
            APIError: If the API request fails
        """
        endpoint = f"https://dev-au.terrak.io/groups/{group_name}"
        print("the endpoint is ", endpoint)
        print
        try:
            response = self.session.get(
                endpoint,
                timeout=self.timeout,
                verify=self.verify
            )
            print("the response is ", response.text)
            if not response.ok:
                error_msg = f"API request failed: {response.status_code} {response.reason}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg += f" - {error_data['detail']}"
                except:
                    pass
                raise APIError(error_msg)
            
            return response.json()
            
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def add_group_to_dataset(self, dataset: str, group: str) -> Dict[str, Any]:
        """
        Add a group to a dataset.
        
        Args:
            dataset: Name of the dataset
            group: Name of the group to add to the dataset
        
        Returns:
            API response data
            
        Raises:
            APIError: If the API request fails
        """
        endpoint = f"{self.api_url}/groups/dataset/{dataset}"
        print("hello")
        print("the endpoint is ", endpoint)
        params = {"group": group}
        print("the endpoint is ", endpoint)
        print("!!!!!!!!!!!")
        print("the params are ", params)
        try:
            response = self.session.post(
                endpoint,
                params=params,
                timeout=self.timeout,
                verify=self.verify
            )
            
            if not response.ok:
                error_msg = f"API request failed: {response.status_code} {response.reason}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg += f" - {error_data['detail']}"
                except:
                    pass
                raise APIError(error_msg)
            
            return response.json()
            
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def add_group_to_user(self, uid: str, group: str) -> Dict[str, Any]:
        """
        Add a group to a user.

        Args:
            uid: User UID
            group: Name of the group to add to the user

        Returns:
            API response data

        Raises:
            APIError: If the API request fails
        """
        endpoint = f"{self.api_url}/groups/users/{uid}"
        params = {"group": group}
        print("the endpoint is ", endpoint)
        print("the params are ", params)
        try:
            response = self.session.post(
                endpoint,
                params=params,
                timeout=self.timeout,
                verify=self.verify
            )

            if not response.ok:
                error_msg = f"API request failed: {response.status_code} {response.reason}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg += f" - {error_data['detail']}"
                except:
                    pass
                raise APIError(error_msg)

            return response.json()

        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def delete_group_from_user(self, uid: str, group: str) -> Dict[str, Any]:
        """
        Delete a group from a user.

        Args:
            uid: User UID
            group: Name of the group to remove from the user

        Returns:
            API response data

        Raises:
            APIError: If the API request fails
        """
        endpoint = f"{self.api_url}/groups/users/{uid}"
        params = {"group": group}

        try:
            response = self.session.delete(
                endpoint,
                params=params,
                timeout=self.timeout,
                verify=self.verify
            )

            if not response.ok:
                error_msg = f"API request failed: {response.status_code} {response.reason}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg += f" - {error_data['detail']}"
                except:
                    pass
                raise APIError(error_msg)

            return response.json()

        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def delete_group_from_dataset(self, dataset: str, group: str) -> Dict[str, Any]:
        """
        Delete a group from a dataset.

        Args:
            dataset: Name of the dataset
            group: Name of the group to remove from the dataset

        Returns:
            API response data

        Raises:
            APIError: If the API request fails
        """
        endpoint = f"{self.api_url}/groups/datasets/{dataset}"
        params = {"group": group}

        try:
            response = self.session.delete(
                endpoint,
                params=params,
                timeout=self.timeout,
                verify=self.verify
            )

            if not response.ok:
                error_msg = f"API request failed: {response.status_code} {response.reason}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg += f" - {error_data['detail']}"
                except:
                    pass
                raise APIError(error_msg)

            return response.json()

        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

