# vmware_client.py

from pyvim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl
from core.config import Config
from core.logger import logger

config = Config()

class VMwareClient:
    def __init__(self):
        self.host = config.get('esxi_hosts.host')
        self.user = config.get('esxi_hosts.user')
        self.pwd = config.get('esxi_hosts.password')
        self.port = config.get('esxi_hosts.port')
        self.disable_ssl_cert_verify = config.get('esxi_hosts.disableSslCertValidation')
        self.si = None

    def connect(self):
        try:
            self.si = SmartConnect(host=self.host, user=self.user, pwd=self.pwd, port=self.port,
                                   disableSslCertValidation=self.disable_ssl_cert_verify)
            logger.info("Connected to VMware environment")
        except Exception as e:
            logger.error(f"Failed to connect to VMware environment: {str(e)}")
            raise

    def disconnect(self):
        if self.si:
            Disconnect(self.si)
            logger.info("Disconnected from VMware environment")

    def _get_host_system(self):
        content = self.si.RetrieveContent()
        container = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
        hosts = container.view
        container.Destroy()
        return hosts[0] if hosts else None

    def _get_datastore_by_name(self, name):
        content = self.si.RetrieveContent()
        container = content.viewManager.CreateContainerView(content.rootFolder, [vim.Datastore], True)
        datastores = container.view
        for datastore in datastores:
            if datastore.name == name:
                container.Destroy()
                return datastore
        container.Destroy()
        return None

    def _get_template_by_name(self, name):
        content = self.si.RetrieveContent()
        container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
        templates = container.view
        for template in templates:
            if template.name == name and template.config.template:
                container.Destroy()
                return template
        container.Destroy()
        return None

    def _get_network_spec(self, network_name):
        content = self.si.RetrieveContent()
        container = content.viewManager.CreateContainerView(content.rootFolder, [vim.Network], True)
        networks = container.view
        for network in networks:
            if network.name == network_name:
                network_spec = vim.vm.device.VirtualDeviceSpec()
                network_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
                network_spec.device = vim.vm.device.VirtualVmxnet3()
                network_spec.device.deviceInfo = vim.Description()
                network_spec.device.deviceInfo.summary = network_name
                network_spec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
                network_spec.device.backing.deviceName = network_name
                container.Destroy()
                return network_spec
        container.Destroy()
        return None

    def _get_resource_pool(self, content):
        container = content.viewManager.CreateContainerView(content.rootFolder, [vim.ResourcePool], True)
        resource_pools = container.view
        for rp in resource_pools:
            if rp:
                container.Destroy()
                return rp
        container.Destroy()
        return None

    # Add methods specific to standalone ESXi host operations

    def create_datastore(self, datastore_name, host):
        try:
            spec = vim.host.DatastoreSystem.DatastoreSpec()
            spec.name = datastore_name
            spec.capacityKB = 1024 * 1024 * 100  # Example: 100 GB
            host.configManager.datastoreSystem.CreateDatastore(spec)
            logger.info(f"Created datastore {datastore_name} on host {host.name}")
            return {"status": True, "message": f"Datastore {datastore_name} created on host {host.name}"}
        except Exception as e:
            logger.error(f"Failed to create datastore {datastore_name} on host {host.name}: {str(e)}")
            return {"status": False, "message": str(e)}

    def delete_datastore(self, datastore_name, host):
        try:
            datastores = host.configManager.datastoreSystem.datastore
            for datastore in datastores:
                if datastore.name == datastore_name:
                    host.configManager.datastoreSystem.RemoveDatastore(datastore)
                    logger.info(f"Deleted datastore {datastore_name} from host {host.name}")
                    return {"status": True, "message": f"Datastore {datastore_name} deleted from host {host.name}"}
            message = f"Datastore {datastore_name} not found on host {host.name}"
            logger.error(message)
            return {"status": False, "message": message}
        except Exception as e:
            logger.error(f"Failed to delete datastore {datastore_name} from host {host.name}: {str(e)}")
            return {"status": False, "message": str(e)}

    def create_vswitch(self, vswitch_name, num_ports, host):
        try:
            vswitch_spec = vim.host.VirtualSwitch.Specification()
            vswitch_spec.numPorts = num_ports
            host.configManager.networkSystem.AddVirtualSwitch(vswitchName=vswitch_name, spec=vswitch_spec)
            logger.info(f"Created vSwitch {vswitch_name} on host {host.name}")
            return {"status": True, "message": f"vSwitch {vswitch_name} created on host {host.name}"}
        except Exception as e:
            logger.error(f"Failed to create vSwitch {vswitch_name} on host {host.name}: {str(e)}")
            return {"status": False, "message": str(e)}

    def delete_vswitch(self, vswitch_name, host):
        try:
            host.configManager.networkSystem.RemoveVirtualSwitch(vswitchName=vswitch_name)
            logger.info(f"Deleted vSwitch {vswitch_name} from host {host.name}")
            return {"status": True, "message": f"vSwitch {vswitch_name} deleted from host {host.name}"}
        except Exception as e:
            logger.error(f"Failed to delete vSwitch {vswitch_name} from host {host.name}: {str(e)}")
            return {"status": False, "message": str(e)}
