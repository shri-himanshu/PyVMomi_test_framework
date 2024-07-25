# this file will have methods/ functions for parsing testbed, saving and updating configurations of the different
# vmware related objects like ESXi hosts, VMs, Templates, vSwitches etc.
import os

import yaml

class Config:
    def __init__(self, config_file='sample_config.yaml'):
        config_file = os.path.join(os.getcwd(), config_file)
        with open(config_file, 'r') as file:
            self.config = yaml.safe_load(file)

    def get(self, key):
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, None)
            if value is None:
                break
        return value

    def get_esxi_host(self, name):
        hosts = self.config.get('esxi_hosts', [])
        for host in hosts:
            if host['name'] == name:
                return host
        return None
