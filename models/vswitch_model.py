# models/vswitch.py

from controller.vswitch_controller import VSwitchController
from view.vswitch_view import OutputFormat

class VSwitchModel:
    def __init__(self):
        self.controller = VSwitchController()

    def create_vswitch(self, name, num_ports, uplink_portgroup):
        result = self.controller.create_vswitch(name, num_ports, uplink_portgroup)
        return OutputFormat.format_result(result)

    def update_vswitch(self, name, num_ports=None, uplink_portgroup=None):
        result = self.controller.update_vswitch(name, num_ports, uplink_portgroup)
        return OutputFormat.format_result(result)

    def delete_vswitch(self, name):
        result = self.controller.delete_vswitch(name)
        return OutputFormat.format_result(result)

    def get_vswitch_list(self):
        result = self.controller.get_vswitch_list()
        return
