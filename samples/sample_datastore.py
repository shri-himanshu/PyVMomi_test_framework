# sample_datastore_script.py

from models.vdatastore_model import DatastoreModel
from core.config import Config


def main():
    # Load configuration
    config = Config()
    connection_type = 'esxi'  # or 'esxi'

    # Create DatastoreModel object
    datastore_model = DatastoreModel(connection_type)

    # Create a datastore
    datastore_name = "sample_datastore"
    capacity_gb = 100  # Capacity in GB
    disk_path = "/vmfs/volumes/sample_disk"  # Path to the disk
    result_create = datastore_model.create_datastore(datastore_name, capacity_gb, disk_path)
    print("Create Datastore:", result_create)

    # List datastores
    result_list = datastore_model.list_datastores()
    print("List Datastores:", result_list)

    # Delete a datastore
    result_delete = datastore_model.delete_datastore(datastore_name)
    print("Delete Datastore:", result_delete)


if __name__ == "__main__":
    main()
