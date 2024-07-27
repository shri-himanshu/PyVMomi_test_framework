# models/vswitch.py

from controller.vswitch_controller import VSwitchController
from view.vswitch_view import OutputFormat

class VSwitchModel:
    def __init__(self, connection_type='vcenter'):
        self.controller = VSwitchController(connection_type)

    def create_vswitch(self, vswitch_name, num_ports=128, uplink_portgroup=None):
        return self.controller.create_vswitch(vswitch_name, num_ports, uplink_portgroup)

    def update_vswitch(self, vswitch_name, num_ports=None, uplink_portgroup=None):
        return self.controller.update_vswitch(vswitch_name, num_ports, uplink_portgroup)

    def delete_vswitch(self, vswitch_name):
        return self.controller.delete_vswitch(vswitch_name)

    def get_vswitch_list(self):
        result = self.controller.get_vswitch_list()
        return
