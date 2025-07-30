from slurpit.models.basemodel import BaseModel

class Vault(BaseModel):
    """
    Vault class epresents a vault storing sensitive user data.

    Args:
        id (int): The unique identifier for the vault.
        username (str): The username associated with the vault.
        default (int): Indicates if this vault is the default one (0 for no, 1 for yes).
        device_os (str): The operating system of the device associated with the vault.
        comment (str): A user-provided comment about the vault.
        createddate (str): The date when the vault was created.
        changeddate (str): The date when the vault was last modified.
    """
    def __init__(
        self,
        id: int,
        username: str,
        default: int,
        device_os: str,
        comment: str,
        createddate: str,
        changeddate: str
    ):
        
        self.id = int(id)  # Convert id to int to ensure it's the correct type
        self.username = username  # Store the username
        self.default = int(default)  # Convert default to int for consistent data type
        self.device_os = device_os  # Store the device operating system
        self.comment = comment  # Store the user comment
        self.createddate = createddate  # Store the creation date
        self.changeddate = changeddate  # Store the last changed date

class SingleVault(Vault):
    """
    This class is used for instances where detailed information and password of a specific vault is needed.

    Args:
        id (int): The unique identifier for the vault.
        username (str): The username associated with the vault.
        password (str): The password associated with the vault.
        default (int): Indicates if this vault is the default one (0 for no, 1 for yes).
        device_os (str): The operating system of the device associated with the vault.
        comment (str): A user-provided comment about the vault.
        createddate (str): The date when the vault was created.
        changeddate (str): The date when the vault was last modified.
    """
    def __init__(
        self,
        id: int,
        username: str,
        password: str,
        ssh_key: str,
        ssh_key_passphrase: str,
        enable_password: str,
        default: int,
        device_os: str,
        comment: str,
        createddate: str,
        changeddate: str
    ):
        self.password = password  # Store the password
        self.ssh_key = ssh_key  # Store the ssh_key
        self.ssh_key_passphrase = ssh_key_passphrase  # Store the ssh_key_passphrase
        self.enable_password = enable_password  # Store the enable_password
        super().__init__(id, username, default, device_os, comment, changeddate, createddate)  # Initialize the superclass (Vault) with the necessary parameters
