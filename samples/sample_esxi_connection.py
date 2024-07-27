# sample_script.py
import time

from models.vswitch_model import VSwitchModel
from core.config import Config


def main():
    # Load configuration
    config = Config()

    connection_type = 'esxi'  # or 'esxi'

    # Create VSwitchModel object
    vswitch_model = VSwitchModel(connection_type)

    # Create a virtual switch
    vswitch_name = config.get('network.vswitch_name')
    num_ports = 128  # Default number of ports
    try:
        result = vswitch_model.create_vswitch(vswitch_name, num_ports)
    except Exception as err:
        print("failed to create vswitch")
    time.sleep(10)
    vswitch_model.delete_vswitch(vswitch_name)

    # Print the result
    print(result)


if __name__ == "__main__":
    main()
