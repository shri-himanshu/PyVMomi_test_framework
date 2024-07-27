# datastore.py

from controller.vdatastore_controller import DatastoreController

class DatastoreModel:
    def __init__(self, connection_type='vcenter'):
        self.controller = DatastoreController(connection_type)

    def create_datastore(self, datastore_name, capacity_gb, disk_path):
        return self.controller.create_datastore(datastore_name, capacity_gb, disk_path)

    def delete_datastore(self, datastore_name):
        return self.controller.delete_datastore(datastore_name)

    def list_datastores(self):
        return self.controller.list_datastores()
