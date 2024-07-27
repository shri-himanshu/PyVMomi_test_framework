# datastore_controller.py

from pyVmomi import vim
from core.vmware_client import VMwareClient
from core.logger import logger

class DatastoreController:
    def __init__(self, connection_type='vcenter'):
        self.client = VMwareClient(connection_type)
        self.client.connect()

    def create_datastore(self, datastore_name, capacity_gb, disk_path):
        host = self.client._get_host_system()
        try:
            datastore_spec = vim.host.DatastoreSystem.DatastoreSpec()
            datastore_spec.name = datastore_name
            datastore_spec.capacityKB = capacity_gb * 1024 * 1024  # Convert GB to KB
            datastore_spec.backing = vim.host.DatastoreSystem.LocalDatastoreBackingInfo(diskPath=disk_path)
            host.configManager.datastoreSystem.CreateDatastore(datastore_spec)
            logger.info(f"Created datastore {datastore_name} with capacity {capacity_gb} GB at {disk_path}")
            return {"status": True, "message": f"Datastore {datastore_name} created with capacity {capacity_gb} GB at {disk_path}"}
        except Exception as e:
            logger.error(f"Failed to create datastore {datastore_name}: {str(e)}")
            return {"status": False, "message": str(e)}
        # finally:
        #     self.client.disconnect()

    def delete_datastore(self, datastore_name):
        host = self.client._get_host_system()
        try:
            datastore = self._get_datastore_by_name(datastore_name)
            if datastore:
                host.configManager.datastoreSystem.RemoveDatastore(datastore)
                logger.info(f"Deleted datastore {datastore_name}")
                return {"status": True, "message": f"Datastore {datastore_name} deleted"}
            else:
                logger.error(f"Datastore {datastore_name} not found")
                return {"status": False, "message": f"Datastore {datastore_name} not found"}
        except Exception as e:
            logger.error(f"Failed to delete datastore {datastore_name}: {str(e)}")
            return {"status": False, "message": str(e)}
        # finally:
        #     self.client.disconnect()

    def list_datastores(self):
        host = self.client._get_host_system()
        try:
            datastores = host.datastore
            datastore_list = [datastore.name for datastore in datastores]
            logger.info(f"Datastores: {datastore_list}")
            return {"status": True, "datastores": datastore_list}
        except Exception as e:
            logger.error(f"Failed to list datastores: {str(e)}")
            return {"status": False, "message": str(e)}
        # finally:
        #     self.client.disconnect()

    def _get_datastore_by_name(self, datastore_name):
        host = self.client._get_host_system()
        datastores = host.datastore
        for datastore in datastores:
            if datastore.name == datastore_name:
                return datastore
        return None
