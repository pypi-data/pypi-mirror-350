from slurpit.apis.baseapi import BaseAPI
from slurpit.models.scanner import Node
from slurpit.utils.utils import handle_response_data
import httpx

class ScannerAPI(BaseAPI):
    def __init__(self, base_url, api_key, verify):
        """
        Initialize the ScannerAPI with the base URL of the API and an API key for authentication.
        
        Args:
            base_url (str): The root URL for the API endpoints.
            api_key (str): The API key used for authenticating requests.
            verfify (bool): Verify HTTPS Certificates.
        """
        formatted_url = "{}/api".format(base_url if base_url[-1] != "/" else base_url[:-1])  # Format the base URL to ensure it ends with '/api'
        self.base_url = formatted_url  # Set the formatted base URL
        super().__init__(api_key, verify)  # Initialize the parent class with the API key

    async def get_nodes(self, batch_id: int, offset: int = 0, limit: int = 1000, export_csv: bool = False, export_df: bool = False):
        """
        Retrieves a list of nodes based on the batch_id with pagination options and optionally exports the data to CSV format or pandas DataFrame.

        Args:
            batch_id (int): The batch identifier to filter nodes.
            offset (int): The starting index for pagination.
            limit (int): The maximum number of nodes to return.
            export_csv (bool): If True, returns the nodes data in CSV format as bytes.
            export_df (bool): If True, returns the nodes data as a pandas DataFrame.

        Returns:
            list[dict] | bytes | pd.DataFrame: A list of nodes, CSV data as bytes if export_csv is True, 
                                            or a pandas DataFrame if export_df is True.
        """
        url = f"{self.base_url}/scanner/{batch_id}"
        response = await self._pager(url, offset=offset, limit=limit, paged_value="nodes")
        return handle_response_data(response, export_csv=export_csv, export_df=export_df)

    async def get_finders(self, offset: int = 0, limit: int = 1000, export_csv: bool = False, export_df: bool = False):
        """
        Retrieves a list of configured finders from the scanner API and optionally exports the data to CSV format or pandas DataFrame.

        Args:
            offset (int): The starting index of the records to fetch.
            limit (int): The maximum number of records to return in one call.
            export_csv (bool): If True, returns the finders data in CSV format as bytes.
            export_df (bool): If True, returns the finders data as a pandas DataFrame.

        Returns:
            list[dict] | bytes | pd.DataFrame: A list of finders, CSV data as bytes if export_csv is True,
                                            or a pandas DataFrame if export_df is True.
        """
        url = f"{self.base_url}/scanner/configured/finders"
        response = await self._pager(url, offset=offset, limit=limit)
        return handle_response_data(response, export_csv=export_csv, export_df=export_df)

    async def get_crawlers(self, offset: int = 0, limit: int = 1000, export_csv: bool = False, export_df: bool = False):
        """
        Retrieves a list of configured crawlers from the scanner API and optionally exports the data to CSV format or pandas DataFrame.

        Args:
            offset (int): The starting index of the records to fetch.
            limit (int): The maximum number of records to return in one call.
            export_csv (bool): If True, returns the crawlers data in CSV format as bytes.
            export_df (bool): If True, returns the crawlers data as a pandas DataFrame.

        Returns:
            list[dict] | bytes | pd.DataFrame: A list of crawlers, CSV data as bytes if export_csv is True,
                                            or a pandas DataFrame if export_df is True.
        """
        url = f"{self.base_url}/scanner/configured/crawlers"
        response = await self._pager(url, offset=offset, limit=limit)
        return handle_response_data(response, export_csv=export_csv, export_df=export_df)

    async def start_scanner(self, scanner_data: dict):
        """
        Starts a scanning process with provided scanner configuration data.

        Args:
            scanner_data (dict): A dictionary containing the scanner configuration data. \n
                                The dictionary should include the following keys: \n
                                - "target" (str): The target to be scanned.
                                - "version" (str): The SNMP version, e.g., "snmpv2c".
                                - "batch_id" (int): The batch ID for the scanning process.
                                - "snmpv2c_key" (str): The SNMPv2c community string.
                                - "snmpv3_username" (str): The SNMPv3 username.
                                - "snmpv3_authkey" (str): The SNMPv3 authentication key.
                                - "snmpv3_authtype" (list of str): The SNMPv3 authentication types, possible values are ["none", "md5", "sha", "sha224", "sha256", "sha384", "sha512"].
                                - "snmpv3_privkey" (str): The SNMPv3 privacy key.
                                - "snmpv3_privtype" (list of str): The SNMPv3 privacy types, possible values are ["none", "des", "3des", "aes128", "aes192", "aes256", "aesblumenthal192", "aesblumenthal256"].

        Returns:
            dict: Status of the scanning process if successful.
        """
        url = f"{self.base_url}/scanner"
        response = await self.post(url, scanner_data)
        if response:
            scanner_status = response.json()
            return scanner_status

    async def clean_logging(self, datetime: str):
        """
        Triggers a cleaning process for scanner logs older than the specified datetime.

        Returns:
            dict: Result of the cleaning process if successful.
        """
        url = f"{self.base_url}/scanner/clean"
        request_data = {"datetime": datetime}
        response = await self.post(url, request_data)
        if response:
            clean_result = response.json()
            return clean_result

    async def get_status(self):
        """
        Retrieves the current status of the scanner.

        Returns:
            dict: The current status of the scanner if successful.
        """
        url = f"{self.base_url}/scanner/status"
        response = await self.get(url)
        if response:
            status_result = response.json()
            return status_result

    async def test_snmp(self, ip_data: dict):
        """
        Tests SNMP configuration by attempting to gather device information from the specified IP.

        Args:
            ip_data (dict): A dictionary containing the SNMP configuration details. \n
                            The dictionary should include the following keys: \n
                            - "ip" (str): The IP address of the device to connect to.
                            - "version" (str): The SNMP version, e.g., "snmpv2c".
                            - "snmpv2c_key" (str): The SNMPv2c community string.
                            - "snmpv3_username" (str): The SNMPv3 username.
                            - "snmpv3_authkey" (str): The SNMPv3 authentication key.
                            - "snmpv3_authtype" (list of str): The SNMPv3 authentication types, possible values are ["none", "md5", "sha", "sha224", "sha256", "sha384", "sha512"].
                            - "snmpv3_privkey" (str): The SNMPv3 privacy key.
                            - "snmpv3_privtype" (list of str): The SNMPv3 privacy types, possible values are ["none", "des", "3des", "aes128", "aes192", "aes256", "aesblumenthal192", "aesblumenthal256"].

        Returns:
            dict: Device information gathered via SNMP if successful.
        """
        url = f"{self.base_url}/scanner/test"
        timeout = httpx.Timeout(connect=10.0, read=60.0, write=60.0, pool=60.0)
        response = await self.post(url, ip_data, timeout=timeout)
        if response:
            device_info = response.json()
            return device_info

    async def get_queue_list(self, export_csv: bool = False, export_df: bool = False):
        """
        Gives a list of currently queued tasks for the scanner.

        Args:
            export_csv (bool): If True, returns the queued tasks data in CSV format as bytes. If False, returns list of queued tasks.
            export_df (bool): If True, returns the crawlers data as a pandas DataFrame.

        Returns:
            list[dict] | bytes: A list of queued tasks or CSV data as bytes if export_csv is True.
        """
        url = f"{self.base_url}/scanner/queue/list"
        response = await self.post(url, None)
        return handle_response_data(response, export_csv=export_csv, export_df=export_df)
    
    async def clear_queue(self):
        """
        Clears the queue of the scanner by sending a DELETE request to the queue list endpoint.

        Returns:
            dict: The result of clearing the queue if successful.
        """
        url = f"{self.base_url}/scanner/queue/clear"
        response = await self.delete(url)
        if response:
            clear_result = response.json()
            return clear_result