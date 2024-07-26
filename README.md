Here's a detailed `README.md` for the framework:

### README.md

# VMware Test Automation Framework

## Overview

This framework is designed to automate operations on VMware vCenter, vSphere ESXi, and virtual machines using the PyVmomi module. It follows an MVC (Model-View-Controller) architecture to ensure maintainability, scalability, and ease of use. The framework separates the business logic, data handling, and presentation layers, making it easy to extend and modify.

## Architecture

The framework consists of the following layers:

- **Model**: Provides a simplified interface (facade) to the controller functions. Test cases interact with the model layer, which in turn calls the necessary controller methods.
- **Controller**: Contains the business logic and interacts with VMware infrastructure using PyVmomi.
- **View**: Formats the output of operations (not extensively used in this example).

### Directory Structure

```
vmware_test_framework/
├── framework/
│   ├── core/
│   │   ├── config.py
│   │   ├── logger.py
│   │   ├── report.py
│   │   └── vmware_client.py
│   ├── controller/
│   │   ├── vswitch_controller.py
│   │   └── vm_controller.py
│   ├── model/
│   │   ├── vswitch.py
│   │   └── vm.py
│   └── view/
│       └── format.py
├── tests/
│   ├── test_vswitch.py
│   └── test_vm.py
├── config.yaml
└── README.md
```

## Configuration

The configuration file `config.yaml` contains settings for VMware connections, logging, test environment, and more. Update the file with your VMware environment details:

```yaml
# VMware Connection Settings
vmware:
  vcenter:
    host: "vcenter.example.com"
    user: "administrator@vsphere.local"
    password: "password"
    port: 443
  esxi:
    host: "esxi.example.com"
    user: "root"
    password: "password"
    port: 443

# Logging Settings
logging:
  log_file: "vmware.log"
  log_level: "INFO"

# Test Environment Settings
test_environment:
  default_template: "ubuntu_template"
  default_datastore: "datastore1"
  default_network: "VM Network"
  default_cpu: 2
  default_memory: 4096

# Report Settings
report:
  report_file: "test_report.json"

# Performance Tool Settings
performance_tools:
  tool1:
    path: "/path/to/tool1"
    options: "--option1 --option2"
  tool2:
    path: "/path/to/tool2"
    options: "--option3 --option4"

# Scale Operation Settings
scale_operations:
  max_vms: 50
  min_vms: 5

# Network Settings
network:
  default_vlan: "vlan100"
  vswitch_name: "vSwitch0"

# Metadata Collection Settings
metadata:
  collect_interval: 300 # in seconds
```

## Adding a New MVC Component

To add a new component, follow these steps:

### 1. Create the Controller

Create a new file in the `controller` directory for your component, e.g., `datastore_controller.py`:

```python
# datastore_controller.py

from pyVmomi import vim
from framework.core.vmware_client import VMwareClient
from framework.core.logger import logger

class DatastoreController:
    def __init__(self):
        self.client = VMwareClient()

    def create_datastore(self, datastore_name, capacity_gb):
        host = self.client._get_host_system()
        try:
            self.client.connect()
            spec = vim.host.DatastoreSystem.DatastoreSpec()
            spec.name = datastore_name
            spec.capacityKB = capacity_gb * 1024 * 1024  # Convert GB to KB
            host.configManager.datastoreSystem.CreateDatastore(spec)
            logger.info(f"Created datastore {datastore_name} with capacity {capacity_gb} GB")
            return {"status": True, "message": f"Datastore {datastore_name} created with capacity {capacity_gb} GB"}
        except Exception as e:
            logger.error(f"Failed to create datastore {datastore_name}: {str(e)}")
            return {"status": False, "message": str(e)}
        finally:
            self.client.disconnect()
```

### 2. Create the Model

Create a new file in the `model` directory for your component, e.g., `datastore.py`:

```python
# datastore.py

from framework.controller.datastore_controller import DatastoreController

class DatastoreModel:
    def __init__(self):
        self.controller = DatastoreController()

    def create_datastore(self, datastore_name, capacity_gb):
        return self.controller.create_datastore(datastore_name, capacity_gb)
```

### 3. Write Test Cases

Create a new file in the `tests` directory for your component, e.g., `test_datastore.py`:

```python
# test_datastore.py

import pytest
from framework.model.datastore import DatastoreModel

@pytest.fixture(scope="module")
def datastore_model():
    return DatastoreModel()

def test_create_datastore(datastore_model):
    result = datastore_model.create_datastore("test_datastore", 50)
    assert result["status"] is True
    assert "Datastore test_datastore created" in result["message"]
```

### 4. Run the Test Cases

Use `pytest` to run the test cases:

```bash
pytest tests/test_datastore.py
```

## Writing a Sample Script to Test MVC Layers

Create a sample script to interact with the new component's MVC layers, e.g., `sample_script.py`:

```python
# sample_script.py

from framework.model.datastore import DatastoreModel

def main():
    datastore_model = DatastoreModel()
    result = datastore_model.create_datastore("sample_datastore", 100)
    print(result)

if __name__ == "__main__":
    main()
```

Run the script:

```bash
python sample_script.py
```

## Benefits of the Design

### Separation of Concerns

The MVC architecture ensures that the data handling, business logic, and presentation are separated. This makes the framework easy to maintain and extend.

### Low Coupling and High Cohesion

Each component is independent and focuses on a single responsibility. This design minimizes dependencies between components and ensures that each component is highly cohesive.

### Scalability

The modular design allows new features to be added without affecting existing functionality. The configuration file makes it easy to adjust the framework for different environments.

### Maintainability and Testability

The use of SOLID principles and design patterns like the Facade pattern ensures that the codebase is easy to maintain and test. The separation of layers allows unit tests to be written for each component in isolation.

### Flexibility

The framework can be easily extended to support new VMware operations or other virtual infrastructure providers. The configuration management allows for easy adaptation to different environments.

---

This detailed explanation and step-by-step guide should help you understand the design choices and benefits of the framework, as well as how to extend it for new components.