from slurpit.apis.baseapi import BaseAPI
from slurpit.models.vault import Vault, SingleVault
from slurpit.utils.utils import handle_response_data

class VaultAPI(BaseAPI):
    def __init__(self, base_url, api_key, verify):
        """
        Initializes a new instance of the VaultAPI class.

        Args:
            base_url (str): The base URL for the Vault API.
            api_key (str): The API key used for authentication.
            verfify (bool): Verify HTTPS Certificates.
        """
        formatted_url = "{}/api".format(base_url if base_url[-1] != "/" else base_url[:-1])  # Format the base URL to ensure it ends with '/api'
        self.base_url = formatted_url  # Set the formatted base URL
        super().__init__(api_key, verify)  # Initializes the BaseAPI with the provided API key

    async def get_vaults(self, offset: int = 0, limit: int = 1000, export_csv: bool = False, export_df: bool = False):
        """
        Fetches a list of all vaults from the API and returns them as a list of Vault objects.
        Optionally exports the data to a CSV format or pandas DataFrame if specified.

        Args:
            offset (int): The starting index of the records to fetch.
            limit (int): The maximum number of records to return in one call.
            export_csv (bool): If True, returns the vault data in CSV format as bytes.
            export_df (bool): If True, returns the vault data as a pandas DataFrame.

        Returns:
            list[Vault] | bytes | pd.DataFrame: Returns a list of Vault objects if successful, bytes if exporting to CSV,
                                            or a pandas DataFrame if exporting to DataFrame.
        """
        url = f"{self.base_url}/vault"
        response = await self._pager(url, offset=offset, limit=limit)
        return handle_response_data(response, Vault, export_csv, export_df)
        
    async def get_vault(self, vault_id: int):
        """
        Fetches a single vault by its ID.

        Args:
            vault_id (int): The ID of the vault to retrieve.

        Returns:
            SingleVault: Returns a SingleVault object if the fetch is successful.
        """
        url = f"{self.base_url}/vault/{vault_id}"
        response = await self.get(url)
        if response:
            vault_data = response.json()
            return SingleVault(**vault_data)
    
    async def update_vault(self, vault_id: int, update_data: dict):
        """
        Updates a vault with specified data.

        Args:
            vault_id (int): The ID of the vault to update.
            update_data (dict): A dictionary containing the data to update in the vault. \n
                                The dictionary should include the following keys: \n
                                - "username" (str): The username for the vault.
                                - "password" (str): The password for the vault.
                                - "default" (int): A flag indicating whether this is the default vault (0 for no, 1 for yes).
                                - "device_os" (str): The operating system associated with the vault.
                                - "comment" (str): Any additional comments or notes about the vault.

        Returns:
            SingleVault: Returns a SingleVault object if the update is successful.
        """
        url = f"{self.base_url}/vault/{vault_id}"
        response = await self.put(url, update_data)
        if response:
            vault_data = response.json()
            return SingleVault(**vault_data)
    
    async def create_vault(self, new_vault: dict):
        """
        Creates a new vault with the specified data.

        Args:
            new_vault (dict): A dictionary containing the data for the new vault. \n
                            The dictionary should include the following keys: \n
                            - "username" (str): The username for the vault.
                            - "password" (str): The password for the vault.
                            - "default" (int): A flag indicating whether this is the default vault (0 for no, 1 for yes).
                            - "device_os" (str): The operating system associated with the vault.
                            - "comment" (str): Any additional comments or notes about the vault.

        Returns:
            SingleVault: Returns a SingleVault object if the creation is successful.
        """
        url = f"{self.base_url}/vault"
        response = await self.post(url, new_vault)
        if response:
            vault_data = response.json()
            return SingleVault(**vault_data)
    
    async def delete_vault(self, vault_id: int):
        """
        Deletes a vault by its ID.

        Args:
            vault_id (int): The ID of the vault to delete.

        Returns:
            SingleVault: Returns a SingleVault object if the deletion is successful.
        """
        url = f"{self.base_url}/vault/{vault_id}"
        response = await self.delete(url)
        if response:
            vault_data = response.json()
            return SingleVault(**vault_data)