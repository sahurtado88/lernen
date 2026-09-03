# Como hago esto A telecommunications company is planning to host a WordPress website on an Amazon ECS Cluster which uses the Fargate launch type. For security purposes, the database credentials should be provided to the WordPress image by using environment variables. Your manager instructed you to ensure that the credentials are secure when passed to the image and that they cannot be viewed on the cluster itself. The credentials must be kept in a dedicated storage with lifecycle management and key rotation.

Which of the following is the most suitable solution in this scenario that you can implement with the least effort?


Store the database credentials using the AWS Secrets Manager and then encrypt them using AWS KMS. Create an IAM Role for your Amazon ECS task execution role and reference it with your task definition which allows access to both KMS and AWS Secrets Manager. Within your container definition, specify secrets with the name of the environment variable to set in the container and the full ARN of the Secrets Manager secret which contains the sensitive data, to present to the container.

Debes hacerlo con Secrets Manager + ECS task definition secrets, no con variables normales environment.

La idea es:

Guardas usuario/password de la DB en AWS Secrets Manager.
Secrets Manager lo cifra con AWS KMS.
Das permisos al ECS task execution role para:
secretsmanager:GetSecretValue
kms:Decrypt
En la task definition, en el container de WordPress usas secrets, no environment.

Ejemplo conceptual:
```
{
  "family": "wordpress-task",
  "requiresCompatibilities": ["FARGATE"],
  "networkMode": "awsvpc",
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "wordpress",
      "image": "wordpress:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "WORDPRESS_DB_HOST",
          "value": "mydb.xxxxxx.us-east-1.rds.amazonaws.com:3306"
        },
        {
          "name": "WORDPRESS_DB_NAME",
          "value": "wordpress"
        }
      ],
      "secrets": [
        {
          "name": "WORDPRESS_DB_USER",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:wordpress-db-user"
        },
        {
          "name": "WORDPRESS_DB_PASSWORD",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:wordpress-db-password"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/wordpress",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```
La razón por la que esta opción es la correcta:

Secrets Manager está hecho para credenciales sensibles, soporta rotación automática, cifrado con KMS, control de acceso con IAM, y ECS puede inyectar el secreto como variable de entorno sin dejarlo visible directamente en la definición del task.

No sería ideal usar variables normales en la task definition porque quedarían expuestas en texto plano dentro de la configuración del contenedor.

si es modo ec2

```
{
  "family": "wordpress-task",
  "requiresCompatibilities": ["EC2"],
  "networkMode": "bridge",
  "executionRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "wordpress",
      "image": "wordpress:latest",
      "essential": true,
      "memory": 512,
      "cpu": 256,
      "portMappings": [
        {
          "containerPort": 80,
          "hostPort": 8080,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "WORDPRESS_DB_HOST",
          "value": "mydb.xxxxxx.us-east-1.rds.amazonaws.com:3306"
        },
        {
          "name": "WORDPRESS_DB_NAME",
          "value": "wordpress"
        }
      ],
      "secrets": [
        {
          "name": "WORDPRESS_DB_USER",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:wordpress-db-user"
        },
        {
          "name": "WORDPRESS_DB_PASSWORD",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:wordpress-db-password"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/wordpress",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```