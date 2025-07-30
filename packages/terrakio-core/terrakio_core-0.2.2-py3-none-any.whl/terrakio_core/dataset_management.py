import requests
from typing import Dict, Any, List, Optional
from .exceptions import APIError

class DatasetManagement:
    def __init__(self, api_url: str, api_key: str, verify: bool = True, timeout: int = 60):
        """
        Initialize the Dataset Management client.
        
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

    def get_dataset(self, name: str, collection: str = "terrakio-datasets") -> Dict[str, Any]:
        """
        Retrieve dataset info by dataset name.
        
        Args:
            name: The name of the dataset (required)
            collection: The dataset collection (default: 'terrakio-datasets')
            
        Returns:
            Dataset information as a dictionary
            
        Raises:
            APIError: If the API request fails
        """
        endpoint = f"{self.api_url}/datasets/{name}"
        params = {"collection": collection} if collection else {}
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

    def list_datasets(self, substring: Optional[str] = None, collection: str = "terrakio-datasets") -> List[Dict[str, Any]]:
        """
        List datasets, optionally filtering by a substring and collection.
        
        Args:
            substring: Substring to filter by (optional)
            collection: Dataset collection (default: 'terrakio-datasets')
            
        Returns:
            List of datasets matching the criteria
            
        Raises:
            APIError: If the API request fails
        """
        endpoint = f"{self.api_url}/datasets"
        params = {"collection": collection}
        if substring:
            params["substring"] = substring
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

    def create_dataset(self, name: str, collection: str = "terrakio-datasets", **kwargs) -> Dict[str, Any]:
        """
        Create a new dataset.
        
        Args:
            name: Name of the dataset (required)
            collection: Dataset collection (default: 'terrakio-datasets')
            **kwargs: Additional dataset parameters including:
                - products: List of products
                - dates_iso8601: List of dates
                - bucket: Storage bucket
                - path: Storage path
                - data_type: Data type
                - no_data: No data value
                - l_max: Maximum level
                - y_size: Y size
                - x_size: X size
                - proj4: Projection string
                - abstract: Dataset abstract
                - geotransform: Geotransform parameters
                
        Returns:
            Created dataset information
            
        Raises:
            APIError: If the API request fails
        """
        endpoint = f"{self.api_url}/datasets"
        params = {"collection": collection}
        # Create payload with required name parameter
        payload = {"name": name}
        
        # Add optional parameters if provided
        for param in ["products", "dates_iso8601", "bucket", "path", "data_type", 
                     "no_data", "l_max", "y_size", "x_size", "proj4", "abstract", "geotransform"]:
            if param in kwargs:
                payload[param] = kwargs[param]
        
        try:
            response = self.session.post(
                endpoint,
                params=params,
                json=payload,
                timeout=self.timeout,
                verify=self.verify
            )
            
            if not response.ok:
                raise APIError(f"API request failed: {response.status_code} {response.reason}")
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def update_dataset(self, name: str, append: bool = True, collection: str = "terrakio-datasets", **kwargs) -> Dict[str, Any]:
        """
        Update a dataset. By default, values are appended unless append is set to False.
        
        Args:
            name: Name of the dataset (required)
            append: Whether to append values (default: True)
            collection: Dataset collection (default: 'terrakio-datasets')
            **kwargs: Additional dataset parameters to update
                
        Returns:
            Updated dataset information
            
        Raises:
            APIError: If the API request fails
        """
        endpoint = f"{self.api_url}/datasets"
        params = {"append": str(append).lower(), "collection": collection}
        payload = {"name": name}
        payload.update(kwargs)
        try:
            response = self.session.patch(
                endpoint,
                params=params,
                json=payload,
                timeout=self.timeout,
                verify=self.verify
            )
            if not response.ok:
                raise APIError(f"API request failed: {response.status_code} {response.reason}")
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def overwrite_dataset(self, name: str, collection: str = "terrakio-datasets", **kwargs) -> Dict[str, Any]:
        """
        Overwrite a dataset (replace all values).
        
        Args:
            name: Name of the dataset (required)
            collection: Dataset collection (default: 'terrakio-datasets')
            **kwargs: New dataset parameters
                
        Returns:
            Updated dataset information
            
        Raises:
            APIError: If the API request fails
        """
        endpoint = f"{self.api_url}/datasets"
        params = {"collection": collection}
        payload = {"name": name}
        payload.update(kwargs)
        try:
            response = self.session.put(
                endpoint,
                params=params,
                json=payload,
                timeout=self.timeout,
                verify=self.verify
            )
            if not response.ok:
                raise APIError(f"API request failed: {response.status_code} {response.reason}")
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def delete_dataset(self, name: str, collection: str = "terrakio-datasets") -> Dict[str, Any]:
        """
        Delete a dataset by name.
        
        Args:
            name: The name of the dataset (required)
            collection: Dataset collection (default: 'terrakio-datasets')
                
        Returns:
            API response as a dictionary
            
        Raises:
            APIError: If the API request fails
        """
        endpoint = f"{self.api_url}/datasets/{name}"
        params = {"collection": collection}
        try:
            response = self.session.delete(
                endpoint,
                params=params,
                timeout=self.timeout,
                verify=self.verify
            )
            if response.status_code == 404:
                return {"status": "error", "message": f"Dataset '{name}' does not exist in collection '{collection}'"}
            if not response.ok:
                raise APIError(f"API request failed: {response.status_code} {response.reason}")
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}") 