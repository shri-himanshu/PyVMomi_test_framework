# this file will have methods/ functions for parsing testbed, saving and updating configurations of the different
# vmware related objects like ESXi hosts, VMs, Templates, vSwitches etc.
import os

import yaml
import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(description="PyVmomi Framework")
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to the configuration file (config.yaml)"
    )
    return parser.parse_args()


class Config:
    def __init__(self, config_file=None):
        # config_file = os.path.join(os.getcwd(), config_file)
        # with open(config_file, 'r') as file:
        #     self.config = yaml.safe_load(file)
        if config_file is None:
            args = parse_args()
            config_file = args.config

        config_file = os.path.join(os.getcwd(), config_file)
        if not os.path.isfile(config_file):
            raise FileNotFoundError(f"Configuration file not found: {config_file}")

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
