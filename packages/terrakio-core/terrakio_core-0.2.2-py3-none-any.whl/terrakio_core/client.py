import requests
import xarray as xr
from io import BytesIO
from typing import Dict, Any, Optional, Union
import json
import aiohttp
import asyncio
from shapely.geometry import shape
from shapely.geometry.base import BaseGeometry as ShapelyGeometry
from .exceptions import APIError, ConfigurationError

class BaseClient:
    def __init__(self, url: Optional[str] = None, key: Optional[str] = None, 
                auth_url: Optional[str] = "https://dev-au.terrak.io",
                quiet: bool = False, config_file: Optional[str] = None,
                verify: bool = True, timeout: int = 60):
        self.quiet = quiet
        self.verify = verify
        self.timeout = timeout
        self.auth_client = None
        if auth_url:
            from terrakio_core.auth import AuthClient
            self.auth_client = AuthClient(
                base_url=auth_url,
                verify=verify,
                timeout=timeout
            )
        self.url = url
        self.key = key
        if self.url is None or self.key is None:
            from terrakio_core.config import read_config_file, DEFAULT_CONFIG_FILE
            if config_file is None:
                config_file = DEFAULT_CONFIG_FILE
            try:
                config = read_config_file(config_file)
                if self.url is None:
                    self.url = config.get('url')
                if self.key is None:
                    self.key = config.get('key')
            except Exception as e:
                raise ConfigurationError(
                    f"Failed to read configuration: {e}\n\n"
                    "To fix this issue:\n"
                    "1. Create a file at ~/.terrakioapirc with:\n"
                    "url: https://api.terrak.io\n"
                    "key: your-api-key\n\n"
                    "OR\n\n"
                    "2. Initialize the client with explicit parameters:\n"
                    "client = terrakio_api.Client(\n"
                    "    url='https://api.terrak.io',\n"
                    "    key='your-api-key'\n"
                    ")"
                )
        if not self.url:
            raise ConfigurationError("Missing API URL in configuration")
        if not self.key:
            raise ConfigurationError("Missing API key in configuration")
        self.url = self.url.rstrip('/')
        if not self.quiet:
            print(f"Using Terrakio API at: {self.url}")
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'x-api-key': self.key
        })
        self.user_management = None
        self.dataset_management = None
        self.mass_stats = None
        self._aiohttp_session = None

    @property
    async def aiohttp_session(self):
        if self._aiohttp_session is None or self._aiohttp_session.closed:
            self._aiohttp_session = aiohttp.ClientSession(
                headers={
                    'Content-Type': 'application/json',
                    'x-api-key': self.key
                },
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self._aiohttp_session

    async def wcs_async(self, expr: str, feature: Union[Dict[str, Any], ShapelyGeometry], 
                       in_crs: str = "epsg:4326", out_crs: str = "epsg:4326", 
                       output: str = "csv", resolution: int = -1, **kwargs):
        """
        Asynchronous version of the wcs() method using aiohttp.
        
        Args:
            expr (str): The WCS expression to evaluate
            feature (Union[Dict[str, Any], ShapelyGeometry]): The geographic feature
            in_crs (str): Input coordinate reference system
            out_crs (str): Output coordinate reference system
            output (str): Output format ('csv' or 'netcdf')
            resolution (int): Resolution parameter
            **kwargs: Additional parameters to pass to the WCS request
            
        Returns:
            Union[pd.DataFrame, xr.Dataset, bytes]: The response data in the requested format
        """
        if hasattr(feature, 'is_valid'):
            from shapely.geometry import mapping
            feature = {
                "type": "Feature",
                "geometry": mapping(feature),
                "properties": {}
            }
        self.validate_feature(feature)
        
        payload = {
            "feature": feature,
            "in_crs": in_crs,
            "out_crs": out_crs,
            "output": output,
            "resolution": resolution,
            "expr": expr,
            **kwargs
        }
        
        request_url = f"{self.url}/geoquery"
        
        try:
            # Get the shared aiohttp session
            session = await self.aiohttp_session
            async with session.post(request_url, json=payload, ssl=self.verify) as response:
                if not response.ok:
                    error_msg = f"API request failed: {response.status} {response.reason}"
                    try:
                        error_data = await response.json()
                        if "detail" in error_data:
                            error_msg += f" - {error_data['detail']}"
                    except:
                        pass
                    raise APIError(error_msg)
                
                content = await response.read()
                
                if output.lower() == "csv":
                    import pandas as pd
                    df = pd.read_csv(BytesIO(content))
                    return df
                elif output.lower() == "netcdf":
                    return xr.open_dataset(BytesIO(content))
                else:
                    try:
                        return xr.open_dataset(BytesIO(content))
                    except ValueError:
                        import pandas as pd
                        try:
                            return pd.read_csv(BytesIO(content))
                        except:
                            return content
                            
        except aiohttp.ClientError as e:
            raise APIError(f"Request failed: {str(e)}")
        except Exception as e:
            raise

    async def close_async(self):
        """Close the aiohttp session"""
        if self._aiohttp_session and not self._aiohttp_session.closed:
            await self._aiohttp_session.close()
            self._aiohttp_session = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_async()

    def validate_feature(self, feature: Dict[str, Any]) -> None:
        if hasattr(feature, 'is_valid'):
            from shapely.geometry import mapping
            feature = {
                "type": "Feature",
                "geometry": mapping(feature),
                "properties": {}
            }
        if not isinstance(feature, dict):
            raise ValueError("Feature must be a dictionary or a Shapely geometry")
        if feature.get("type") != "Feature":
            raise ValueError("GeoJSON object must be of type 'Feature'")
        if "geometry" not in feature:
            raise ValueError("Feature must contain a 'geometry' field")
        if "properties" not in feature:
            raise ValueError("Feature must contain a 'properties' field")
        try:
            geometry = shape(feature["geometry"])
        except Exception as e:
            raise ValueError(f"Invalid geometry format: {str(e)}")
        if not geometry.is_valid:
            raise ValueError(f"Invalid geometry: {geometry.is_valid_reason}")
        geom_type = feature["geometry"]["type"]
        if geom_type == "Point":
            if len(feature["geometry"]["coordinates"]) != 2:
                raise ValueError("Point must have exactly 2 coordinates")
        elif geom_type == "Polygon":
            if not geometry.is_simple:
                raise ValueError("Polygon must be simple (not self-intersecting)")
            if geometry.area == 0:
                raise ValueError("Polygon must have non-zero area")
            coords = feature["geometry"]["coordinates"][0]
            if coords[0] != coords[-1]:
                raise ValueError("Polygon must be closed (first and last points must match)")

    def signup(self, email: str, password: str) -> Dict[str, Any]:
        if not self.auth_client:
            raise ConfigurationError("Authentication client not initialized. Please provide auth_url during client initialization.")
        return self.auth_client.signup(email, password)

    def login(self, email: str, password: str) -> Dict[str, str]:
        if not self.auth_client:
            raise ConfigurationError("Authentication client not initialized. Please provide auth_url during client initialization.")
        
        try:
            # First attempt to login
            token_response = self.auth_client.login(email, password)
            
            print("the token response is ", token_response)
            # Only proceed with API key retrieval if login was successful
            if token_response:
                # After successful login, get the API key
                api_key_response = self.view_api_key()
                self.key = api_key_response
                
                # Save email and API key to config file
                import os
                import json
                config_path = os.path.join(os.environ.get("HOME", ""), ".tkio_config.json")
                try:
                    config = {"EMAIL": email, "TERRAKIO_API_KEY": self.key}
                    if os.path.exists(config_path):
                        with open(config_path, 'r') as f:
                            config = json.load(f)
                        config["EMAIL"] = email
                        config["TERRAKIO_API_KEY"] = self.key
                    
                    os.makedirs(os.path.dirname(config_path), exist_ok=True)
                    with open(config_path, 'w') as f:
                        json.dump(config, f, indent=4)
                    
                    if not self.quiet:
                        print(f"Successfully authenticated as: {email}")
                        print(f"API key saved to {config_path}")
                except Exception as e:
                    if not self.quiet:
                        print(f"Warning: Failed to update config file: {e}")
            
            return {"token": token_response} if token_response else {"error": "Login failed"}
        except Exception as e:
            if not self.quiet:
                print(f"Login failed: {str(e)}")
            raise

    def refresh_api_key(self) -> str:
        if not self.auth_client:
            raise ConfigurationError("Authentication client not initialized. Please provide auth_url during client initialization.")
        if not self.auth_client.token:
            raise ConfigurationError("Not authenticated. Call login() first.")
        self.key = self.auth_client.refresh_api_key()
        self.session.headers.update({'x-api-key': self.key})
        import os
        config_path = os.path.join(os.environ.get("HOME", ""), ".tkio_config.json")
        try:
            config = {"EMAIL": "", "TERRAKIO_API_KEY": ""}
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
            config["TERRAKIO_API_KEY"] = self.key
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
            if not self.quiet:
                print(f"API key generated successfully and updated in {config_path}")
        except Exception as e:
            if not self.quiet:
                print(f"Warning: Failed to update config file: {e}")
        return self.key

    def view_api_key(self) -> str:
        if not self.auth_client:
            raise ConfigurationError("Authentication client not initialized. Please provide auth_url during client initialization.")
        if not self.auth_client.token:
            raise ConfigurationError("Not authenticated. Call login() first.")
        self.key = self.auth_client.view_api_key()
        self.session.headers.update({'x-api-key': self.key})
        return self.key

    def get_user_info(self) -> Dict[str, Any]:
        if not self.auth_client:
            raise ConfigurationError("Authentication client not initialized. Please provide auth_url during client initialization.")
        if not self.auth_client.token:
            raise ConfigurationError("Not authenticated. Call login() first.")
        return self.auth_client.get_user_info()

    def wcs(self, expr: str, feature: Union[Dict[str, Any], ShapelyGeometry], in_crs: str = "epsg:4326",
            out_crs: str = "epsg:4326", output: str = "csv", resolution: int = -1,
            **kwargs):
        if hasattr(feature, 'is_valid'):
            from shapely.geometry import mapping
            feature = {
                "type": "Feature",
                "geometry": mapping(feature),
                "properties": {}
            }
        self.validate_feature(feature)
        payload = {
            "feature": feature,
            "in_crs": in_crs,
            "out_crs": out_crs,
            "output": output,
            "resolution": resolution,
            "expr": expr,
            **kwargs
        }
        request_url = f"{self.url}/geoquery"
        try:
            response = self.session.post(request_url, json=payload, timeout=self.timeout, verify=self.verify)
            if not response.ok:
                error_msg = f"API request failed: {response.status_code} {response.reason}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_msg += f" - {error_data['detail']}"
                except:
                    pass
                raise APIError(error_msg)
            if output.lower() == "csv":
                import pandas as pd
                return pd.read_csv(BytesIO(response.content))
            elif output.lower() == "netcdf":
                return xr.open_dataset(BytesIO(response.content))
            else:
                try:
                    return xr.open_dataset(BytesIO(response.content))
                except ValueError:
                    import pandas as pd
                    try:
                        return pd.read_csv(BytesIO(response.content))
                    except:
                        return response.content
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    # Admin/protected methods
    def _get_user_by_id(self, user_id: str):
        if not self.user_management:
            from terrakio_core.user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.get_user_by_id(user_id)

    def _get_user_by_email(self, email: str):
        if not self.user_management:
            from terrakio_core.user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.get_user_by_email(email)

    def _list_users(self, substring: str = None, uid: bool = False):
        if not self.user_management:
            from terrakio_core.user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.list_users(substring=substring, uid=uid)

    def _edit_user(self, user_id: str, uid: str = None, email: str = None, role: str = None, apiKey: str = None, groups: list = None, quota: int = None):
        if not self.user_management:
            from terrakio_core.user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.edit_user(
            user_id=user_id,
            uid=uid,
            email=email,
            role=role,
            apiKey=apiKey,
            groups=groups,
            quota=quota
        )

    def _reset_quota(self, email: str, quota: int = None):
        if not self.user_management:
            from terrakio_core.user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.reset_quota(email=email, quota=quota)

    def _delete_user(self, uid: str):
        if not self.user_management:
            from terrakio_core.user_management import UserManagement
            if not self.url or not self.key:
                raise ConfigurationError("User management client not initialized. Make sure API URL and key are set.")
            self.user_management = UserManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.user_management.delete_user(uid=uid)

    # Dataset management protected methods
    def _get_dataset(self, name: str, collection: str = "terrakio-datasets"):
        if not self.dataset_management:
            from terrakio_core.dataset_management import DatasetManagement
            if not self.url or not self.key:
                raise ConfigurationError("Dataset management client not initialized. Make sure API URL and key are set.")
            self.dataset_management = DatasetManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.dataset_management.get_dataset(name=name, collection=collection)

    def _list_datasets(self, substring: str = None, collection: str = "terrakio-datasets"):
        if not self.dataset_management:
            from terrakio_core.dataset_management import DatasetManagement
            if not self.url or not self.key:
                raise ConfigurationError("Dataset management client not initialized. Make sure API URL and key are set.")
            self.dataset_management = DatasetManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.dataset_management.list_datasets(substring=substring, collection=collection)

    def _create_dataset(self, name: str, collection: str = "terrakio-datasets", **kwargs):
        if not self.dataset_management:
            from terrakio_core.dataset_management import DatasetManagement
            if not self.url or not self.key:
                raise ConfigurationError("Dataset management client not initialized. Make sure API URL and key are set.")
            self.dataset_management = DatasetManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.dataset_management.create_dataset(name=name, collection=collection, **kwargs)

    def _update_dataset(self, name: str, append: bool = True, collection: str = "terrakio-datasets", **kwargs):
        if not self.dataset_management:
            from terrakio_core.dataset_management import DatasetManagement
            if not self.url or not self.key:
                raise ConfigurationError("Dataset management client not initialized. Make sure API URL and key are set.")
            self.dataset_management = DatasetManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.dataset_management.update_dataset(name=name, append=append, collection=collection, **kwargs)

    def _overwrite_dataset(self, name: str, collection: str = "terrakio-datasets", **kwargs):
        if not self.dataset_management:
            from terrakio_core.dataset_management import DatasetManagement
            if not self.url or not self.key:
                raise ConfigurationError("Dataset management client not initialized. Make sure API URL and key are set.")
            self.dataset_management = DatasetManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.dataset_management.overwrite_dataset(name=name, collection=collection, **kwargs)

    def _delete_dataset(self, name: str, collection: str = "terrakio-datasets"):
        if not self.dataset_management:
            from terrakio_core.dataset_management import DatasetManagement
            if not self.url or not self.key:
                raise ConfigurationError("Dataset management client not initialized. Make sure API URL and key are set.")
            self.dataset_management = DatasetManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.dataset_management.delete_dataset(name=name, collection=collection)

    def close(self):
        """Close all client sessions"""
        self.session.close()
        if self.auth_client:
            self.auth_client.session.close()
        # Close aiohttp session if it exists
        if self._aiohttp_session and not self._aiohttp_session.closed:
            asyncio.run(self.close_async())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # Mass Stats methods
    def upload_mass_stats(self, name, size, bucket, output, location=None, **kwargs):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.upload_request(name, size, bucket, output, location, **kwargs)

    def start_mass_stats_job(self, task_id):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.start_job(task_id)

    def get_mass_stats_task_id(self, name, stage, uid=None):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.get_task_id(name, stage, uid)

    def track_mass_stats_job(self, ids=None):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.track_job(ids)

    def get_mass_stats_history(self, limit=100):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.get_history(limit)

    def start_mass_stats_post_processing(self, process_name, data_name, output, consumer_path, overwrite=False):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.start_post_processing(process_name, data_name, output, consumer_path, overwrite)

    def download_mass_stats_results(self, id=None, force_loc=False, **kwargs):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.download_results(id, force_loc, **kwargs)

    def cancel_mass_stats_job(self, id):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.cancel_job(id)

    def cancel_all_mass_stats_jobs(self):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.cancel_all_jobs()

    def _create_pyramids(self, name, levels, config):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.create_pyramids(name, levels, config)

    def random_sample(self, name, **kwargs):
        if not self.mass_stats:
            from terrakio_core.mass_stats import MassStats
            if not self.url or not self.key:
                raise ConfigurationError("Mass Stats client not initialized. Make sure API URL and key are set.")
            self.mass_stats = MassStats(
                base_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.mass_stats.random_sample(name, **kwargs)

    async def zonal_stats_async(self, gdb, expr, conc=20, inplace=False, output="csv"):
        """
        Compute zonal statistics for all geometries in a GeoDataFrame using asyncio for concurrency.
        """
        import asyncio
        import pandas as pd
        import geopandas as gpd
        from shapely.geometry import mapping
        
        # Process geometries in batches
        all_results = []
        row_indices = []
        
        async def process_geometry(geom, index):
            """Process a single geometry"""
            try:
                feature = {
                    "type": "Feature",
                    "geometry": mapping(geom),
                    "properties": {"index": index}
                }
                result = await self.wcs_async(expr=expr, feature=feature, output=output)
                # Add original index to track which geometry this result belongs to
                if isinstance(result, pd.DataFrame):
                    result['_geometry_index'] = index
                return result
            except Exception as e:
                raise
        
        async def process_batch(batch_indices):
            """Process a batch of geometries concurrently using TaskGroup"""
            try:
                async with asyncio.TaskGroup() as tg:
                    tasks = []
                    for idx in batch_indices:
                        geom = gdb.geometry.iloc[idx]
                        task = tg.create_task(process_geometry(geom, idx))
                        tasks.append(task)
                
                # Get results from completed tasks
                results = []
                for task in tasks:
                    try:
                        result = task.result()
                        results.append(result)
                    except Exception as e:
                        raise
                
                return results
            except* Exception as e:
                # Get the actual exceptions from the tasks
                for task in tasks:
                    if task.done() and task.exception():
                        raise task.exception()
                raise
            
        # Process in batches to control concurrency
        for i in range(0, len(gdb), conc):
            batch_indices = range(i, min(i + conc, len(gdb)))
            try:
                batch_results = await process_batch(batch_indices)
                all_results.extend(batch_results)
                row_indices.extend(batch_indices)
            except Exception as e:
                if hasattr(e, 'response'):
                    raise APIError(f"API request failed: {e.response.text}")
                raise
        
        if not all_results:
            raise ValueError("No valid results were returned for any geometry")
            
        # Combine all results
        combined_df = pd.concat(all_results, ignore_index=True)
        
        # Check if we have temporal results
        has_time = 'time' in combined_df.columns
        
        # Create a result GeoDataFrame
        if has_time:
            # For temporal data, we'll create a hierarchical index
            # First make sure we have the geometry index and time columns
            if '_geometry_index' not in combined_df.columns:
                raise ValueError("Missing geometry index in results")
            
            # Create hierarchical index on geometry_index and time
            combined_df.set_index(['_geometry_index', 'time'], inplace=True)
            
            # For each unique geometry index, we need the corresponding geometry
            geometry_series = gdb.geometry.copy()
            
            # Get columns that will become new attributes (exclude index/utility columns)
            result_cols = combined_df.columns
            
            # Create a new GeoDataFrame with multi-index
            result_rows = []
            geometries = []
            
            # Iterate through the hierarchical index
            for (geom_idx, time_val), row in combined_df.iterrows():
                # Create a new row with geometry properties + result columns
                new_row = {}
                
                # Add original GeoDataFrame columns (except geometry)
                for col in gdb.columns:
                    if col != 'geometry':
                        new_row[col] = gdb.loc[geom_idx, col]
                
                # Add result columns
                for col in result_cols:
                    new_row[col] = row[col]
                
                result_rows.append(new_row)
                geometries.append(gdb.geometry.iloc[geom_idx])
            
            # Create a new GeoDataFrame with multi-index
            multi_index = pd.MultiIndex.from_tuples(
                combined_df.index.tolist(),
                names=['geometry_index', 'time']
            )
            
            result_gdf = gpd.GeoDataFrame(
                result_rows, 
                geometry=geometries,
                index=multi_index
            )
            
            if inplace:
                # Can't really do inplace with multi-temporal results as we're changing the structure
                return result_gdf
            else:
                return result_gdf
        else:
            # Non-temporal data - just add new columns to the existing GeoDataFrame
            result_gdf = gdb.copy() if not inplace else gdb
            
            # Get column names from the results (excluding utility columns)
            result_cols = [col for col in combined_df.columns if col not in ['_geometry_index']]
            
            # Create a mapping from geometry index to result rows
            geom_idx_to_row = {}
            for idx, row in combined_df.iterrows():
                geom_idx = int(row['_geometry_index'])
                geom_idx_to_row[geom_idx] = row
            
            # Add results as new columns to the GeoDataFrame
            for col in result_cols:
                # Initialize the column with None or appropriate default
                if col not in result_gdf.columns:
                    result_gdf[col] = None
                
                # Fill in values from results
                for geom_idx, row in geom_idx_to_row.items():
                    result_gdf.loc[geom_idx, col] = row[col]
            
            if inplace:
                return None
            else:
                return result_gdf

    def zonal_stats(self, gdb, expr, conc=20, inplace=False, output="csv"):
        """
        Compute zonal statistics for all geometries in a GeoDataFrame.
        
        Args:
            gdb (geopandas.GeoDataFrame): GeoDataFrame containing geometries
            expr (str): Terrakio expression to evaluate, can include spatial aggregations
            conc (int): Number of concurrent requests to make
            inplace (bool): Whether to modify the input GeoDataFrame in place
            output (str): Output format (csv or netcdf)
            
        Returns:
            geopandas.GeoDataFrame: GeoDataFrame with added columns for results, or None if inplace=True
        """
        import asyncio
        result = asyncio.run(self.zonal_stats_async(gdb, expr, conc, inplace, output))
        # Ensure aiohttp session is closed after running async code
        try:
            if self._aiohttp_session and not self._aiohttp_session.closed:
                asyncio.run(self.close_async())
        except RuntimeError:
            # Event loop may already be closed, ignore
            pass
        return result

    # Group access management protected methods
    def _get_group_users_and_datasets(self, group_name: str):
        if not hasattr(self, "group_access_management") or self.group_access_management is None:
            from terrakio_core.group_access_management import GroupAccessManagement
            if not self.url or not self.key:
                raise ConfigurationError("Group access management client not initialized. Make sure API URL and key are set.")
            self.group_access_management = GroupAccessManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.group_access_management.get_group_users_and_datasets(group_name)

    def _add_group_to_dataset(self, dataset: str, group: str):
        if not hasattr(self, "group_access_management") or self.group_access_management is None:
            from terrakio_core.group_access_management import GroupAccessManagement
            if not self.url or not self.key:
                raise ConfigurationError("Group access management client not initialized. Make sure API URL and key are set.")
            self.group_access_management = GroupAccessManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.group_access_management.add_group_to_dataset(dataset, group)

    def _add_group_to_user(self, uid: str, group: str):
        if not hasattr(self, "group_access_management") or self.group_access_management is None:
            from terrakio_core.group_access_management import GroupAccessManagement
            if not self.url or not self.key:
                raise ConfigurationError("Group access management client not initialized. Make sure API URL and key are set.")
            self.group_access_management = GroupAccessManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        print("the uid is and the group is ", uid, group)
        return self.group_access_management.add_group_to_user(uid, group)

    def _delete_group_from_user(self, uid: str, group: str):
        if not hasattr(self, "group_access_management") or self.group_access_management is None:
            from terrakio_core.group_access_management import GroupAccessManagement
            if not self.url or not self.key:
                raise ConfigurationError("Group access management client not initialized. Make sure API URL and key are set.")
            self.group_access_management = GroupAccessManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.group_access_management.delete_group_from_user(uid, group)

    def _delete_group_from_dataset(self, dataset: str, group: str):
        if not hasattr(self, "group_access_management") or self.group_access_management is None:
            from terrakio_core.group_access_management import GroupAccessManagement
            if not self.url or not self.key:
                raise ConfigurationError("Group access management client not initialized. Make sure API URL and key are set.")
            self.group_access_management = GroupAccessManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.group_access_management.delete_group_from_dataset(dataset, group)

    # Space management protected methods
    def _get_total_space_used(self):
        if not hasattr(self, "space_management") or self.space_management is None:
            from terrakio_core.space_management import SpaceManagement
            if not self.url or not self.key:
                raise ConfigurationError("Space management client not initialized. Make sure API URL and key are set.")
            self.space_management = SpaceManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.space_management.get_total_space_used()

    def _get_space_used_by_job(self, name: str, region: str = None):
        if not hasattr(self, "space_management") or self.space_management is None:
            from terrakio_core.space_management import SpaceManagement
            if not self.url or not self.key:
                raise ConfigurationError("Space management client not initialized. Make sure API URL and key are set.")
            self.space_management = SpaceManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.space_management.get_space_used_by_job(name, region)

    def _delete_user_job(self, name: str, region: str = None):
        if not hasattr(self, "space_management") or self.space_management is None:
            from terrakio_core.space_management import SpaceManagement
            if not self.url or not self.key:
                raise ConfigurationError("Space management client not initialized. Make sure API URL and key are set.")
            self.space_management = SpaceManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.space_management.delete_user_job(name, region)

    def _delete_data_in_path(self, path: str, region: str = None):
        if not hasattr(self, "space_management") or self.space_management is None:
            from terrakio_core.space_management import SpaceManagement
            if not self.url or not self.key:
                raise ConfigurationError("Space management client not initialized. Make sure API URL and key are set.")
            self.space_management = SpaceManagement(
                api_url=self.url,
                api_key=self.key,
                verify=self.verify,
                timeout=self.timeout
            )
        return self.space_management.delete_data_in_path(path, region)

