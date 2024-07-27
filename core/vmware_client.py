# vmware_client.py

from pyvim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl
from core.config import Config
from core.logger import logger

class VMwareClient:
    def __init__(self, connection_type='esxi'):
        config = Config()
        if connection_type == 'vcenter':
            self.host = config.get('vmware.vcenter.host')
            self.user = config.get('vmware.vcenter.user')
            self.pwd = config.get('vmware.vcenter.password')
            self.port = config.get('vmware.vcenter.port')
            self.disable_ssl_cert_verify = config.get('vmware.vcenter.disableSslCertValidation')
        elif connection_type == 'esxi':
            self.host = config.get('vmware.esxi.host')
            self.user = config.get('vmware.esxi.user')
            self.pwd = config.get('vmware.esxi.password')
            self.port = config.get('vmware.esxi.port')
            self.disable_ssl_cert_verify = config.get('vmware.esxi.disableSslCertValidation')
        else:
            raise ValueError("Invalid connection type")
        self.si = None

    def connect(self):
        try:
            self.si = SmartConnect(host=self.host, user=self.user, pwd=self.pwd, port=self.port,
                                   disableSslCertValidation=self.disable_ssl_cert_verify)
            logger.info(f"Connected to VMware environment at {self.host}")
        except Exception as e:
            logger.error(f"Failed to connect to VMware environment at {self.host}: {str(e)}")
            raise

    def disconnect(self):
        if self.si:
            Disconnect(self.si)
            logger.info(f"Disconnected from VMware environment at {self.host}")

    def _get_host_system(self):
        content = self.si.RetrieveContent()
        container = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
        hosts = container.view
        container.Destroy()
        return hosts[0] if hosts else None
