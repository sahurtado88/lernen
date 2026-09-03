Para reducir significativamente el riesgo de ataques en un pod de Kubernetes, las fuentes destacan varios parámetros clave dentro del securityContext que limitan los privilegios y las acciones que un atacante puede realizar:

runAsUser y runAsNonRoot: Por defecto, los contenedores se ejecutan como el usuario root, el más privilegiado en Linux, lo que permitiría a un atacante instalar malware o herramientas como curl para descargar archivos maliciosos


Configurar runAsUser con un ID de usuario que no sea root obliga a todos los contenedores a ejecutarse sin privilegios administrativos

El parámetro runAsNonRoot: true actúa como una medida de seguridad adicional que fuerza la ejecución como un usuario no raíz, ya sea mediante la configuración del pod o del Dockerfile.

allowPrivilegeEscalation: false: Este parámetro es fundamental para evitar que un proceso gane más privilegios de los que tiene su proceso padre, bloqueando el uso de herramientas como sudo para elevar permisos temporalmente y realizar funciones administrativas

readOnlyRootFilesystem: true: Al establecer el sistema de archivos como de solo lectura, se impide que un atacante escriba archivos maliciosos, instale mineros de criptomonedas o configure puertas traseras, incluso si logra explotar una vulnerabilidad de ejecución remota de código


El contenedor solo podrá escribir en los montajes de volumen autorizados, protegiendo los archivos críticos del sistema operativo

capabilities (drop: ["ALL"]): Las capacidades de Linux permiten realizar llamadas al sistema (como cambiar la hora o interactuar con hardware) que las aplicaciones comunes no suelen necesitar

Al eliminar todas las capacidades por defecto, se quita al atacante cualquier "combustible" para explotar llamadas al sistema operativo y comprometer el nodo


Además de estos parámetros, las fuentes recomiendan complementar la seguridad utilizando imágenes base más pequeñas (como Alpine o versiones "slim") para reducir la cantidad de herramientas disponibles para un atacante

En casos de aplicaciones que se compilan como binarios estáticos (como Go o Rust), se sugiere usar la imagen scratch, que está vacía y no contiene terminales ni utilidades de sistema