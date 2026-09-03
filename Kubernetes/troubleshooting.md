# Kubernetes & Amazon EKS Troubleshooting Guide

Guía práctica orientada a troubleshooting operativo y diagnóstico en entornos Kubernetes y Amazon EKS de producción.

---

# Tabla de contenido

1. Troubleshooting de Pods
2. Troubleshooting de Nodos
3. Troubleshooting de Networking
4. Troubleshooting específico de Amazon EKS
5. Troubleshooting de almacenamiento
6. Comandos esenciales
7. Buenas prácticas operativas

---

# 1. Troubleshooting de Pods

## Pods en CrashLoopBackOff

### Síntomas

- Reinicios constantes del contenedor
- Estado:
```bash
CrashLoopBackOff
```

### Diagnóstico

```bash
kubectl describe pod <pod>
kubectl logs <pod> --previous
kubectl get events --sort-by=.metadata.creationTimestamp
```

### Solución

- Revisar logs de aplicación
- Validar ConfigMaps y Secrets
- Ajustar requests/limits
- Verificar dependencias externas

---

## Pods en ImagePullBackOff

### Diagnóstico

```bash
kubectl describe pod <pod>
aws ecr describe-images --repository-name myrepo
```

### Solución

```bash
aws ecr get-login-password
```

---

## Pods Pending

### Diagnóstico

```bash
kubectl describe pod <pod>
kubectl top nodes
```

### Eventos comunes

```text
0/5 nodes are available: insufficient memory
```

---

## Pods OOMKilled

### Diagnóstico

```bash
kubectl top pod
kubectl describe pod <pod>
```

### Ejemplo

```yaml
resources:
  requests:
    memory: "512Mi"
  limits:
    memory: "1Gi"
```

---

## Problemas de probes

### Ejemplo

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  timeoutSeconds: 5
```

---

# 2. Troubleshooting de Nodos

## Nodo NotReady

### Diagnóstico

```bash
kubectl get nodes
kubectl describe node <node>
journalctl -u kubelet -f
```

---

## Presión de memoria/disco

### Diagnóstico

```bash
df -h
du -sh /var/lib/containerd/*
```

### Limpieza

```bash
crictl rmi --prune
```

---

## Problemas de kubelet

```bash
systemctl restart kubelet
journalctl -u kubelet
```

---

# 3. Troubleshooting de Networking

## DNS failures

```bash
kubectl exec -it <pod> -- nslookup kubernetes.default
```

---

## CoreDNS

```bash
kubectl logs -n kube-system deployment/coredns
kubectl rollout restart deployment coredns -n kube-system
```

---

## Problemas de CNI

```bash
kubectl logs -n kube-system daemonset/aws-node
```

---

## Comunicación entre pods

```bash
kubectl exec -it <pod> -- curl http://service
kubectl get endpoints
```

---

# 4. Troubleshooting específico de Amazon EKS

## aws-node issues

```bash
kubectl logs -n kube-system daemonset/aws-node
```

---

## IRSA failures

```bash
kubectl describe sa
aws iam get-role
```

---

## EBS CSI Driver issues

```bash
kubectl logs deployment/ebs-csi-controller -n kube-system
```

---

## ALB Controller

```bash
kubectl logs deployment/aws-load-balancer-controller -n kube-system
```

---

## Cluster Autoscaler / Karpenter

```bash
kubectl logs deployment/cluster-autoscaler -n kube-system
kubectl logs deployment/karpenter -n karpenter
```

---

# 5. Troubleshooting de almacenamiento

## PVC Pending

```bash
kubectl describe pvc
```

---

## StorageClass

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
```

---

# 6. Comandos esenciales

## kubectl

```bash
kubectl get pods -A
kubectl logs <pod>
kubectl describe pod <pod>
kubectl get events
```

---

## AWS CLI

```bash
aws eks describe-cluster --name <cluster>
aws eks describe-nodegroup
```

---

## crictl

```bash
crictl ps
crictl logs <container-id>
```

---

# 7. Buenas prácticas operativas

## Observabilidad

| Herramienta | Uso |
|---|---|
| Prometheus | Métricas |
| Grafana | Dashboards |
| Loki | Logs |
| Tempo | Tracing |

---

## Alta disponibilidad

- Multi-AZ
- HPA + Cluster Autoscaler
- PDBs
- Readiness probes

---

## Seguridad

| Área | Recomendación |
|---|---|
| IAM | Least privilege |
| Networking | NetworkPolicies |
| Secrets | External Secrets |

---
