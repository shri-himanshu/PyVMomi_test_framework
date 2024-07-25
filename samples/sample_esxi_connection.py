# Example of using VMwareClient to perform operations on a standalone ESXi host

from core.vmware_client import VMwareClient
from models.vswitch_model import VSwitchModel


client = VMwareClient()
import pdb;pdb.set_trace()
# Connect to the ESXi host
client.connect()

# Get the host system
host = client._get_host_system()

# Create a datastore on the ESXi host
# result = client.create_datastore(datastore_name="example_datastore", host=host)
# print(result)
#
# # Delete the datastore from the ESXi host
# result = client.delete_datastore(datastore_name="example_datastore", host=host)
# print(result)
#
# # Create a vSwitch on the ESXi host
# result = client.create_vswitch(vswitch_name="example_vswitch", num_ports=128, host=host)
# print(result)
#
# # Delete the vSwitch from the ESXi host
# result = client.delete_vswitch(vswitch_name="example_vswitch", host=host)
# print(result)

# Disconnect from the ESXi host
client.disconnect()
