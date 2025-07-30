import requests
from typing import Optional, Dict, Any

class MassStats:
    def __init__(self, base_url: str, api_key: str, verify: bool = True, timeout: int = 60):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.verify = verify
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'x-api-key': self.api_key
        })

    def upload_request(
        self,
        name: str,
        size: int,
        bucket: str,
        output: str,
        location: Optional[str] = None,
        force_loc: bool = False,
        config: Optional[Dict[str, Any]] = None,
        overwrite: bool = False,
        server: Optional[str] = None,
        skip_existing: bool = False
    ) -> Dict[str, Any]:
        """
        Initiate a mass stats upload job.
        
        Args:
            name: Name of the job
            size: Size of the data
            bucket: Storage bucket
            output: Output path or identifier
            location: (Optional) Location for the upload
            force_loc: Force location usage
            config: Optional configuration dictionary
            overwrite: Overwrite existing data
            server: Optional server
            skip_existing: Skip existing files
        """
        url = f"{self.base_url}/mass_stats/upload"
        data = {
            "name": name,
            "size": size,
            "bucket": bucket,
            "output": output,
            "force_loc": force_loc,
            "overwrite": overwrite,
            "skip_existing": skip_existing
        }
        if location is not None:
            data["location"] = location
        if config is not None:
            data["config"] = config
        if server is not None:
            data["server"] = server
        response = self.session.post(url, json=data, verify=self.verify, timeout=self.timeout)
        print("the response is ", response.text)
        # response.raise_for_status()
        return response.json()

    def start_job(self, task_id: str) -> Dict[str, Any]:
        """
        Start a mass stats job by task ID.
        """
        url = f"{self.base_url}/mass_stats/start/{task_id}"
        print("the self session header is ", self.session.headers)
        response = self.session.post(url, verify=self.verify, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_task_id(self, name: str, stage: str, uid: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the task ID for a mass stats job by name and stage (and optionally user ID).
        """
        url = f"{self.base_url}/mass_stats/job_id?name={name}&stage={stage}"
        if uid is not None:
            url += f"&uid={uid}"
        response = self.session.get(url, verify=self.verify, timeout=self.timeout)
        print("response text is ", response.text)
        return response.json()

    def track_job(self, ids: Optional[list] = None) -> Dict[str, Any]:
        """
        Track the status of one or more mass stats jobs.
        If ids is None, gets progress for all of the user's jobs.
        """
        url = f"{self.base_url}/mass_stats/track"
        data = {"ids": ids} if ids is not None else {}
        response = self.session.post(url, json=data, verify=self.verify, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_history(self, limit: int = 100) -> Dict[str, Any]:
        """
        Get the history of mass stats jobs.
        """
        url = f"{self.base_url}/mass_stats/history"
        params = {"limit": limit}
        response = self.session.get(url, params=params, verify=self.verify, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def start_post_processing(
        self,
        process_name: str,
        data_name: str,
        output: str,
        consumer_path: str,
        overwrite: bool = False
    ) -> Dict[str, Any]:
        """
        Start post processing for a mass stats job.
        Args:
            process_name: Folder to store output
            data_name: Name of job used to create data
            output: Output type
            consumer_path: Path to the post processing script (Python file)
            overwrite: Overwrite existing post processing output in same location
        Returns:
            Dict with task_id
        """
        url = f"{self.base_url}/mass_stats/post_process"
        files = {
            'consumer': (consumer_path, open(consumer_path, 'rb'), 'text/x-python')
        }
        data = {
            'process_name': process_name,
            'data_name': data_name,
            'output': output,
            'overwrite': str(overwrite).lower()
        }
        response = self.session.post(url, data=data, files=files, verify=self.verify, timeout=self.timeout)
        print("the response is ", response.text)
        # response.raise_for_status()
        return response.json()

    def download_results(
        self,
        id: Optional[str] = None,
        force_loc: bool = False,
        bucket: Optional[str] = None,
        location: Optional[str] = None,
        output: Optional[str] = None,
        file_name: Optional[str] = None
    ) -> bytes:
        """
        Download results from a mass stats job or arbitrary results if force_loc is True.
        Returns the content of the .zip file.
        """
        url = f"{self.base_url}/mass_stats/download"
        data = {}
        if id is not None:
            data["id"] = id
        if force_loc:
            data["force_loc"] = True
            if bucket is not None:
                data["bucket"] = bucket
            if location is not None:
                data["location"] = location
            if output is not None:
                data["output"] = output
        if file_name is not None:
            data["file_name"] = file_name
        response = self.session.post(url, json=data, verify=self.verify, timeout=self.timeout)
        print("the response is ", response.text)
        # response.raise_for_status()
        print("the response content is ", response.content)
        return response.content

    def cancel_job(self, id: str) -> Dict[str, Any]:
        """
        Cancel a mass stats job by ID.
        """
        url = f"{self.base_url}/mass_stats/cancel/{id}"
        response = self.session.post(url, verify=self.verify, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def cancel_all_jobs(self) -> Dict[str, Any]:
        """
        Cancel all mass stats jobs for the user.
        """
        url = f"{self.base_url}/mass_stats/cancel"
        response = self.session.post(url, verify=self.verify, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def create_pyramids(self, name: str, levels: int, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create pyramids for a dataset.
        Args:
            name: Name for the pyramid job
            levels: Number of zoom levels to compute
            config: Dataset config (mapping)
        Returns:
            Dict with task_id
        """
        url = f"{self.base_url}/pyramids/create"
        data = {
            "name": name,
            "levels": levels,
            "config": config
        }
        response = self.session.post(url, json=data, verify=self.verify, timeout=self.timeout)
        print("the url is   ", url)
        print("the response is ", response.text)
        print("the response status code is ", response.status_code)
        # response.raise_for_status()
        return response.json()

    def random_sample(
        self,
        name: str,
        config: dict,
        aoi: dict,
        samples: int,
        year_range: list,
        crs: str,
        tile_size: int,
        res: float,
        output: str,
        server: str,
        region: str,
        bucket: str,
        overwrite: bool = False
    ) -> Dict[str, Any]:
        """
        Submit a random sample job.
        """
        if year_range is None or len(year_range) != 2:
            raise ValueError("year_range must be a list of two integers")
        start_year, end_year = year_range
        if start_year is None or end_year is None:
            raise ValueError("Both start_year and end_year must be provided for year_range.")

        url = f"{self.base_url}/random_sample"
        data = {
            "name": name,
            "overwrite": overwrite,
            "config": config,
            "aoi": aoi,
            "samples": samples,
            "year_range": [start_year, end_year],
            "crs": crs,
            "tile_size": tile_size,
            "res": res,
            "output": output,
            "server": server,
            "region": region,
            "bucket": bucket
        }
        print("the data is ", data)
        print("the url is ", url)
        response = self.session.post(url, json=data, verify=self.verify, timeout=self.timeout)
        print("Status code:", response.status_code)
        print("Response text:", response.text)
        # response.raise_for_status()
        return response.json() 
    
