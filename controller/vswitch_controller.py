# controllers/vswitch_controller.py

from pyVmomi import vim
from core.vmware_client import VMwareClient
from core.logger import logger


class VSwitchController:
    def __init__(self, connection_type='esxi'):
        self.client = VMwareClient(connection_type)
        self.client.connect()

    def create_vswitch(self, vswitch_name, num_ports, uplink_portgroup):
        host = self.client._get_host_system()
        try:
            vss = vim.host.VirtualSwitch.Specification()
            vss.numPorts = num_ports
            host.configManager.networkSystem.AddVirtualSwitch(vswitch_name, vss)
            logger.info(f"Created virtual switch {vswitch_name} with {num_ports} ports")
            return {"status": True, "message": f"Virtual switch {vswitch_name} created with {num_ports} ports"}
        except Exception as e:
            logger.error(f"Failed to create virtual switch {vswitch_name}: {str(e)}")
            return {"status": False, "message": str(e)}
        # finally:
        #     self.client.disconnect()

    def delete_vswitch(self, vswitch_name):
        try:
            host = self.client._get_host_system()
            if host:
                network_system = host.configManager.networkSystem
                vswitch = self._get_vswitch_by_name(network_system, vswitch_name)
                if vswitch:
                    network_system.RemoveVirtualSwitch(vswitch_name)
                    logger.info(f"Deleted vSwitch {vswitch_name} on host {host.name}")
                    return {"status": True, "message": f"vSwitch {vswitch_name} deleted"}
                else:
                    logger.error(f"vSwitch {vswitch_name} not found")
                    return {"status": False, "message": "vSwitch not found"}
            else:
                logger.error(f"Host {host.name} not found")
                return {"status": False, "message": "Host not found"}
        except Exception as e:
            logger.error(f"Failed to delete vSwitch {vswitch_name}: {str(e)}")
            return {"status": False, "message": str(e)}

    def update_vswitch(self, vswitch_name, num_ports):
        try:
            host = self.client._get_host_system()
            if host:
                network_system = host.configManager.networkSystem
                vswitch = self._get_vswitch_by_name(network_system, vswitch_name)
                if vswitch:
                    vswitch_spec = vim.host.VirtualSwitch.Specification()
                    vswitch_spec.numPorts = num_ports
                    network_system.UpdateVirtualSwitch(vswitch_name, vswitch_spec)
                    logger.info(f"Updated vSwitch {vswitch_name} on host {host.name}")
                    return {"status": True, "message": f"vSwitch {vswitch_name} updated"}
                else:
                    logger.error(f"vSwitch {vswitch_name} not found")
                    return {"status": False, "message": "vSwitch not found"}
            else:
                logger.error(f"Host {host.name} not found")
                return {"status": False, "message": "Host not found"}
        except Exception as e:
            logger.error(f"Failed to update vSwitch {vswitch_name}: {str(e)}")
            return {"status": False, "message": str(e)}

    def _get_vswitch_by_name(self, network_system, vswitch_name):
        for vswitch in network_system.networkInfo.vswitch:
            if vswitch.name == vswitch_name:
                return vswitch
        return None
