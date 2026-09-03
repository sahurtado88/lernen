# puedes darm un ejemplo para que el pod traiga la imagen de un ecr

Usar:

ServiceAccount
IAM Role
IRSA (IAM Roles for Service Accounts)

Así el Pod obtiene credenciales temporales automáticamente y NO guardas passwords/docker secrets.

```
Pod
  ↓
ServiceAccount
  ↓
IAM Role
  ↓
Permiso para ECR
  ↓
Pull image
````

1. Crear IAM Policy

Permisos mínimos para pull desde ECR:
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchCheckLayerAvailability"
      ],
      "Resource": "*"
    }
  ]
}
```
2. Crear IAM Role con trust policy IRSA

Ejemplo trust relationship:
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/oidc.eks.us-east-1.amazonaws.com/id/XXXX"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.us-east-1.amazonaws.com/id/XXXX:sub": "system:serviceaccount:orders:orders-api-sa"
        }
      }
    }
  ]
}
```
3. Asociar el role a la ServiceAccount
```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: orders-api-sa
  namespace: orders
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/orders-api-ecr-role
```
4. Deployment
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-api
  namespace: orders

spec:
  replicas: 2

  selector:
    matchLabels:
      app: orders-api

  template:
    metadata:
      labels:
        app: orders-api

    spec:
      serviceAccountName: orders-api-sa

      containers:
      - name: orders-api
        image: 123456789012.dkr.ecr.us-east-1.amazonaws.com/orders-api:1.0.0

        imagePullPolicy: IfNotPresent

        ports:
        - containerPort: 8080
```
