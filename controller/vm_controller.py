# controllers/vm_controller.py

from pyVmomi import vim
from core.vmware_client import VMwareClient
from models.vm_model import VM
from core.logger import logger


class VMController:
    def __init__(self):
        self.client = VMwareClient()
        self.client.connect()

    def create_vm(self, name, template_name, datastore_name, cpu, memory, network):
        try:
            content = self.client.si.RetrieveContent()
            template = self._get_template_by_name(content, template_name)
            datastore = self._get_datastore_by_name(content, datastore_name)
            if not template or not datastore:
                message = "Template or datastore not found"
                logger.error(message)
                return {"status": False, "message": message}

            vm_spec = vim.vm.ConfigSpec(
                name=name,
                memoryMB=memory,
                numCPUs=cpu,
                guestId=template.config.guestId,
                files=vim.vm.FileInfo(vmPathName=f"[{datastore_name}]")
            )

            network_spec = self._get_network_spec(network)
            if network_spec:
                vm_spec.deviceChange = [network_spec]

            resource_pool = self._get_resource_pool(content)
            if resource_pool:
                task = resource_pool.CreateVM_Task(config=vm_spec, pool=resource_pool, host=template.runtime.host)
                self._wait_for_task(task)
                logger.info(f"Created VM {name}")
                return {"status": True, "message": f"VM {name} created"}
            else:
                message = "Resource pool not found"
                logger.error(message)
                return {"status": False, "message": message}

        except Exception as e:
            logger.error(f"Failed to create VM {name}: {str(e)}")
            return {"status": False, "message": str(e)}

    def edit_vm(self, vm_name, cpu=None, memory=None):
        try:
            vm = self._get_vm_by_name(vm_name)
            if not vm:
                message = f"VM {vm_name} not found"
                logger.error(message)
                return {"status": False, "message": message}

            config_spec = vim.vm.ConfigSpec()
            if cpu:
                config_spec.numCPUs = cpu
            if memory:
                config_spec.memoryMB = memory

            task = vm.Reconfigure(config_spec)
            self._wait_for_task(task)
            logger.info(f"Edited VM {vm_name}")
            return {"status": True, "message": f"VM {vm_name} edited"}

        except Exception as e:
            logger.error(f"Failed to edit VM {vm_name}: {str(e)}")
            return {"status": False, "message": str(e)}

    def delete_vm(self, vm_name):
        try:
            vm = self._get_vm_by_name(vm_name)
            if not vm:
                message = f"VM {vm_name} not found"
                logger.error(message)
                return {"status": False, "message": message}

            task = vm.Destroy_Task()
            self._wait_for_task(task)
            logger.info(f"Deleted VM {vm_name}")
            return {"status": True, "message": f"VM {vm_name} deleted"}

        except Exception as e:
            logger.error(f"Failed to delete VM {vm_name}: {str(e)}")
            return {"status": False, "message": str(e)}

    def migrate_vm(self, vm_name, host_name):
        try:
            vm = self._get_vm_by_name(vm_name)
            if not vm:
                message = f"VM {vm_name} not found"
                logger.error(message)
                return {"status": False, "message": message}

            host = self._get_host_by_name(host_name)
            if not host:
                message = f"Host {host_name} not found"
                logger.error(message)
                return {"status": False, "message": message}

            task = vm.Migrate(host=host, priority=vim.vm.MigratePriority.defaultPriority)
            self._wait_for_task(task)
            logger.info(f"Migrated VM {vm_name} to host {host_name}")
            return {"status": True, "message": f"VM {vm_name} migrated to host {host_name}"}

        except Exception as e:
            logger.error(f"Failed to migrate VM {vm_name}: {str(e)}")
            return {"status": False, "message": str(e)}

    def get_vm_list(self):
        try:
            content = self.client.si.RetrieveContent()
            vm_list = []
            for datacenter in content.rootFolder.childEntity:
                for vm in datacenter.vmFolder.childEntity:
                    vm_list.append(vm.name)
            logger.info("Retrieved VM list")
            return {"status": True, "data": vm_list}

        except Exception as e:
            logger.error(f"Failed to get VM list: {str(e)}")
            return {"status": False, "message": str(e)}

    def get_vm_details(self, vm_name):
        try:
            vm = self._get_vm_by_name(vm_name)
            if not vm:
                message = f"VM {vm_name} not found"
                logger.error(message)
                return {"status": False, "message": message}

            details = {
                "name": vm.name,
                "cpu": vm.config.hardware.numCPU,
                "memory": vm.config.hardware.memoryMB,
                "datastore": vm.datastore[0].name if vm.datastore else None,
                "network": [net.name for net in vm.network]
            }
            logger.info(f"Retrieved details for VM {vm_name}")
            return {"status": True, "data": details}

        except Exception as e:
            logger.error(f"Failed to get VM details: {str(e)}")
            return {"status": False, "message": str(e)}

    def _get_template_by_name(self, content, template_name):
        for datacenter in content.rootFolder.childEntity:
            for vm in datacenter.vmFolder.childEntity:
                if vm.name == template_name and vm.config.template:
                    return vm
        return None

    def _get_datastore_by_name(self, content, datastore_name):
        for datacenter in content.rootFolder.childEntity:
            for datastore in datacenter.datastoreFolder.childEntity:
                if datastore.name == datastore_name:
                    return datastore
        return None

    def _get_resource_pool(self, content):
        for datacenter in content.rootFolder.childEntity:
            for cluster in datacenter.hostFolder.childEntity:
                return cluster.resourcePool
        return None

    def _get_vm_by_name(self, vm_name):
        content = self.client.si.RetrieveContent()
        for datacenter in content.rootFolder.childEntity:
            for vm in datacenter.vmFolder.childEntity:
                if vm.name == vm_name:
                    return vm
        return None

    def _get_host_by_name(self, host_name):
        content = self.client.si.RetrieveContent()
        for datacenter in content.rootFolder.childEntity:
            for cluster in datacenter.hostFolder.childEntity:
                for host in cluster.host:
                    if host.name == host_name:
                        return host
        return None

    def _get_network_spec(self, network_name):
        content = self.client.si.RetrieveContent()
        network = self._get_network_by_name(content, network_name)
        if not network:
            return None

        nic_spec = vim.vm.device.VirtualDeviceSpec()
        nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        nic_spec.device = vim.vm.device.VirtualVmxnet3()
        nic_spec.device.wakeOnLanEnabled = True
        nic_spec.device.deviceInfo = vim.Description()
        nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
        nic_spec.device.backing.network = network
        nic_spec.device.backing.deviceName = network.name
        nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        nic_spec.device.connectable.connected = True
        nic_spec.device.connectable.startConnected = True

        return nic_spec

    def _get_network_by_name(self, content, network_name):
        for datacenter in content.rootFolder.childEntity:
            for network in datacenter.network:
                if network.name == network_name:
                    return network
        return None

    def _wait_for_task(self, task):
        while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
            continue
