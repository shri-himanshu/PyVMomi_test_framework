# models/vm_model.py

from controller.vm_controller import VMController
from view.vm_view import OutputFormat


class VMModel:
    def __init__(self):
        self.controller = VMController()

    def create_vm(self, name, template_name, datastore_name, cpu, memory, network):
        result = self.controller.create_vm(name, template_name, datastore_name, cpu, memory, network)
        return OutputFormat.format_result(result)

    def edit_vm(self, vm_name, cpu=None, memory=None):
        result = self.controller.edit_vm(vm_name, cpu, memory)
        return OutputFormat.format_result(result)

    def delete_vm(self, vm_name):
        result = self.controller.delete_vm(vm_name)
        return OutputFormat.format_result(result)

    def migrate_vm(self, vm_name, host_name):
        result = self.controller.migrate_vm(vm_name, host_name)
        return OutputFormat.format_result(result)

    def get_vm_list(self):
        result = self.controller.get_vm_list()
        return OutputFormat.format_data(result)

    def get_vm_details(self, vm_name):
        result = self.controller.get_vm_details(vm_name)
        return OutputFormat.format_data(result)
