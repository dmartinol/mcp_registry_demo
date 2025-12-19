# MCP Registry Demo

Resources to deploy and manage an MCP (Model Context Protocol) registry in OpenShift using the Stacklok ToolHive operator.

## Overview

This repository contains comprehensive resources for demonstrating the deployment and management of an MCP registry on OpenShift. The demo showcases how to use the Stacklok ToolHive operator to manage MCP tools and registries in a Kubernetes/OpenShift environment.

## Contents

- **manifests/** - Kubernetes/OpenShift YAML manifests for deploying the MCP registry and related resources
- **notebooks/** - Jupyter notebooks providing interactive step-by-step demos
- **config/** - JSON configuration files for the MCP registry and tools
- **docs/** - Additional documentation and guides

## Prerequisites

Before running this demo, ensure you have:

1. **OpenShift Cluster Access**
   - OpenShift 4.12 or later
   - Cluster admin privileges or appropriate RBAC permissions
   - `oc` CLI tool installed and configured

2. **Required Tools**
   - Jupyter Notebook or JupyterLab (for running interactive demos)
   - `kubectl` or `oc` CLI
   - `curl` or `wget` for downloading resources
   - Python 3.8+ (for running notebooks)

3. **Python Dependencies** (for Jupyter notebooks)
   ```bash
   pip install jupyter kubernetes pyyaml requests
   ```

## Quick Start

1. **Clone this repository**
   ```bash
   git clone https://github.com/dmartinol/mcp_registry_demo.git
   cd mcp_registry_demo
   ```

2. **Login to your OpenShift cluster**
   ```bash
   oc login <your-cluster-url>
   ```

3. **Start the demo using Jupyter notebooks**
   ```bash
   jupyter notebook notebooks/
   ```

4. **Follow the notebooks in order**
   - `01-setup-and-prerequisites.ipynb` - Environment setup
   - `02-deploy-toolhive-operator.ipynb` - Deploy the ToolHive operator
   - `03-deploy-mcp-registry.ipynb` - Deploy and configure the MCP registry
   - `04-manage-and-test.ipynb` - Manage tools and test the registry

## Manual Deployment

If you prefer to deploy without notebooks:

1. **Create the namespace**
   ```bash
   oc apply -f manifests/00-namespace.yaml
   ```

2. **Deploy the ToolHive operator**
   ```bash
   oc apply -f manifests/01-toolhive-operator.yaml
   ```

3. **Deploy the MCP registry**
   ```bash
   oc apply -f manifests/02-mcp-registry.yaml
   ```

4. **Configure services and routes**
   ```bash
   oc apply -f manifests/03-services.yaml
   oc apply -f manifests/04-route.yaml
   ```

## Architecture

The demo deploys the following components:

- **ToolHive Operator** - Manages the lifecycle of MCP tools and registries
- **MCP Registry** - A central registry for storing and serving MCP tool definitions
- **Storage** - Persistent storage for registry data
- **Ingress/Route** - External access to the registry

See [docs/architecture.md](docs/architecture.md) for detailed architecture information.

## Documentation

- [Architecture Overview](docs/architecture.md) - Detailed system architecture
- [Troubleshooting Guide](docs/troubleshooting.md) - Common issues and solutions
- [API Reference](docs/api-reference.md) - MCP registry API documentation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## References

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Stacklok ToolHive Documentation](https://github.com/stacklok/minder)
- [OpenShift Documentation](https://docs.openshift.com/)

## Support

For questions or issues, please open an issue in this repository.
