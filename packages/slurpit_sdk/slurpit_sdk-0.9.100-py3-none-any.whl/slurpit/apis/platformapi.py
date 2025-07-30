from slurpit.apis.baseapi import BaseAPI
from slurpit.models.platform import Platform, PlatformLicense
from slurpit.utils.utils import handle_response_data

class PlatformAPI(BaseAPI):
    def __init__(self, base_url, api_key, verify):
        """
        Initializes a new instance of the PlatformAPI class, which extends BaseAPI. This class is designed to interact with platform-related endpoints of an API.

        Args:
            base_url (str): The root URL for the API endpoints.
            api_key (str): The API key used for authenticating requests.
            verfify (bool): Verify HTTPS Certificates.
        """
        formatted_url = "{}/api".format(base_url if base_url[-1] != "/" else base_url[:-1])  # Format the base URL to ensure it ends with '/api'
        self.base_url = formatted_url  # Set the formatted base URL
        super().__init__(api_key, verify)

    async def license(self):
        """
        Retrieves a list of the current license status

        Returns:
            PlatformLicense: A PlatformLicense object initialized with the data from the API response if the request is successful.
        """
        url = f"{self.base_url}/platform/license" 
        response = await self.get(url)
        if response:
            platform_data = response.json()  
            return PlatformLicense(**platform_data)
        
    async def ping(self):
        """
        Sends a 'ping' request to the platform's ping endpoint to check connectivity and retrieve platform information.

        Returns:
            Platform: A Platform object initialized with the data from the API response if the request is successful.
        """
        url = f"{self.base_url}/platform/ping" 
        response = await self.get(url)
        if response:
            platform_data = response.json()  
            return Platform(**platform_data)
    
    async def version(self):
        """
        Returns the current installed Slurp'it version.

        Returns:
            dict: A dictionary initialized with the data from the Version response if the request is successful.
        """
        url = f"{self.base_url}/platform/version" 
        response = await self.get(url)
        if response:
            platform_data = response.json()  
            return platform_data  
    
    async def scraper_connectivity(self):
        """
        Test the Scraper (Data Collector) connectivity.

        Returns:
            Platform: A Platform object initialized with the data from the Service Status response if the request is successful (online/offline).
        """
        url = f"{self.base_url}/platform/scraper_connectivity" 
        response = await self.get(url)
        if response:
            platform_data = response.json()  
            return Platform(**platform_data)
    
    async def scanner_connectivity(self):
        """
        Test the Scanner (Device Finder) connectivity.

        Returns:
            Platform: A Platform object initialized with the data from the Service Status response if the request is successful (online/offline).
        """
        url = f"{self.base_url}/platform/scanner_connectivity" 
        response = await self.get(url)
        if response:
            platform_data = response.json()  
            return Platform(**platform_data)

    async def warehouse_connectivity(self):
        """
        Test the Warehouse connectivity.

        Returns:
            Platform: A Platform object initialized with the data from the Service Status response if the request is successful (online/offline).
        """
        url = f"{self.base_url}/platform/warehouse_connectivity" 
        response = await self.get(url)
        if response:
            platform_data = response.json()  
            return Platform(**platform_data)
    
    async def warehouse_db_size(self):
        """
        Get the Scraper (Data Collector) DB (MongoDB) size in MB

        Returns:
            Platform: A Platform object initialized with the data from the Warehouse DB Size response if the request is successful.
        """
        url = f"{self.base_url}/platform/warehouse_db_size" 
        response = await self.get(url)
        if response:
            platform_data = response.json()  
            return Platform(**platform_data)  