Los VPC Endpoints son una forma de conectar tu VPC con servicios de AWS sin salir a Internet y (muchas veces) sin usar NAT. En vez de ir “VPC → Internet/NAT → servicio”, vas “VPC → endpoint privado → servicio”.

Hay dos tipos principales y conviene entenderlos bien porque funcionan distinto:

1) Gateway Endpoints (solo S3 y DynamoDB)
Qué son

Un Gateway Endpoint es una entrada de ruta en tus route tables que hace que el tráfico hacia S3 o DynamoDB vaya por la red privada de AWS.

Características clave

Servicios soportados: solo S3 y DynamoDB.

Dónde se configuran: en route tables (no en subnets directamente).

No usan ENIs (no crean interfaces de red).

No hay security group asociado al endpoint.

Control de acceso: con Endpoint Policy (y luego S3 Bucket Policy / IAM).

Cómo “se siente” en red

Tus instancias siguen resolviendo S3 con el hostname normal (s3.<region>.amazonaws.com) y la ruta “se va por el endpoint”.

No necesitas NAT para que una instancia en subred privada acceda a S3/DynamoDB.

Caso típico

Instancias privadas que descargan paquetes/artefactos de S3 sin Internet.

Workloads que escriben en S3 y no quieres pagar NAT ni exponer salida.

2) Interface Endpoints (PrivateLink) — “para casi todo lo demás”
Qué son

Un Interface Endpoint crea una o más ENIs (Elastic Network Interfaces) en tus subnets. Esas ENIs tienen IPs privadas dentro de tu VPC. Tu tráfico a un servicio de AWS se conecta a esas IPs privadas por HTTPS (normalmente 443).

En el fondo esto es AWS PrivateLink: tú “entras” por una interfaz privada y AWS enruta hacia el servicio.

Características clave

Servicios soportados: la mayoría (SSM, EC2 API, ECR, CloudWatch Logs, KMS, Secrets Manager, STS, etc.) y también servicios propios/terceros publicados por PrivateLink.

Dónde se colocan: eliges subnets (una por AZ recomendada).

Sí usan ENIs y por lo tanto:

Consumen IPs en tus subnets.

Puedes asociar Security Groups al endpoint.

Acceso controlable con:

Security Group del endpoint (quién puede conectarse a la interfaz).

Endpoint Policy (qué acciones/recursos se permiten) en muchos servicios.

IAM del llamador (siempre aplica).

DNS: normalmente habilitas “Private DNS” para que el hostname público del servicio resuelva a tus IPs privadas.

Detalle importante: Private DNS

Cuando activas Private DNS para un interface endpoint, AWS hace que en tu VPC:

ssm.<region>.amazonaws.com (por ejemplo) resuelva a las IPs privadas del endpoint.

Así, tu app no cambia URLs; solo cambia la resolución DNS “por dentro”.

Si NO activas Private DNS, igual puedes usarlo, pero tendrías que apuntar a un hostname específico del endpoint (más feo y propenso a errores).

Conceptos que de verdad importan
A) ¿Qué problema resuelven?

Sin Internet: Subnets privadas sin NAT/IGW pueden hablar con AWS.

Seguridad: menos superficie (sin egress a Internet), y puedes forzar que S3/SSM solo se usen desde tu VPC.

Costo: reduces/eliminas costo de NAT (aunque interface endpoints tienen costo propio).

Cumplimiento: tráfico se mantiene en la red de AWS.

B) Flujo mental “antes vs después”

Sin endpoints (subred privada):

EC2 → route table 0.0.0.0/0 → NAT → IGW → endpoint público del servicio

Con endpoints:

Para S3/DynamoDB: EC2 → route table (prefix list de S3/DDB) → gateway endpoint → servicio

Para SSM/otros: EC2 → IP privada del ENI del endpoint → PrivateLink → servicio

C) Seguridad y control (lo que te salva en auditorías)
1) Endpoint Policies

