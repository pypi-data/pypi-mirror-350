from slurpit.models.basemodel import BaseModel

class Node(BaseModel):
    """
    This class represents a network device or node with various attributes that help identify and manage it in a network.

    Args:
        ip (str): The IP address of the network node, used for network communication and identification.
        device_type (str): The type of device, such as router, switch, or firewall, which helps in categorizing the node.
        hostname (str): The local name of the device, used for easier identification within a network.
        fqdn (str): The Fully Qualified Domain Name, providing a complete domain name address for the node.
        vendor (str): The manufacturer of the device, giving insights into the device's specifications and compatibility.
        product (str): The specific product name or model of the device as defined by the vendor.
        batch_id (int): A batch identifier that can link this node to a specific production or shipment batch.
        snmp_vars (str): A string representing SNMP variables used for monitoring the device via SNMP.
        timestamp (str): The date and time when the node data was last updated, important for tracking changes.
        error (str): A field to note any errors related to the node, useful for troubleshooting and maintenance.
    """
    def __init__(
        self,
        ip: str,
        device_type: str,
        hostname: str,
        fqdn: str,
        vendor: str,
        product: str,
        batch_id: int,
        snmp_vars: str,
        timestamp: str,
        error: str
    ):
        self.ip = ip
        self.device_type = device_type
        self.hostname = hostname
        self.fqdn = fqdn
        self.vendor = vendor
        self.product = product
        self.batch_id = batch_id
        self.snmp_vars = snmp_vars
        self.timestamp = timestamp
        self.error = error
