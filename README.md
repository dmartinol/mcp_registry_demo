# MCP Registry Demo on Openshift
Follow the steps defined in the following Jupoyter Notebooks to configure an MCP registry in OpenShift
using the [ToolHive registry server](https://github.com/Stacklok/toolhive-registry-server).

More details in the linked article on [Red Hat Developer's Blog](__TODO__).

## Prerequisites

### Python Dependencies

The notebooks require Python packages to interact with the registry API. It's recommended to use a virtual environment to isolate dependencies.

#### Create and Activate Virtual Environment

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### OpenShift CLI Tools

- `oc` - OpenShift CLI (for deploying resources)
- `helm` - Helm CLI (for installing the ToolHive operator)
- `yq` - YAML processor (optional, for parsing YAML output)

## Project Structure

The project includes a shared utility library to avoid code duplication:

```
mcp_registry_demo/
├── lib/
│   ├── __init__.py
│   └── registry_client.py    # Shared registry API client
├── notebooks/                # Jupyter notebooks
│   ├── 01-setup.ipynb
│   ├── 02-deploy-registry.ipynb
│   └── ...
├── manifests/                # Kubernetes/OpenShift manifests
├── catalogs/                 # MCP catalog JSON files
└── requirements.txt
```

The `lib/registry_client.py` module provides:
- `RegistryClient` class for interacting with the MCP Registry API
- Helper functions: `print_server_details()`, `print_server_cards()`

Notebooks automatically add the `lib` directory to the Python path, so you can import these utilities directly.

## Notebooks

* [Setup ToolHive operator](./notebooks/01-setup.ipynb)
* [Deploy the MCP registry](./notebooks/02-deploy-registry.ipynb)
* [Deploy and discover MCP server](./notebooks/03-deploy-and-discover-mcp-server.ipynb)
* [Monitoring](./notebooks/04-monitoring.ipynb) - Configure monitoring and metrics collection
* [Cleanup](./notebooks/05-cleanup.ipynb) - Optional cleanup notebook to remove deployed resources


