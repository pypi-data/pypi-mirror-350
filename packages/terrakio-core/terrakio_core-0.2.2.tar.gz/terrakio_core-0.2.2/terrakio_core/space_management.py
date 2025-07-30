import requests
from typing import Dict, Any, Optional
from .exceptions import APIError

class SpaceManagement:
    def __init__(self, api_url: str, api_key: str, verify: bool = True, timeout: int = 60):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.verify = verify
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        })

    def get_total_space_used(self) -> Dict[str, Any]:
        """
        Get total space used by the user.
        Returns a dict with user, total, and jobs breakdown.
        """
        endpoint = f"{self.api_url}/users/jobs"
        try:
            response = self.session.get(endpoint, timeout=self.timeout, verify=self.verify)
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

    def get_space_used_by_job(self, name: str, region: Optional[str] = None) -> Dict[str, Any]:
        """
        Get space used by a specific job.
        """
        endpoint = f"{self.api_url}/users/jobs/{name}"
        params = {"region": region} if region else {}
        try:
            response = self.session.get(endpoint, params=params, timeout=self.timeout, verify=self.verify)
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

    def delete_user_job(self, name: str, region: Optional[str] = None) -> Dict[str, Any]:
        """
        Delete a user job by name and region.
        """
        endpoint = f"{self.api_url}/users/job/{name}"
        params = {"region": region} if region else {}
        try:
            response = self.session.delete(endpoint, params=params, timeout=self.timeout, verify=self.verify)
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

    def delete_data_in_path(self, path: str, region: Optional[str] = None) -> Dict[str, Any]:
        """
        Delete data in a GCS path for a given region.
        """
        endpoint = f"{self.api_url}/users/jobs"
        params = {"path": path}
        if region:
            params["region"] = region
        try:
            response = self.session.delete(endpoint, params=params, timeout=self.timeout, verify=self.verify)
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