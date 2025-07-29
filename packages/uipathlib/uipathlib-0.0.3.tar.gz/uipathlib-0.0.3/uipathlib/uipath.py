"""
This library provides a Python client for interacting with the UiPath Orchestrator API.
"""

# import base64
import dataclasses
from datetime import datetime
import json
import logging
from pydantic import BaseModel, Field, parse_obj_as, validator
import requests
from typing import Any, Type


class UiPath(object):
    @dataclasses.dataclass
    class Configuration:
        url_base: str | None = None
        client_id: str | None = None
        refresh_token: str | None = None
        token: str | None = None

    @dataclasses.dataclass
    class Response:
        status_code: int
        content: Any = None

    def __init__(self, url_base: str, client_id: str, refresh_token: str) -> None:
        """
        Initializes the UiPath Cloud client with the provided credentials and configuration.

        Args:
            url_base (str): The base URL for the UiPath Orchestrator API.
            client_id (str): The client ID for authentication.
            refresh_token (str): The refresh token for authentication.
        """
        # Init logging
        self.__logger = logging.getLogger(name=__name__)
        self.__logger.setLevel(level=logging.INFO)
        handler = logging.StreamHandler()
        self.__logger.addHandler(handler)

        # Init variables
        self.__session: requests.Session = requests.Session()

        # Credentials/Configuration
        self.__configuration = self.Configuration(url_base=url_base,
                                                  client_id=client_id,
                                                  refresh_token=refresh_token,
                                                  token=None)

        # Authenticate
        self.auth()

    def __del__(self) -> None:
        """
        Cleans the house at the exit.
        """
        self.__logger.info(msg="Cleans the house at the exit")
        self.__session.close()

    def is_auth(self) -> bool:
        """
        Checks whether authentication was successful.

        Returns:
            bool: If true, then authentication was successful.
        """
        self.__logger.info(msg="Gets authentication status")
        return False if self.__configuration.token is None else True

    def auth(self) -> None:
        """
        Authentication.
        This method performs the authentication process to obtain an access token
        using the client credentials flow. The token is stored in the Configuration
        dataclass for subsequent API requests.
        """
        self.__logger.info(msg="Authentication")

        # Request headers
        headers = {"Connection": "keep-alive",
                   "Content-Type": "application/json"}

        # Authorization URL
        url_auth = "https://account.uipath.com/oauth/token"

        # Request body
        body = {"grant_type": "refresh_token",
                "client_id": self.__configuration.client_id,
                "refresh_token": self.__configuration.refresh_token}

        # Request
        response = self.__session.post(url=url_auth, json=body, headers=headers)  # , verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Return valid response
        if response.status_code == 200:
            self.__configuration.token = json.loads(response.content.decode("utf-8"))["access_token"]

    def _export_to_json(self, content: bytes, save_as: str | None) -> None:
        """
        Export response content to a JSON file.

        This method takes the content to be exported and saves it to a specified file in JSON format.
        If the `save_as` parameter is provided, the content will be written to that file.

        Args:
            content (bytes): The content to be exported, typically the response content from an API call.
            save_as (str): The file path where the JSON content will be saved. If None, the content will not be saved.
        """
        if save_as is not None:
            self.__logger.info(msg="Exports response to JSON file.")
            with open(file=save_as, mode="wb") as file:
                file.write(content)
    
    def _handle_response(self, response: requests.Response, model: Type[BaseModel], rtype: str = "scalar") -> BaseModel | list[BaseModel]:
        """
        Handles the response from an API request and deserializes the JSON content.

        This method processes the response from an API request and deserializes the JSON content
        that contains a single instance of a Pydantic BaseModel (scalar) or a list of instances (list).

        Args:
            response (requests.Response): The response object from the API request.
            model (BaseModel): The Pydantic BaseModel class to use for deserialization and validation.
            rtype (str, optional): The type of response to handle. Options are "scalar" for a single record
                                   and "list" for a list of records. Defaults to "scalar".

        Returns:
            BaseModel | list[BaseModel]: The deserialized content as a Pydantic BaseModel instance or a list of instances.
        """
        if rtype.lower() == "scalar": 
            # Deserialize json (scalar values)
            content_raw = response.json()
            # Pydantic v1
            return model(**content_raw)
        else:
            # Deserialize json
            content_raw = response.json()["value"]
            # Pydantic v1
            # return parse_obj_as(list[model], content_raw)
            return [dict(data) for data in parse_obj_as(list[model], content_raw)]

    # ASSETS
    def list_assets(self, fid: str, save_as: str | None = None) -> Response:
        """
        Retrieves a list of all assets from the UiPath Orchestrator.

        Args:
            fid (str): The folder ID for the organization unit.
            save_as (str, optional): The file path where the JSON content will be saved. 
                                     If None, the content will not be saved.

        Returns:
            Response: A dataclass containing the status code and the list of assets.
        """
        self.__logger.info(msg="Gets a list of all assets")

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/Assets"

        # Pydantic output data structure
        class DataStructure(BaseModel):
            id: int = Field(alias="Id")
            name: str = Field(alias="Name")
            external_name: str | None = Field(alias="ExternalName", default=None)
            has_default_value: bool = Field(alias="HasDefaultValue")
            value: str = Field(alias="Value")
            value_scope: str = Field(alias="ValueScope")
            value_type: str = Field(alias="ValueType")
            int_value: int = Field(alias="IntValue")
            string_value: str = Field(alias="StringValue")
            bool_value: bool = Field(alias="BoolValue")
            credential_username: str = Field(alias="CredentialUsername")
            credential_store_id: int | None = Field(alias="CredentialStoreId", default=None)
            can_be_deleted: bool = Field(alias="CanBeDeleted")
            description: str | None = Field(alias="Description", default=None)

        # Query parameters
        # Pydantic v1
        alias_list = [field.alias for field in DataStructure.__fields__.values() if field.field_info.alias is not None]
        params = {"$select": ",".join(alias_list)}

        # Request
        response = self.__session.get(url=url_query, headers=headers, params=params, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")

            # Export response to json file
            self._export_to_json(content=response.content, save_as=save_as)

            # Deserialize json (scalar values)
            content = self._handle_response(response=response, model=DataStructure, rtype="list")

        return self.Response(status_code=response.status_code, content=content)

    # BUCKETS
    def list_buckets(self, fid: str, save_as: str | None = None) -> Response:
        """
        Buckets - Get all.
        Gets the UiPath Orchestrator buckets.

        Args:
            fid (str): The folder ID for the organization unit.
            save_as (str, optional): The file path where the JSON content will be saved. 
                                     If None, the content will not be saved.

        Returns:
            Response: A dataclass containing the status code and the list of buckets.
        """
        self.__logger.info(msg="Gets a list of all buckets")

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/Buckets"

        # Pydantic output data structure
        class DataStructure(BaseModel):
            id: int = Field(alias="Id")
            identifier: str = Field(alias="Identifier")
            name: str = Field(alias="Name")
            description: str | None = Field(alias="Description", default=None)
        
        # Query parameters
        # Pydantic v1
        alias_list = [field.alias for field in DataStructure.__fields__.values() if field.field_info.alias is not None]
        params = {"$select": ",".join(alias_list)}

        # Request
        response = self.__session.get(url=url_query, headers=headers, params=params, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")

            # Export response to json file
            self._export_to_json(content=response.content, save_as=save_as)

            # Deserialize json (scalar values)
            content = self._handle_response(response=response, model=DataStructure, rtype="list")

        return self.Response(status_code=response.status_code, content=content)

    def create_bucket(self, fid: str, name: str, identifier: str, description: str | None = None) -> Response:
        """
        Creates a new Storage Bucket in UiPath Orchestrator.
        GUID generator: https://www.guidgenerator.com/online-guid-generator.aspx

        Args:
            fid (str): The folder ID for the organization unit.
            name (str): The name of the Storage Bucket.
            identifier (str): The unique identifier (GUID) for the Storage Bucket.
            description (str, optional): A description for the Storage Bucket. Defaults to None.

        Returns:
            Response: A dataclass containing the status code and the response content.
        """
        self.__logger.info(msg="Create bucket")
        self.__logger.info(msg=name)

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}
        
        # Description
        description = "" if description is None else description

        # Request query
        url_query = fr"{url_base}/odata/Buckets"

        # Body
        body = {"Name": name,
                "Description": description,
                "Identifier": identifier,
                "StorageProvider": None,
                "StorageParameters": None,
                "StorageContainer": None,
                "CredentialStoreId": None,
                "ExternalName": None,
                "Password": None,
                "FoldersCount": 0,
                "Id": 0}
        
        # Request
        response = self.__session.post(url=url_query, json=body, headers=headers, verify=True)
        
        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        content = None
        if response.status_code == 201:
            self.__logger.info(msg="Request successful")

        return self.Response(status_code=response.status_code, content=content)

    def upload_bucket_file(self, fid: str, id: str, localpath: str, remotepath: str) -> Response:
        """
        Uploads a file to a Storage Bucket.

        Args:
            fid (str): The folder ID for the organization unit.
            id (str): Storage bucket ID (example: 2).
            localpath (str): The local file to copy.
            remotepath (str): File name in Storage Bucket.
              Example: remotepath="PR123.json".

        Returns:
            Response: A dataclass containing the status code and the response content.
        """
        self.__logger.info(msg="Uploads file to bucket")
        self.__logger.info(msg=id)
        self.__logger.info(msg=localpath)
        self.__logger.info(msg=remotepath)

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/Buckets({id})/UiPath.Server.Configuration.OData.GetWriteUri?path={remotepath}&expiryInMinutes=0"
        
        # Request
        response = self.__session.get(url=url_query, headers=headers, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            # Extract URI
            uri = response.json()["Uri"]
            # Body
            with open(file=localpath, mode="rb") as file:
                # Upload file
                headers = {"x-ms-blob-type": "BlockBlob"}
                response = self.__session.put(url=uri, headers=headers, data=file, verify=True)

        return self.Response(status_code=response.status_code, content=content)

    def delete_bucket_file(self, fid: str, id: str, filename: str) -> Response:
        """
        Deletes a file from a Storage Bucket.

        Args:
            fid (str): The folder ID for the organization unit.
            id (str): Storage bucket ID.
            filename (str): The name of the file to delete.

        Returns:
            Response: A dataclass containing the status code and the response content.
        """
        self.__logger.info(msg="Delete bucket file")
        self.__logger.info(msg=filename)
        
        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/Buckets({id})/UiPath.Server.Configuration.OData.DeleteFile?path={filename}"

        # Request
        response = self.__session.delete(url=url_query, headers=headers, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 204:
            self.__logger.info(msg="Request successful")

        return self.Response(status_code=response.status_code, content=content)

    # CALENDARS
    def list_calendars(self, fid: str, save_as: str | None = None) -> Response:
        """
        Gets the UiPath Orchestrator calendars.

        Args:
            fid (str): The folder ID for the organization unit.
            save_as (str, optional): The file path where the JSON content will be saved. 
                                     If None, the content will not be saved.

        Returns:
            Response: A dataclass containing the status code and the list of calendars.
        """
        self.__logger.info(msg="Gets a list of all calendars")

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/Calendars"

        # Pydantic output data structure
        class DataStructure(BaseModel):
            id: int = Field(alias="Id")
            name: str = Field(alias="Name")
            excluded_dates: list = Field(alias="ExcludedDates")
            time_zone_id: str | None = Field(alias="TimeZoneId", default=None)

        # Query parameters
        # Pydantic v1
        alias_list = [field.alias for field in DataStructure.__fields__.values() if field.field_info.alias is not None]
        params = {"$select": ",".join(alias_list)}

        # Request
        response = self.__session.get(url=url_query, headers=headers, params=params, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")

            # Export response to json file
            self._export_to_json(content=response.content, save_as=save_as)

            # Deserialize json (scalar values)
            content = self._handle_response(response=response, model=DataStructure, rtype="list")

        return self.Response(status_code=response.status_code, content=content)

    # ENVIRONMENTS
    def list_environments(self, fid: str, save_as: str | None = None) -> Response:
        """
        Gets the UiPath Orchestrator environments.

        Args:
            fid (str): The folder ID for the organization unit.
            save_as (str, optional): The file path where the JSON content will be saved. 
                                     If None, the content will not be saved.

        Returns:
            Response: A dataclass containing the status code and the list of environments.
        """
        self.__logger.info(msg="Gets a list of all environments")

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/Environments"

        # Pydantic output data structure
        class DataStructure(BaseModel):
            id: int = Field(alias="Id")
            name: str = Field(alias="Name")
            type: str = Field(alias="Type")
            description: str | None = Field(alias="Description", default=None)

        # Query parameters
        # Pydantic v1
        alias_list = [field.alias for field in DataStructure.__fields__.values() if field.field_info.alias is not None]
        params = {"$select": ",".join(alias_list)}

        # Request
        response = self.__session.get(url=url_query, headers=headers, params=params, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")

            # Export response to json file
            self._export_to_json(content=response.content, save_as=save_as)

            # Deserialize json (scalar values)
            content = self._handle_response(response=response, model=DataStructure, rtype="list")

        return self.Response(status_code=response.status_code, content=content)

    # JOBS
    def list_jobs(self, fid: str, filter: str, save_as: str | None = None) -> Response:
        """
        Gets UiPath Orchestrator jobs.
        Filter use connetion: https://www.odata.org/documentation/odata-version-2-0/uri-conventions/

        Args:
            fid (str): The folder ID for the organization unit.
            filter (str): Condition to be used. Example: State eq 'Running'.
            save_as (str, optional): Name of the JSON file that contains the request response.

        Returns:
            Response: A dataclass containing the status code and the list of jobs.
        """
        self.__logger.info(msg="Gets a list of all jobs based on the applied filter")
        self.__logger.info(msg=filter)

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/Jobs"

        # Pydantic output data structure
        class DataStructure(BaseModel):
            id: int = Field(alias="Id")
            key: str = Field(alias="Key")
            release_name: str = Field(alias="ReleaseName")
            host_machine_name: str | None = Field(alias="HostMachineName", default=None)
            type: str = Field(alias="Type")
            starting_schedule_id: int | None = Field(alias="StartingScheduleId", default=None)
            creation_time: datetime | None = Field(alias="CreationTime", default=None)
            start_time: datetime | None = Field(alias="StartTime", default=None)
            end_time: datetime | None = Field(alias="EndTime", default=None)
            state: str = Field(alias="State")
            source: str = Field(alias="Source")

        # Query parameters
        # Pydantic v1
        alias_list = [field.alias for field in DataStructure.__fields__.values() if field.field_info.alias is not None]
        params = {"$select": ",".join(alias_list), "$filter": filter}

        # Request
        response = self.__session.get(url=url_query, headers=headers, params=params, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")

            # Export response to json file
            self._export_to_json(content=response.content, save_as=save_as)

            # Deserialize json (scalar values)
            content = self._handle_response(response=response, model=DataStructure, rtype="list")

        return self.Response(status_code=response.status_code, content=content)

    def start_job(self, fid: str, robot_id: int, process_key: str) -> Response:
        """
        Starts a job using a process key and a robot id.

        Args:
            fid (str): The folder ID for the organization unit.
            robot_id (int): Robot ID code.
            process_key (str): Process key.

        Returns:
            Response: A dataclass containing the status code and the response content.
        """
        self.__logger.info(msg="Starts the job on a robot")
        self.__logger.info(msg=process_key)
        self.__logger.info(msg=robot_id)

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs"

        # Body
        # case-sensitive
        # Strategy field - This dictates how the process should be run and has
        # 3 options:
        #  * Specific - The process will run on a specific set of robots, whose
        #               IDs are indicated in the RobotIds field.
        #  * JobsCount - The process will run x times, where x is the value of
        #                the JobsCount field. Use this strategy if
        #                you don't care on which robots the job runs.
        #                Orchestrator will automatically allocate the work
        #                to any available robots.
        #  * All - The process will run once on all robots.
        # Source: Manual, Time Trigger, Agent, Queue Trigger
        body = {"startInfo": {"ReleaseKey": process_key,
                              "Strategy": "Specific",
                              "RobotIds": [robot_id],
                              "JobsCount": 0,
                              "Source": "Manual"}}

        # Request
        response = self.__session.post(url=url_query, json=body, headers=headers, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        return self.Response(status_code=response.status_code, content=None)

    def stop_job(self, fid: str, id: str) -> Response:
        """
        Stops a job using a job id.

        Args:
            fid (str): The folder ID for the organization unit.
            id (str): Job Id.

        Returns:
            Response: A dataclass containing the status code and the response content.
        """
        self.__logger.info(msg="Stops a job")
        self.__logger.info(msg=id)

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/Jobs({id})/UiPath.Server.Configuration.OData.StopJob"

        # Body
        body = {"strategy": "2"}

        # Request
        response = self.__session.post(url=url_query, json=body, headers=headers, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")
            
        return self.Response(status_code=response.status_code, content=content)

    # MACHINES
    def list_machines(self, fid: str, save_as: str | None = None) -> Response:
        """
        Machines - Get all.
        Gets the machines from the UiPath Orchestrator.

        Args:
            fid (str): The folder ID for the organization unit.
            save_as (str, optional): Name of the JSON file that contains the request response.

        Returns:
            Response: A dataclass containing the status code and the list of machines.
        """
        self.__logger.info(msg="Gets a list of all machines")

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/Machines"

        # Pydantic output data structure
        class DataStructure(BaseModel):
            id: int = Field(alias="Id")
            name: str = Field(alias="Name")
            description: str | None = Field(alias="Description", default=None)
            type: str = Field(alias="Type")
            non_production_slots: int = Field(alias="NonProductionSlots")
            unattended_slots: int = Field(alias="UnattendedSlots")
            robot_versions: str | None = Field(alias="RobotVersions", default=None)

            # @field_validator("RobotVersions", mode="before")
            # @classmethod
            @validator("robot_versions", pre=True)
            def extract_robot_version(cls, value):
                # if len(value) > 0:
                #     return value[0]["Version"]
                if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                    return value[0].get("Version")
                return None

        # Query parameters
        # Pydantic v1
        alias_list = [field.alias for field in DataStructure.__fields__.values() if field.field_info.alias is not None]
        params = {"$select": ",".join(alias_list)}

        # Request
        response = self.__session.get(url=url_query, headers=headers, params=params, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")

            # Export response to json file
            self._export_to_json(content=response.content, save_as=save_as)

            # Deserialize json
            content = self._handle_response(response=response, model=DataStructure, rtype="list")

        return self.Response(status_code=response.status_code, content=content)

    # PROCESSES
    def list_processes(self, fid: str, save_as: str | None = None) -> Response:
        """
        Gets UiPath Orchestrator processes.

        Args:
            fid (str): The folder ID for the organization unit.
            save_as (str, optional): Name of the JSON file that contains the request response.

        Returns:
            Response: A dataclass containing the status code and the list of processes.
        """
        self.__logger.info(msg="Gets a list of all processes")

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/Processes"

        # Pydantic output data structure
        class DataStructure(BaseModel):
            id: str = Field(alias="Id")
            version: str = Field(alias="Version")
            published: datetime = Field(alias="Published")
            authors: str = Field(alias="Authors")
            description: str | None = Field(alias="Description", default=None)

        # Query parameters
        # Pydantic v1
        alias_list = [field.alias for field in DataStructure.__fields__.values() if field.field_info.alias is not None]
        params = {"$select": ",".join(alias_list)}

        # Request
        response = self.__session.get(url=url_query, headers=headers, params=params, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")

            # Export response to json file
            self._export_to_json(content=response.content, save_as=save_as)

            # Deserialize json
            content = self._handle_response(response=response, model=DataStructure, rtype="list")

        return self.Response(status_code=response.status_code, content=content)

    # QUEUES
    def list_queues(self, fid: str, save_as: str | None = None) -> Response:
        """
        Retrieves all queues from the UiPath Orchestrator.

        Args:
            fid (str): The folder ID for the organization unit.
            save_as (str, optional): The file path where the JSON content will be saved. 
                                     If None, the content will not be saved.

        Returns:
            Response: A dataclass containing the status code and the list of queues.
        """
        self.__logger.info(msg="Gets a list of all queues")

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base
        
        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/QueueDefinitions"

        # Pydantic output data structure
        class DataStructure(BaseModel):
            id: int = Field(alias="Id")
            name: str = Field(alias="Name")
            description: str | None = Field(alias="Description", default=None)

        # Query parameters
        # Pydantic v1
        alias_list = [field.alias for field in DataStructure.__fields__.values() if field.field_info.alias is not None]
        params = {"$select": ",".join(alias_list)}

        # Request
        response = self.__session.get(url=url_query, headers=headers, params=params, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")

            # Export response to json file
            self._export_to_json(content=response.content, save_as=save_as)

            # Deserialize json
            content = self._handle_response(response=response, model=DataStructure, rtype="list")

        return self.Response(status_code=response.status_code, content=content)

    def list_queue_items(self, fid: str, filter: str, save_as: str | None = None) -> Response:
        """
        Retrieves all queue items from the UiPath Orchestrator based on the specified filter.

        Args:
            fid (str): The folder ID for the organization unit.
            filter (str): The filter condition to select the queue and item status.
                          Example: "QueueDefinitionId eq 1 and Status eq 'New'"
            save_as (str, optional): The file path where the JSON content will be saved.
                                     If None, the content will not be saved.

        Returns:
            Response: A dataclass containing the status code and the list of queue items.
        """
        self.__logger.info(msg="Gets a list of queue items using filter")
        self.__logger.info(msg=filter)

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/QueueItems"

        # Pydantic output data structure
        class DataStructure(BaseModel):
            id: int = Field(alias="Id")
            queue_definition_id: int = Field(alias="QueueDefinitionId")
            status: str = Field(alias="Status")
            reference: str = Field(alias="Reference")
            creation_time: datetime = Field(alias="CreationTime")
            start_processing: datetime | None = Field(alias="StartProcessing", default=None)
            end_processing: datetime | None = Field(alias="EndProcessing", default=None)
            retry_number: int = Field(alias="RetryNumber")
            specific_data: str = Field(alias="SpecificData")

        # Query parameters
        # Pydantic v1
        alias_list = [field.alias for field in DataStructure.__fields__.values() if field.field_info.alias is not None]
        params = {"$select": ",".join(alias_list), "$filter": filter}

        # Request
        response = self.__session.get(url=url_query, headers=headers, params=params, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")

            # Export response to json file
            self._export_to_json(content=response.content, save_as=save_as)

            # Deserialize json
            content = self._handle_response(response=response, model=DataStructure, rtype="list")

        return self.Response(status_code=response.status_code, content=content)

    def get_queue_item(self, fid: str, id: int, save_as: str | None = None) -> Response:
        """
        Retrieves the details of a specific queue item from the UiPath Orchestrator.

        Args:
            fid (str): The folder ID for the organization unit.
            id (int): The ID of the queue item to retrieve.
            save_as (str, optional): The file path where the JSON content will be saved. 
                                     If None, the content will not be saved.

        Returns:
            Response: A dataclass containing the status code and the details of the queue item.
        """
        self.__logger.info(msg="Gets queue item details from queue")
        self.__logger.info(msg=id)

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/QueueItems({id})"

        # Pydantic output data structure
        class DataStructure(BaseModel):
            id: int = Field(alias="Id")
            queue_definition_id: int = Field(alias="QueueDefinitionId")
            status: str = Field(alias="Status")
            reference: str = Field(alias="Reference")
            creation_time: datetime = Field(alias="CreationTime")
            start_processing: datetime | None = Field(alias="StartProcessing", default=None)
            end_processing: datetime | None = Field(alias="EndProcessing", default=None)
            retry_number: int = Field(alias="RetryNumber")
            specific_data: str = Field(alias="SpecificData")

        # Query parameters
        # Pydantic v1
        alias_list = [field.alias for field in DataStructure.__fields__.values() if field.field_info.alias is not None]
        params = {"$select": ",".join(alias_list)}

        # Request
        response = self.__session.get(url=url_query, headers=headers, params=params, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")

            # Export response to json file
            self._export_to_json(content=response.content, save_as=save_as)

            # Deserialize json
            content = self._handle_response(response=response, model=DataStructure, rtype="scalar")
        
        return self.Response(status_code=response.status_code, content=content)

    def add_queue_item(self, fid: str, queue: str, data: dict, reference: str, priority: str = "Normal", save_as: str | None = None) -> Response:
        """
        Adds an item to a UiPath Orchestrator queue.

        Example: add_queue_item(fid="123",
                                queue="ElegibilityQueueNAM",
                                data={"PRCode": "PR1234"},
                                reference="PR1234",
                                priority="Normal")

        Args:
            fid (str): The folder ID for the organization unit.
            queue (str): The name of the queue.
            data (dict): A dictionary containing the item information.
            reference (str): A unique reference for the queue item.
            priority (str, optional): The priority of the queue item. Defaults to "Normal".
            save_as (str, optional): The file path where the JSON content will be saved. 
                                     If None, the content will not be saved.

        Returns:
            Response: A dataclass containing the status code and the response content.
        """

        self.__logger.info(msg="Adds item to queue")
        self.__logger.info(msg=queue)
        self.__logger.info(msg=reference)
        
        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/Queues/UiPathODataSvc.AddQueueItem"

        # Pydantic output data structure
        class DataStructure(BaseModel):
            id: int = Field(alias="Id")
            organization_unit_id: int = Field(alias="OrganizationUnitId")
            queue_definition_id: int = Field(alias="QueueDefinitionId")

        # Query parameters
        # Pydantic v1
        alias_list = [field.alias for field in DataStructure.__fields__.values() if field.field_info.alias is not None]
        params = {"$select": ",".join(alias_list)}

        # Body
        # DueDate: null -> DueDate: None
        body = {"itemData": {"Name": queue,
                             "Priority": priority,  # Normal, High
                             "DeferDate": None,
                             "DueDate": None,
                             "Reference": reference,
                             "SpecificContent": data}}

        # Request
        # .encode("utf-8")
        response = self.__session.post(url=url_query, json=body, headers=headers, params=params, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Unique reference violation
        if response.status_code == 409:
            self.__logger.warning(f"Item with reference {reference} already in the queue")

        # Output
        content = None
        if response.status_code == 201:
            self.__logger.info(msg="Request successful")

            # Export response to json file
            self._export_to_json(content=response.content, save_as=save_as)

            # Deserialize json
            content = self._handle_response(response=response, model=DataStructure, rtype="scalar")
        
        return self.Response(status_code=response.status_code, content=content)

    def update_queue_item(self, fid: str, queue: str, id: int, data: dict) -> Response:
        """
        Updates an item in a UiPath Orchestrator queue.

        Args:
            fid (str): The folder ID for the organization unit.
            queue (str): The name of the queue.
              Example: queue="ElegibilityQueueNAM"
            id (int): The ID of the queue item to update.
              Example: id=1489001
            data (dict): A dictionary containing the updated item information.
              Example: content={"PRCode": "PR1234"}

        Returns:
            Response: A dataclass containing the status code and the response content.
        """
        self.__logger.info(msg="Updates queue item in the queue")
        self.__logger.info(msg=queue)

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/QueueItems({id})"

        # Body
        body = {"Name": queue,
                "Priority": "High",
                "SpecificContent": data,
                "DeferDate": None,
                "DueDate": None,
                "RiskSlaDate": None}

        # Request
        # do not remove encode: data=body.encode("utf-8")
        # test in the future the body: dict and data=json.dumps(body)
        response = self.__session.put(url=url_query, json=body, headers=headers, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")

        return self.Response(status_code=response.status_code, content=content)

    def delete_queue_item(self, fid: str, id: int) -> Response:
        """
        Deletes an item from a UiPath Orchestrator queue.

        Args:
            fid (str): The folder ID for the organization unit.
            id (int): The ID of the queue item to delete.

        Returns:
            Response: A dataclass containing the status code and the response content.
        """
        self.__logger.info(msg="Deletes queue item")
        self.__logger.info(msg=id)

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/QueueItems({id})"

        # Request
        response = self.__session.delete(url=url_query, headers=headers, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 204:
            self.__logger.info(msg="Request successful")

        return self.Response(status_code=response.status_code, content=content)

    # RELEASES
    def list_releases(self, fid: str, save_as: str | None = None) -> Response:
        """
        Retrieves a list of all process releases from the UiPath Orchestrator.

        Args:
            fid (str): The folder ID for the organization unit.
            save_as (str, optional): The file path where the JSON content will be saved.
                                     If None, the content will not be saved.

        Returns:
            Response: A dataclass containing the status code and the list of releases.
        """
        self.__logger.info(msg="Gets list of releases")

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/Releases"

        # Pydantic output data structure
        class DataStructure(BaseModel):
            id: int = Field(alias="Id")
            key: str = Field(alias="Key")
            process_key: str = Field(alias="ProcessKey")
            process_version: str = Field(alias="ProcessVersion")
            environment_id: str | None = Field(alias="EnvironmentId", default=None)

        # Query parameters
        # Pydantic v1
        alias_list = [field.alias for field in DataStructure.__fields__.values() if field.field_info.alias is not None]
        params = {"$select": ",".join(alias_list)}

        # Request
        response = self.__session.get(url=url_query, headers=headers, params=params, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")

            # Export response to json file
            self._export_to_json(content=response.content, save_as=save_as)

            # Deserialize json
            content = self._handle_response(response=response, model=DataStructure, rtype="list")

        return self.Response(status_code=response.status_code, content=content)

    def get_release_process_key(self, fid: str, name: str, save_as: str | None = None) -> Response:
        """
        Retrieves the process key for a given process name from the UiPath Orchestrator.

        Args:
            fid (str): The folder ID for the organization unit.
            name (str): The name of the UiPath Orchestrator process.
            save_as (str, optional): The file path where the JSON content will be saved.
                                     If None, the content will not be saved.

        Returns:
            Response: A dataclass containing the status code and the process key information.
        """
        self.__logger.info(msg="Gets the process key")
        self.__logger.info(msg=name)

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/Releases"

        # Pydantic output data structure
        class DataStructure(BaseModel):
            key: str = Field(alias="Key")

        # Query parameters
        # Pydantic v1
        alias_list = [field.alias for field in DataStructure.__fields__.values() if field.field_info.alias is not None]
        params = {"$select": ",".join(alias_list), "$filter": f"ProcessKey eq '{name}'"}

        # Request
        response = self.__session.get(url=url_query, headers=headers, params=params, verify=True)
        print(response.content)
        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")

            # Export response to json file
            self._export_to_json(content=response.content, save_as=save_as)

            # Deserialize json
            content = self._handle_response(response=response, model=DataStructure, rtype="scalar")
        
        return self.Response(status_code=response.status_code, content=content)

    # ROBOTS
    def list_robots(self, fid: str, save_as: str | None = None) -> Response:
        """
        Retrieves a list of all robots from the UiPath Orchestrator.

        Args:
            fid (str): The folder ID for the organization unit.
            save_as (str, optional): The file path where the JSON content will be saved. 
                                     If None, the content will not be saved.

        Returns:
            Response: A dataclass containing the status code and the list of robots.
        """
        self.__logger.info(msg="Gets a list of all robots")

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/Robots"

        # Pydantic output data structure
        class DataStructure(BaseModel):
            id: int = Field(alias="Id")
            machine_name: str = Field(alias="MachineName")
            name: str = Field(alias="Name")
            username: str = Field(alias="Username")
            type: str = Field(alias="Type")
            robot_environments: str = Field(alias="RobotEnvironments")

        # Query parameters
        # Pydantic v1
        alias_list = [field.alias for field in DataStructure.__fields__.values() if field.field_info.alias is not None]
        params = {"$select": ",".join(alias_list)}

        # Request
        response = self.__session.get(url=url_query, headers=headers, params=params, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")

            # Export response to json file
            self._export_to_json(content=response.content, save_as=save_as)

            # Deserialize json
            content = self._handle_response(response=response, model=DataStructure, rtype="list")

        return self.Response(status_code=response.status_code, content=content)
    
    def list_robot_logs(self, fid: str, filter: str, save_as: str | None = None) -> Response:
        """
        Retrieves a list of robot logs from the UiPath Orchestrator.

        Example: get_robot_logs(fid="123",
                                filter="JobKey eq 'bde11c1e-11e1-1bb1-11d1-e11f111111db'")

        Args:
            fid (str): The folder ID for the organization unit.
            filter (str): The filter condition to apply to the API call.
                          Example: "JobKey eq 'bde11c1e-11e1-1bb1-11d1-e11f111111db'"
            save_as (str, optional): The file path where the JSON content will be saved.
                                     If None, the content will not be saved.

        Returns:
            Response: A dataclass containing the status code and the list of robot logs.
        """
        self.__logger.info(msg="Gets a list of robot logs")

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/RobotLogs"

        # Pydantic output data structure
        class DataStructure(BaseModel):
            id: int = Field(alias="Id")
            job_key: str = Field(alias="JobKey")
            level: str = Field(alias="Level")
            windows_identity: str = Field(alias="WindowsIdentity")
            process_name: str = Field(alias="ProcessName")
            time_stamp: str = Field(alias="TimeStamp")
            message: str = Field(alias="Message")
            robot_name: str = Field(alias="RobotName")
            Machine_id: int = Field(alias="MachineId")

        # Query parameters
        # Pydantic v1
        # ?$top=10
        # last log line for robot X
        #   ?$top=1&$filter=RobotName eq 'Porto_Prod_2'&$orderby=TimeStamp desc
        # ?$filter=Level eq 'Error' or Level eq 'Fatal'
        # ?$filter=Level eq UiPath.Core.Enums.LogLevel%27Fatal%27
        # ?$filter=TimeStamp gt 2021-10-12T00:00:00.000Z and Level eq 'Error' or Level eq 'Fatal'
        # ?$filter=JobKey eq 98f59394-45e7-4da6-a695-50c70f4d87e3
        alias_list = [field.alias for field in DataStructure.__fields__.values() if field.field_info.alias is not None]
        params = {"$select": ",".join(alias_list), "$filter": filter}

        # Request
        response = self.__session.get(url=url_query, headers=headers, params=params, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")

            # Export response to json file
            self._export_to_json(content=response.content, save_as=save_as)

            # Deserialize json
            content = self._handle_response(response=response, model=DataStructure, rtype="list")

        return self.Response(status_code=response.status_code, content=content)

    def get_robot_id(self, fid: str, name: str, save_as: str | None = None) -> Response:
        """
        Retrieves the ID of a robot by its name from the UiPath Orchestrator.

        Args:
            fid (str): The folder ID for the organization unit.
            name (str): The name of the UiPath Orchestrator robot.
            save_as (str, optional): The file path where the JSON content will be saved.
                                     If None, the content will not be saved.

        Returns:
            Response: A dataclass containing the status code and the robot ID information.
        """
        self.__logger.info(msg="Gets the robot id")
        self.__logger.info(msg=name)

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/Robots"

        # Pydantic output data structure
        class DataStructure(BaseModel):
            id: str = Field(alias="Id")

        # Query parameters
        # Pydantic v1
        alias_list = [field.alias for field in DataStructure.__fields__.values() if field.field_info.alias is not None]
        params = {"$select": ",".join(alias_list), "$filter": f"Name eq '{name}'", "$top": 1}

        # Request
        response = self.__session.get(url=url_query, headers=headers, params=params, verify=True)
        print(response.content)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")

            # Export response to json file
            self._export_to_json(content=response.content, save_as=save_as)

            # Deserialize json
            content = self._handle_response(response=response, model=DataStructure, rtype="scalar")
        
        return self.Response(status_code=response.status_code, content=content)

    # ROLES
    def list_roles(self, save_as: str | None = None) -> Response:
        """
        Retrieves a list of all roles from the UiPath Orchestrator.

        Args:
            save_as (str, optional): The file path where the JSON content will be saved.
                                     If None, the content will not be saved.

        Returns:
            Response: A dataclass containing the status code and the list of roles.
        """
        self.__logger.info(msg="Gets a list of all roles")

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}"}
 
        # Request query
        url_query = fr"{url_base}/odata/Roles"

        # Pydantic output data structure
        class DataStructure(BaseModel):
            id: int = Field(alias="Id")
            name: str = Field(alias="Name")
            display_name: str = Field(alias="DisplayName")
            type: str = Field(alias="Type")

        # Query parameters
        # Pydantic v1
        alias_list = [field.alias for field in DataStructure.__fields__.values() if field.field_info.alias is not None]
        params = {"$select": ",".join(alias_list)}

        # Request
        response = self.__session.get(url=url_query, headers=headers, params=params, verify=True)
        print(response.content)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")

            # Export response to json file
            self._export_to_json(content=response.content, save_as=save_as)

            # Deserialize json
            content = self._handle_response(response=response, model=DataStructure, rtype="list")

        return self.Response(status_code=response.status_code, content=content)

    # SCHEDULES
    def list_schedules(self, fid: str, save_as: str | None = None) -> Response:
        """
        Retrieves a list of all schedules from the UiPath Orchestrator.

        Args:
            fid (str): The folder ID for the organization unit.
            save_as (str, optional): The file path where the JSON content will be saved.
                                     If None, the content will not be saved.

        Returns:
            Response: A dataclass containing the status code and the list of schedules.
        """
        self.__logger.info(msg="Gets a list of all schedules")

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/ProcessSchedules"

        # pydantic output data structure
        class DataStructure(BaseModel):
            id: int = Field(alias="Id")
            name: str = Field(alias="Name")
            package_name: str = Field(alias="PackageName")
            environment_id: str | None = Field(alias="EnvironmentId", default=None)
            environment_name: str | None = Field(alias="EnvironmentName", default=None)
            start_process_cron: str = Field(alias="StartProcessCron")
            start_process_cron_summary: str = Field(alias="StartProcessCronSummary")
            enabled: bool = Field(alias="Enabled")

        # Query parameters
        # Pydantic v1
        alias_list = [field.alias for field in DataStructure.__fields__.values() if field.field_info.alias is not None]
        params = {"$select": ",".join(alias_list)}

        # Request
        response = self.__session.get(url=url_query, headers=headers, params=params, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")

            # Export response to json file
            self._export_to_json(content=response.content, save_as=save_as)

            # Deserialize json
            content = self._handle_response(response=response, model=DataStructure, rtype="list")

        return self.Response(status_code=response.status_code, content=content)

    # SESSIONS
    def list_sessions(self, fid: str, save_as: str | None = None) -> Response:
        """
        Retrieves a list of all sessions from the UiPath Orchestrator.

        Args:
            fid (str): The folder ID for the organization unit.
            save_as (str, optional): The file path where the JSON content will be saved.
                                     If None, the content will not be saved.

        Returns:
            Response: A dataclass containing the status code and the list of sessions.
        """
        self.__logger.info(msg="Gets a list of all sessions")

        # Configuration
        token = self.__configuration.token
        url_base = self.__configuration.url_base

        # Request headers
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}",
                   "X-UIPATH-OrganizationUnitID": fid}

        # Request query
        url_query = fr"{url_base}/odata/Sessions"

        # Pydantic output data structure
        class DataStructure(BaseModel):
            id: int = Field(alias="Id")
            machine_id: str = Field(alias="MachineId")
            host_machine_name: str = Field(alias="HostMachineName")
            machine_name: str = Field(alias="MachineName")
            state: str = Field(alias="State")
            reporting_time: str = Field(alias="ReportingTime")
            organization_unit_id: str = Field(alias="OrganizationUnitId")
            folder_name: str = Field(alias="FolderName")

        # Query parameters
        # Pydantic v1
        alias_list = [field.alias for field in DataStructure.__fields__.values() if field.field_info.alias is not None]
        params = {"$select": ",".join(alias_list)}

        # Request
        response = self.__session.get(url=url_query, headers=headers, params=params, verify=True)

        # Log response code
        self.__logger.info(msg=f"HTTP Status Code {response.status_code}")

        # Output
        content = None
        if response.status_code == 200:
            self.__logger.info(msg="Request successful")

            # Export response to json file
            self._export_to_json(content=response.content, save_as=save_as)

            # Deserialize json
            content = self._handle_response(response=response, model=DataStructure, rtype="list")

        return self.Response(status_code=response.status_code, content=content)

# eom
