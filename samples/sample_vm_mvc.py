# Example of how to use the controller to create a VM

from controller.vm_controller import VMController
from view.vm_view import OutputFormat

vm_controller = VMController()
result = vm_controller.create_vm(
    name="test_vm",
    template_name="template_name",
    datastore_name="datastore_name",
    cpu=2,
    memory=4096,
    network="network_name"
)
print(OutputFormat.format_result(result))