Son políticas que se “pegan” al endpoint y actúan como un filtro adicional. Aun si IAM permite algo, la endpoint policy puede bloquearlo.

En S3 gateway endpoint: muy usado para permitir solo ciertos buckets o acciones.

En interface endpoints: depende del servicio, pero cuando aplica, es útil para restringir.

2) Security Groups (solo Interface endpoints)

Puedes decir: “solo desde estas subnets / SGs / IPs se puede conectar al endpoint”.

Ejemplo: el endpoint de Secrets Manager solo aceptará tráfico desde tu SG de apps.

3) Políticas del servicio destino (ej. S3 Bucket Policy)

En S3 es muy común usar condiciones tipo:

Permitir acceso solo si viene desde un endpoint específico (aws:sourceVpce).

O incluso solo desde cierto VPC (aws:sourceVpc, depende del caso).

Resultado: aunque alguien robe credenciales, desde fuera de tu VPC no puede acceder al bucket.

D) Routing vs DNS (diferencia crítica)

Gateway endpoint: la magia pasa en routing (route tables).

Interface endpoint: la magia pasa mucho en DNS (Private DNS) + ENIs.

Por eso, cuando algo “no funciona”:

En gateway: revisas route tables.

En interface: revisas DNS/Private DNS, SG del endpoint, NACLs, y que estés en subnets/AZ correctas.

Costos (muy importante para decidir)
Gateway endpoints

Normalmente sin costo por hora del endpoint (S3/DDB).

Sigues pagando lo normal del servicio (requests, storage, etc.).

Interface endpoints

Costo por hora por endpoint por AZ (porque creas ENIs por AZ).

Costo por GB procesado.

Aun así, puede ser más barato que NAT en ciertos patrones… o más caro si creas muchos endpoints sin control.

Regla práctica:

Si tu uso principal es S3: gateway endpoint casi siempre “sí”.

Si vas a necesitar 10+ servicios por interface endpoints, compara contra NAT, y revisa si te conviene centralizar egress o usar endpoints solo para servicios críticos.

Ejemplos reales (muy comunes)
1) EC2 sin Internet usando SSM (tu caso original)

Para que Session Manager funcione sin NAT/Internet, normalmente necesitas interface endpoints:

ssm

ec2messages

ssmmessages

Y la instancia con:

SSM Agent

Rol AmazonSSMManagedInstanceCore

SG/NACL que permitan salida a 443 (en realidad es conexión dentro de la VPC a las IPs del endpoint).

2) ECR en subnets privadas sin NAT

Necesitas interface endpoints para:

ecr.api

ecr.dkr
y casi siempre también:

s3 (para capas, depende del flujo) → aquí suele convenir gateway endpoint S3.

3) CloudWatch Logs sin NAT

Interface endpoint:

logs

Diseño recomendado (buenas prácticas)

Uno por AZ (Interface endpoints)

Si tienes subnets privadas en 2 AZ, crea el endpoint en 2 subnets (una por AZ) para resiliencia.

Security Group del endpoint restrictivo

Permite inbound 443 SOLO desde los SGs de tus workloads.

Private DNS activado

Para que tus apps usen los hostnames normales.

Evita “crear endpoints por crear”

Haz lista de servicios realmente usados desde subnets privadas.

Mide costos vs NAT.

Usa políticas para forzar tráfico privado

Ejemplo: en S3, bucket policy con aws:sourceVpce para que solo funcione vía endpoint.

Lista rápida de “¿cuál uso?”

Quiero acceso privado a S3/DynamoDB → Gateway endpoint

Quiero acceso privado a SSM, KMS, Logs, Secrets Manager, STS, ECR, etc. → Interface endpoint

Quiero consumir un servicio de otra cuenta/tercero de forma privada → Interface endpoint / PrivateLink

https://chatgpt.com/c/6967c160-68d0-832d-84f1-e8229ae1b3e6