from slurpit.apis.baseapi import BaseAPI
from slurpit.models.device import Device, Vendor
from slurpit.utils.utils import handle_response_data, deprecated
import httpx

class DeviceAPI(BaseAPI):
    def __init__(self, base_url, api_key, verify):
        """
        Initializes a new instance of DeviceAPI, extending the BaseAPI class.
        Sets up the base URL for API calls specific to devices and initializes authentication.

        Args:
            base_url (str): The root URL for the device-related API endpoints.
            api_key (str): The API key used for authenticating requests.
            verfify (bool): Verify HTTPS Certificates.
        """
        formatted_url = "{}/api".format(base_url if base_url[-1] != "/" else base_url[:-1])  # Format the base URL to ensure it ends with '/api'
        self.base_url = formatted_url  # Set the formatted base URL
        super().__init__(api_key, verify)

    async def get_devices(self, offset: int = 0, limit: int = 1000, export_csv: bool = False, export_df: bool = False):
        """
        Fetches a list of devices from the API with pagination and optionally exports the data to a CSV format or pandas DataFrame.
        
        Args:
            offset (int): The starting index of the records to fetch.
            limit (int): The maximum number of records to return in one call.
            export_csv (bool): If True, returns the device data in CSV format as bytes.
                            If False, returns a list of Device objects.
            export_df (bool): If True, returns the device data as a pandas DataFrame.

        Returns:
            list[Device] | bytes | pd.DataFrame: A list of Device instances, CSV data as bytes if export_csv is True, 
                                                or a pandas DataFrame if export_df is True.
        """
        url = f"{self.base_url}/devices"
        response = await self._pager(url, offset=offset, limit=limit)
        return handle_response_data(response, Device, export_csv, export_df)

    async def get_device(self, device_id: int):
        """
        Fetches a single device by its ID.

        Args:
            device_id (int): The unique identifier of the device to retrieve.

        Returns:
            Device: A Device instance if successful.
        """
        url = f"{self.base_url}/devices/{device_id}"
        response = await self.get(url)
        if response:
            device_data = response.json()
            return Device(**device_data)

    async def update_device(self, device_id: int, update_data: dict):
        """
        Updates a specific device using its ID.

        Args:
            device_id (int): The unique identifier of the device to update.
            update_data (dict): A dictionary containing the updated device attributes. \n
                            The dictionary should include the following keys: \n
                            - "hostname" (str): The hostname of the device.
                            - "fqdn" (str): The fully qualified domain name of the device.
                            - "port" (int): The port number for device communication, typically 22.
                            - "ipv4" (str): The IPv4 address of the device.
                            - "device_os" (str): The operating system running on the device.
                            - "device_type" (str): The type of the device.
                            - "disabled" (int): Status flag where 0 indicates enabled and 1 indicates disabled.

        Returns:
            Device: An updated Device instance if successful.
        """
        url = f"{self.base_url}/devices/{device_id}"
        response = await self.put(url, update_data)
        if response:
            device_data = response.json()
            return Device(**device_data)

    async def create_device(self, device_data: dict):
        """
        Creates a new device in the system.

        Args:
            device_data (dict): A dictionary containing the device attributes. \n
                            The dictionary should include the following keys: \n
                            - "hostname" (str): The hostname of the device.
                            - "fqdn" (str): The fully qualified domain name of the device.
                            - "port" (int): The port number for device communication, typically 22.
                            - "ipv4" (str): The IPv4 address of the device.
                            - "device_os" (str): The operating system running on the device.
                            - "device_type" (str): The type of the device.
                            - "disabled" (int): Status flag where 0 indicates enabled and 1 indicates disabled.

        Returns:
            Device: A newly created Device instance if successful.
        """
        url = f"{self.base_url}/devices"
        response = await self.post(url, device_data)
        if response:
            device_data = response.json()
            return Device(**device_data)

    async def delete_device(self, device_id: int):
        """
        Deletes a device using its ID.

        Args:
            device_id (int): The unique identifier of the device to delete.

        Returns:
            Device: A Device instance representing the deleted device if successful.
        """
        url = f"{self.base_url}/devices/{device_id}"
        response = await self.delete(url)
        if response:
            device_data = response.json()
            return Device(**device_data)

    async def sync_device(self, sync_data: dict):
        """
        Synchronizes a device with the given device data. Inserts or updates a device with the provided data.

        Args:
            sync_data (dict): A dictionary containing the device attributes to be synchronized. \n
                            The dictionary should include the following keys: \n
                            - "hostname" (str): The hostname of the device.
                            - "fqdn" (str): The fully qualified domain name of the device.
                            - "port" (int): The port number for device communication, typically 22.
                            - "ipv4" (str): The IPv4 address of the device.
                            - "device_os" (str): The operating system running on the device.
                            - "device_type" (str): The type of the device.
                            - "disabled" (int): Status flag where 0 indicates enabled and 1 indicates disabled.

        Returns:
            None | Device: None if the synchronization is successful and 'success' is reported by the API, 
                        otherwise returns a Device instance based on the returned data.
        """
        url = f"{self.base_url}/devices/sync"
        response = await self.post(url, sync_data)
        if response:
            sync_result = response.json()
            if 'success' in sync_result:
                return None

            return Device(**sync_result)

    async def get_vendors(self, offset: int = 0, limit: int = 1000, export_csv: bool = False, export_df: bool = False):
        """
        Retrieves a list of vendors from the API and optionally exports the data to a CSV format or pandas DataFrame.
        
        Args:
            offset (int): The starting index of the records to fetch.
            limit (int): The maximum number of records to return in one call.
            export_csv (bool): If True, returns the vendor data in CSV format as bytes.
                            If False, returns a list of Vendor objects.
            export_df (bool): If True, returns the vendor data as a pandas DataFrame.

        Returns:
            list[Vendor] | bytes | pd.DataFrame: A list of Vendor instances, CSV data as bytes if export_csv is True, 
                                                or a pandas DataFrame if export_df is True.
        """
        url = f"{self.base_url}/devices/vendors"
        response = await self._pager(url, offset=offset, limit=limit)
        return handle_response_data(response, Vendor, export_csv, export_df)

    async def get_types(self, offset: int = 0, limit: int = 1000, export_csv: bool = False, export_df: bool = False):
        """
        Retrieves a list of device types from the API and optionally exports the data to CSV format or pandas DataFrame.
        
        Args:
            offset (int): The starting index of the records to fetch.
            limit (int): The maximum number of records to return in one call.
            export_csv (bool): If True, returns the device type data in CSV format as bytes.
                            If False, returns a list of device types as strings.
            export_df (bool): If True, returns the device type data as a pandas DataFrame.

        Returns:
            list[str] | bytes | pd.DataFrame: A list of device types, CSV data as bytes if export_csv is True, 
                                            or a pandas DataFrame if export_df is True.
        """
        url = f"{self.base_url}/devices/types"
        response = await self._pager(url, offset=offset, limit=limit)
        return handle_response_data(response, export_csv=export_csv, export_df=export_df)


    async def get_snapshots(self, hostname: str, export_csv: bool = False, export_df: bool = False):
        """
        Retrieve latest data for a given hostname for all plannings, optionally filtered by date,
        and optionally exports the data to a CSV format or pandas DataFrame.
        
        Args:
            hostname (str): The hostname of the device for which snapshots are required.
            export_csv (bool): If True, returns the snapshot data in CSV format as bytes.
                            If False, returns a list of snapshot data dictionaries.
            export_df (bool): If True, returns the snapshot data as a pandas DataFrame.

        Returns:
            list[dict] | bytes | pd.DataFrame: A list of snapshot data dictionaries, CSV data as bytes if export_csv is True,
                                            or a pandas DataFrame if export_df is True.
        """
        url = f"{self.base_url}/devices/snapshot/all/{hostname}"
        response = await self.get(url)
        return handle_response_data(response, export_csv=export_csv, export_df=export_df)

    async def get_snapshot(self, hostname: str, planning_id: int, batch_id: int):
        """
        Retrieves latest data for a given hostname, planning id and batch id.

        Args:
            hostname (str): The hostname of the device.
            planning_id (int): The planning ID associated with the snapshot.
            batch_id (int): Batch ID, if empty it will use the latest batch id

        Returns:
            dict: Snapshot data as a dictionary if successful.
        """
        url = f"{self.base_url}/devices/snapshot/single/{hostname}/{planning_id}"
        if batch_id:
            url += f"/{batch_id}"
        response = await self.get(url)
        if response:
            snapshot_data = response.json()
            return snapshot_data


    async def get_snapshot_batches(self, hostname: str, planning_id: int):
        """
        Retrieve batch id data for a given hostname.

        Args:
            hostname (str): The hostname of the device.
            planning_id (int): Planning id, if not given it returns data for all planning ids

        Returns:
            dict: Batch id data for a given hostname and planning id.

        """
        url = f"{self.base_url}/devices/snapshot/batches/{hostname}"
        if planning_id:
            url += f"/{planning_id}"
        response = await self.get(url)
        if response:
            snapshot_data = response.json()
            return snapshot_data

    @deprecated("Use test_login() instead")
    async def test_ssh(self, ssh_info: dict):
        """
        Tests SSH connectivity using the provided SSH information.

        Args:
            ssh_info (dict): A dictionary containing the SSH credentials and details. \n
                            The dictionary should include the following keys: \n
                            - "username" (str): The username for SSH login.
                            - "password" (str): The password for SSH login.
                            - "ip" (str): The IP address of the device to connect to.
                            - "port" (int): The port number for SSH communication, typically 22.
                            - "device_os" (str): The operating system running on the device.

        Returns:
            dict: SSH test response as a dictionary if successful.
        """
        url = f"{self.base_url}/devices/test/ssh"
        timeout = httpx.Timeout(connect=10.0, read=60.0, write=60.0, pool=60.0)
        response = await self.post(url, ssh_info, timeout=timeout)
        if response:
            ssh_response = response.json()
            return ssh_response

    async def test_login(self, login_info: dict):
        """
        Tests SSH connectivity using the provided SSH information.

        Args:
            login_info (dict): A dictionary containing the SSH credentials and details. \n
                            The dictionary should include the following keys: \n
                            - "username" (str): The username for SSH login.
                            - "password" (str): The password for SSH login.
                            - "ssh_key" (str): The ssh_key for SSH login.
                            - "ssh_passphrase" (str): The ssh_passphrase for SSH Key logins.
                            - "enable_password" (str): The Enable password.
                            - "host" (str): The IP address of the device to connect to.
                            - "port" (int): The port number for SSH communication, typically 22.
                            - "device_os" (str): The operating system running on the device.

        Returns:
            dict: SSH test response as a dictionary if successful.
        """
        url = f"{self.base_url}/devices/test/login"
        timeout = httpx.Timeout(connect=10.0, read=60.0, write=60.0, pool=60.0)
        response = await self.post(url, login_info, timeout=timeout)
        if response:
            ssh_response = response.json()
            return ssh_response
    
    async def test_reachability(self, host: str, port: int):
        """
        Validate if the device is reachable by the provided port.

        Args:
            - "host" (str): The IP address of the device to connect to.
            - "port" (int): The port number for SSH communication, typically 22 or 23.

        Returns:
            dict: Reachability test response as a dictionary if successful.
        """
        url = f"{self.base_url}/devices/test/reachability/{host}/{port}"
        timeout = httpx.Timeout(connect=10.0, read=60.0, write=60.0, pool=60.0)

        response = await self.get(url, timeout=timeout)
        if response:
            reachability_response = response.json()
            return reachability_response