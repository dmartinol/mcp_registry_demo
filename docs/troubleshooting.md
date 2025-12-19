# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the MCP Registry deployment.

## Table of Contents

1. [General Troubleshooting Steps](#general-troubleshooting-steps)
2. [Operator Issues](#operator-issues)
3. [Registry Issues](#registry-issues)
4. [Network and Access Issues](#network-and-access-issues)
5. [Storage Issues](#storage-issues)
6. [Performance Issues](#performance-issues)

## General Troubleshooting Steps

### Check Resource Status

```bash
# Check all resources in the namespace
oc get all -n mcp-registry

# Check events for errors
oc get events -n mcp-registry --sort-by='.lastTimestamp'

# Check pod status
oc get pods -n mcp-registry -o wide

# Describe pod for detailed information
oc describe pod <pod-name> -n mcp-registry
```

### View Logs

```bash
# View registry logs
oc logs -n mcp-registry deployment/mcp-registry

# View operator logs
oc logs -n mcp-registry deployment/toolhive-operator

# Follow logs in real-time
oc logs -f -n mcp-registry deployment/mcp-registry

# View previous container logs (if pod crashed)
oc logs -n mcp-registry <pod-name> --previous
```

## Operator Issues

### Operator Pod Not Starting

**Symptoms:**
- Operator pod is in `Pending`, `CrashLoopBackOff`, or `Error` state
- No operator logs available

**Diagnosis:**
```bash
oc describe pod -n mcp-registry -l app=toolhive-operator
oc get events -n mcp-registry | grep toolhive-operator
```

**Common Causes & Solutions:**

1. **Image Pull Errors**
   - Cause: Cannot pull operator image
   - Solution: Verify image name and registry access
   ```bash
   oc describe pod <operator-pod> -n mcp-registry | grep -A 5 "Events"
   ```

2. **Insufficient Permissions**
   - Cause: ServiceAccount lacks required permissions
   - Solution: Verify RBAC configuration
   ```bash
   oc get clusterrole toolhive-operator
   oc get clusterrolebinding toolhive-operator
   ```

3. **Resource Constraints**
   - Cause: Node has insufficient CPU/memory
   - Solution: Check node resources
   ```bash
   oc describe node <node-name>
   oc top nodes
   ```

### Operator Not Reconciling

**Symptoms:**
- Registry resources not being created/updated
- No operator activity in logs

**Diagnosis:**
```bash
oc logs -n mcp-registry deployment/toolhive-operator | tail -100
```

**Solutions:**
1. Check operator logs for errors
2. Verify CRDs are installed: `oc get crd`
3. Restart operator: `oc rollout restart deployment/toolhive-operator -n mcp-registry`

## Registry Issues

### Registry Pod Not Starting

**Symptoms:**
- Registry pod in `Pending`, `CrashLoopBackOff`, or `Error` state
- Health checks failing

**Diagnosis:**
```bash
oc describe pod -n mcp-registry -l app=mcp-registry
oc logs -n mcp-registry deployment/mcp-registry
```

**Common Causes & Solutions:**

1. **PVC Not Bound**
   - Cause: PersistentVolumeClaim pending
   - Solution: Check PVC status
   ```bash
   oc get pvc -n mcp-registry
   oc describe pvc mcp-registry-data -n mcp-registry
   ```
   - Ensure StorageClass is available
   ```bash
   oc get storageclass
   ```

2. **ConfigMap Missing**
   - Cause: Registry config not found
   - Solution: Verify ConfigMaps
   ```bash
   oc get configmap -n mcp-registry
   oc get configmap mcp-registry-config -n mcp-registry -o yaml
   ```

3. **Python Dependencies**
   - Cause: Required Python packages not installed
   - Solution: Check pod logs for import errors
   ```bash
   oc logs -n mcp-registry deployment/mcp-registry | grep -i error
   ```

### Registry Not Responding

**Symptoms:**
- Health endpoints return errors
- API requests timeout

**Diagnosis:**
```bash
# Test from within cluster
oc run -it --rm test-pod --image=curlimages/curl --restart=Never -- \
  curl http://mcp-registry.mcp-registry.svc.cluster.local:8080/health

# Check service endpoints
oc get endpoints -n mcp-registry
```

**Solutions:**

1. **Port Mismatch**
   - Verify service and pod ports match
   ```bash
   oc get svc mcp-registry -n mcp-registry -o yaml
   oc get pod -n mcp-registry -l app=mcp-registry -o yaml | grep containerPort
   ```

2. **Application Error**
   - Check registry logs for Python errors
   ```bash
   oc logs -n mcp-registry deployment/mcp-registry --tail=50
   ```

3. **Resource Limits**
   - Pod may be OOMKilled
   ```bash
   oc describe pod -n mcp-registry -l app=mcp-registry | grep -A 5 "State"
   ```

## Network and Access Issues

### Cannot Access Registry Externally

**Symptoms:**
- Route exists but URL not accessible
- SSL/TLS errors
- 404 or 503 errors

**Diagnosis:**
```bash
# Check route status
oc get route mcp-registry -n mcp-registry

# Get route details
oc describe route mcp-registry -n mcp-registry

# Test DNS resolution
nslookup <route-hostname>
```

**Solutions:**

1. **Route Not Created**
   ```bash
   oc apply -f manifests/04-route.yaml
   ```

2. **TLS Certificate Issues**
   - OpenShift generates certificates automatically
   - For custom certs, verify TLS configuration
   ```bash
   oc get route mcp-registry -n mcp-registry -o yaml | grep -A 10 tls
   ```

3. **Service Not Found**
   - Verify service exists and has endpoints
   ```bash
   oc get svc mcp-registry -n mcp-registry
   oc get endpoints mcp-registry -n mcp-registry
   ```

### Internal Communication Issues

**Symptoms:**
- Pods cannot communicate with registry
- Operator cannot reach registry

**Diagnosis:**
```bash
# Test service from a test pod
oc run -it --rm debug --image=busybox --restart=Never -n mcp-registry -- \
  wget -qO- http://mcp-registry:8080/health
```

**Solutions:**

1. **Network Policy Blocking**
   ```bash
   oc get networkpolicy -n mcp-registry
   ```
   - Adjust or remove restrictive policies

2. **Service Selector Mismatch**
   ```bash
   # Check service selector
   oc get svc mcp-registry -n mcp-registry -o yaml | grep -A 3 selector
   
   # Check pod labels
   oc get pod -n mcp-registry -l app=mcp-registry --show-labels
   ```

## Storage Issues

### PVC Pending

**Symptoms:**
- PersistentVolumeClaim stuck in `Pending` state
- Pod cannot start due to volume mount failure

**Diagnosis:**
```bash
oc describe pvc mcp-registry-data -n mcp-registry
oc get pv
```

**Solutions:**

1. **No Available PV**
   - Ensure StorageClass can dynamically provision
   ```bash
   oc get storageclass
   ```
   - Check if StorageClass is set as default
   ```bash
   oc get storageclass -o yaml | grep -B 3 "is-default-class: \"true\""
   ```

2. **Insufficient Capacity**
   - Reduce requested storage size in PVC
   - Or provision more storage in cluster

3. **Access Mode Not Supported**
   - Change PVC accessMode to match storage capabilities

### Storage Full

**Symptoms:**
- Registry cannot save new tools
- Pod logs show write errors
- `No space left on device` errors

**Diagnosis:**
```bash
# Check PVC usage
oc exec -n mcp-registry deployment/mcp-registry -- df -h /data/registry

# Check PVC size
oc get pvc mcp-registry-data -n mcp-registry
```

**Solutions:**

1. **Expand PVC** (if supported by StorageClass)
   ```bash
   oc patch pvc mcp-registry-data -n mcp-registry -p '{"spec":{"resources":{"requests":{"storage":"20Gi"}}}}'
   ```

2. **Clean Up Old Data**
   ```bash
   oc exec -n mcp-registry deployment/mcp-registry -- ls -lh /data/registry
   # Remove unnecessary files manually
   ```

## Performance Issues

### Slow Response Times

**Symptoms:**
- API requests take longer than expected
- Timeouts occur

**Diagnosis:**
```bash
# Check pod resource usage
oc top pod -n mcp-registry

# Check node resources
oc top nodes

# Review logs for performance issues
oc logs -n mcp-registry deployment/mcp-registry | grep -i slow
```

**Solutions:**

1. **Increase Resource Limits**
   - Edit deployment to increase CPU/memory
   ```bash
   oc edit deployment mcp-registry -n mcp-registry
   ```

2. **Add More Replicas**
   ```bash
   oc scale deployment mcp-registry -n mcp-registry --replicas=3
   ```
   - Note: Requires ReadWriteMany storage

3. **Storage Performance**
   - Use faster StorageClass
   - Check storage I/O metrics

### High Memory Usage

**Symptoms:**
- Pod being OOMKilled
- Pod restarts frequently

**Diagnosis:**
```bash
oc describe pod -n mcp-registry -l app=mcp-registry | grep -A 10 "State"
oc logs -n mcp-registry <pod-name> --previous
```

**Solutions:**

1. **Increase Memory Limit**
   ```yaml
   resources:
     limits:
       memory: 1Gi
     requests:
       memory: 512Mi
   ```

2. **Fix Memory Leaks**
   - Review application code
   - Update to latest stable version

## Getting Help

If you continue to experience issues:

1. **Collect Diagnostic Information**
   ```bash
   # Create a diagnostic bundle
   oc adm inspect namespace/mcp-registry --dest-dir=/tmp/mcp-registry-diagnostics
   ```

2. **Check Documentation**
   - [Architecture Overview](architecture.md)
   - [API Reference](api-reference.md)

3. **Community Support**
   - [MCP Community Forums](https://modelcontextprotocol.io/)
   - [OpenShift Community](https://www.openshift.com/community)

4. **Report Issues**
   - GitHub Issues: [Repository Issues](https://github.com/dmartinol/mcp_registry_demo/issues)
