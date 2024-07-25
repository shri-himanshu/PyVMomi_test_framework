# controllers/vswitch_controller.py

from pyVmomi import vim
from core.vmware_client import VMwareClient
# from models.vswitch_model import VSwitchModel
from core.logger import logger

class VSwitchController:
    def __init__(self):
        self.client = VMwareClient()
        self.client.connect()

    def create_vswitch(self, host_name, vswitch_name, num_ports):
        try:
            content = self.client.si.RetrieveContent()
            host = self._get_host_by_name(content, host_name)
            if host:
                network_system = host.configManager.networkSystem
                vswitch_spec = vim.host.VirtualSwitch.Specification()
                vswitch_spec.numPorts = num_ports
                network_system.AddVirtualSwitch(vswitch_name, vswitch_spec)
                logger.info(f"Created vSwitch {vswitch_name} on host {host_name}")
                return {"status": True, "message": f"vSwitch {vswitch_name} created"}
            else:
                logger.error(f"Host {host_name} not found")
                return {"status": False, "message": "Host not found"}
        except Exception as e:
            logger.error(f"Failed to create vSwitch {vswitch_name}: {str(e)}")
            return {"status": False, "message": str(e)}

    def update_vswitch(self, host_name, vswitch_name, num_ports):
        try:
            content = self.client.si.RetrieveContent()
            host = self._get_host_by_name(content, host_name)
            if host:
                network_system = host.configManager.networkSystem
                vswitch = self._get_vswitch_by_name(network_system, vswitch_name)
                if vswitch:
                    vswitch_spec = vim.host.VirtualSwitch.Specification()
                    vswitch_spec.numPorts = num_ports
                    network_system.UpdateVirtualSwitch(vswitch_name, vswitch_spec)
                    logger.info(f"Updated vSwitch {vswitch_name} on host {host_name}")
                    return {"status": True, "message": f"vSwitch {vswitch_name} updated"}
                else:
                    logger.error(f"vSwitch {vswitch_name} not found")
                    return {"status": False, "message": "vSwitch not found"}
            else:
                logger.error(f"Host {host_name} not found")
                return {"status": False, "message": "Host not found"}
        except Exception as e:
            logger.error(f"Failed to update vSwitch {vswitch_name}: {str(e)}")
            return {"status": False, "message": str(e)}

    def delete_vswitch(self, host_name, vswitch_name):
        try:
            content = self.client.si.RetrieveContent()
            host = self._get_host_by_name(content, host_name)
            if host:
                network_system = host.configManager.networkSystem
                vswitch = self._get_vswitch_by_name(network_system, vswitch_name)
                if vswitch:
                    network_system.RemoveVirtualSwitch(vswitch_name)
                    logger.info(f"Deleted vSwitch {vswitch_name} on host {host_name}")
                    return {"status": True, "message": f"vSwitch {vswitch_name} deleted"}
                else:
                    logger.error(f"vSwitch {vswitch_name} not found")
                    return {"status": False, "message": "vSwitch not found"}
            else:
                logger.error(f"Host {host_name} not found")
                return {"status": False, "message": "Host not found"}
        except Exception as e:
            logger.error(f"Failed to delete vSwitch {vswitch_name}: {str(e)}")
            return {"status": False, "message": str(e)}

    def _get_host_by_name(self, content, host_name):
        for datacenter in content.rootFolder.childEntity:
            for cluster in datacenter.hostFolder.childEntity:
                for host in cluster.host:
                    if host.name == host_name:
                        return host
        return None

    def _get_vswitch_by_name(self, network_system, vswitch_name):
        for vswitch in network_system.networkInfo.vswitch:
            if vswitch.name == vswitch_name:
                return vswitch
        return None
