# MCP Registry Architecture

This document describes the architecture of the MCP Registry deployment on OpenShift.

## Overview

The MCP Registry is a centralized service for managing and distributing Model Context Protocol (MCP) tools in an OpenShift environment. It leverages the Stacklok ToolHive operator for lifecycle management.

## Components

### 1. ToolHive Operator

The ToolHive operator is responsible for managing the lifecycle of MCP tools and the registry itself.

**Key Features:**
- Custom Resource Definitions (CRDs) for MCP tools
- Automated deployment and updates
- Health monitoring and self-healing
- Integration with OpenShift

**Resources:**
- Deployment: `toolhive-operator`
- Service Account: `toolhive-operator`
- ClusterRole & ClusterRoleBinding for RBAC

### 2. MCP Registry

The registry service stores and serves MCP tool definitions.

**Key Features:**
- RESTful API for tool management
- Persistent storage for tool data
- Health and readiness probes
- Versioning support

**Resources:**
- Deployment: `mcp-registry`
- PersistentVolumeClaim: `mcp-registry-data`
- ConfigMaps:
  - `mcp-registry-config`: Registry configuration
  - `mcp-registry-server`: Python server implementation

### 3. Storage Layer

Persistent storage for registry data.

**Configuration:**
- StorageClass: Default (cluster-specific)
- AccessMode: ReadWriteOnce
- Size: 10Gi
- Path: `/data/registry`

### 4. Service Layer

Kubernetes services for internal communication.

**Services:**
- `mcp-registry`: ClusterIP service on port 8080
- `toolhive-operator`: ClusterIP service on port 8443

### 5. Ingress Layer

OpenShift Route for external access.

**Route Configuration:**
- TLS Termination: Edge
- Insecure Traffic: Redirect to HTTPS
- Target Service: `mcp-registry:8080`

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     External Users                       │
└────────────────────────┬────────────────────────────────┘
                         │ HTTPS
                         │
┌────────────────────────▼────────────────────────────────┐
│                  OpenShift Route                         │
│              (TLS Edge Termination)                      │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP
                         │
┌────────────────────────▼────────────────────────────────┐
│              MCP Registry Service                        │
│                  (ClusterIP:8080)                        │
└────────────────────────┬────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼────────┐  ┌───▼───────┐  ┌────▼──────────┐
│ MCP Registry   │  │ ConfigMap │  │ PersistentVol │
│   Pod(s)       │──│  (Config) │  │   (Storage)   │
│                │  └───────────┘  └───────────────┘
└────────┬───────┘
         │
         │ Managed by
         │
┌────────▼──────────────────────────────────────────────┐
│              ToolHive Operator                         │
│           (Lifecycle Management)                       │
└────────────────────────────────────────────────────────┘
```

## Data Flow

### Tool Registration Flow

1. User sends POST request to `/api/v1/tools` with tool definition
2. Route forwards request to MCP Registry Service
3. Service routes to MCP Registry Pod
4. Registry validates tool definition
5. Registry stores tool as JSON file in persistent storage
6. Registry returns success response

### Tool Retrieval Flow

1. User sends GET request to `/api/v1/tools/{tool_name}`
2. Route forwards request to MCP Registry Service
3. Service routes to MCP Registry Pod
4. Registry reads tool definition from persistent storage
5. Registry returns tool definition as JSON

### Operator Management Flow

1. ToolHive Operator watches for Registry custom resources
2. Operator reconciles desired state with actual state
3. Operator creates/updates/deletes Kubernetes resources
4. Operator monitors health and performs self-healing

## Security Considerations

### Network Security

- All external traffic uses TLS (HTTPS)
- Internal traffic uses ClusterIP services (cluster-only)
- Network policies can be added for additional isolation

### Authentication & Authorization

Current implementation:
- No authentication (demo/development mode)
- No authorization checks

Production recommendations:
- Enable OAuth/OIDC authentication
- Implement RBAC for API access
- Use ServiceMesh for mTLS

### Pod Security

- Pods run as non-root user (when configured)
- SecurityContext with dropped capabilities
- ReadOnlyRootFilesystem (where applicable)
- Seccomp profile: RuntimeDefault

## Scalability

### Current Configuration

- Single replica deployment
- Suitable for demo and development

### Scaling Recommendations

For production:
- **Horizontal Scaling**: Increase replicas (requires ReadWriteMany storage)
- **Vertical Scaling**: Increase CPU/memory limits
- **Storage**: Use enterprise storage with snapshots
- **Caching**: Add Redis for frequently accessed tools
- **Database**: Replace filesystem with PostgreSQL/MongoDB

## High Availability

For production environments:

1. **Multiple Replicas**: Deploy 3+ registry replicas
2. **Pod Anti-Affinity**: Spread replicas across nodes/zones
3. **ReadWriteMany Storage**: Use NFS, CephFS, or cloud storage
4. **Load Balancing**: OpenShift Route provides automatic load balancing
5. **Health Checks**: Configured for liveness and readiness

## Monitoring & Observability

### Health Endpoints

- `/health`: Basic health check
- `/ready`: Readiness probe

### Metrics (Future)

- Tool registration/retrieval rates
- API response times
- Storage usage
- Error rates

### Logging

- Structured JSON logging
- Stdout/stderr collection by OpenShift
- Integration with cluster logging stack

## Backup & Recovery

### Backup Strategy

1. **PVC Snapshots**: Regular snapshots of `mcp-registry-data`
2. **ConfigMap Backups**: Export ConfigMaps regularly
3. **Export Tools**: Use API to export all tools as JSON

### Recovery Procedures

1. Restore PVC from snapshot
2. Redeploy manifests
3. Verify data integrity

## Technology Stack

- **Container Platform**: OpenShift 4.12+
- **Language**: Python 3.x
- **Web Framework**: Flask
- **Storage**: Kubernetes PersistentVolumes
- **Operator Framework**: Kubernetes Operators (Go)
- **Configuration Format**: JSON/YAML

## API Specification

See [API Reference](api-reference.md) for detailed API documentation.

## Related Documentation

- [Troubleshooting Guide](troubleshooting.md)
- [MCP Specification](https://modelcontextprotocol.io/)
- [OpenShift Documentation](https://docs.openshift.com/)
