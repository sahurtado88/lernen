# Tiempo estimado

Depende de tu dedicación:

Básico (2–4 semanas): Aprendes a moverte con soltura, ejecutar scripts sencillos y automatizar tareas pequeñas.

Intermedio (2–3 meses): Manejo fluido de condicionales, bucles, funciones, regex y manejo avanzado de variables.

Avanzado/Ninja (6–12 meses): Puedes optimizar scripts grandes, depurar, integrar con otros lenguajes (Python, awk, sed, jq), aplicar buenas prácticas y escribir utilidades robustas para producción.

Con práctica diaria en entornos reales (por ejemplo, automatizando tu trabajo en DevOps), en menos de un año puedes sentirte muy sólido.

# Conceptos que debes dominar a la perfección

- Fundamentos de shell

- Diferencia entre sh, bash, zsh.

- Manejo de procesos (ps, jobs, kill, fg, bg).

- Redirecciones (>, >>, <, 2>, &>).

- Pipes (|) y sustitución de comandos $( ).

## Variables y entorno

- Variables locales, globales y de entorno.
 
- Expansiones: \${}, "$@", ${#var}, ${var/patron/reemplazo}.

## Arrays y diccionarios.

## Estructuras de control

- Condicionales: if, [[ ]], case.

- Bucles: for, while, until.

- Break/continue.

## Funciones y modularidad

- Declaración y scope de variables.

- Uso de return y $?.

- Reutilización de código con source.

- Expresiones regulares y filtros

- Uso de grep, sed, awk, cut, sort, uniq.

## Regex básicas y extendidas.

- Procesar logs y archivos CSV/JSON.

- Gestión avanzada

- Trampas (trap) para señales.

- Manejo de errores (set -e, set -u, set -o pipefail).

- Depuración (bash -x script.sh).

- Interacción con el sistema

- Cron jobs y automatización.

- SSH y scripting remoto.

- Integración con utilidades externas (curl, jq, tar, gzip).

- Buenas prácticas

- Código legible y comentado.

- Uso de shellcheck para validar.



# Ruta de estudio recomendada

## Nivel básico

Aprende comandos de uso diario (ls, cd, cat, less, tail, head).

Haz mini scripts para automatizar cosas simples (ej: backup de un directorio).

## Nivel intermedio

Profundiza en variables, condicionales y bucles.

Empieza a manipular texto con awk, sed, grep.

Construye un script de monitoreo básico (ej: chequear si un servicio está arriba).

## Nivel avanzado

Trabaja con señales, errores y debugging.

Escribe funciones reutilizables y librerías de bash.

Automatiza pipelines completos de DevOps (ej: despliegues con logs y validaciones).

## Perfeccionamiento

Revisa código de otros (ej. scripts en GitHub).

Aprende a escribir scripts “idempotentes” y seguros.

Combínalo con Python para tareas más complejas.



# Ruta semanal para volverte “ninja” en Bash

🔹 Semana 1 – Fundamentos de la terminal

Conceptos: ls, cd, pwd, man, history, redirecciones >, >>, <, tuberías |.

Ejercicios:

Crea un script que liste todos los archivos de un directorio y guarde la salida en un log.

Usa history para repetir comandos y redirige errores a un archivo (2>).

🔹 Semana 2 – Variables y entorno

Conceptos: variables locales y de entorno, echo, export, $PATH, sustitución de comandos \$( ).

Ejercicios:

Escribe un script que imprima el nombre de usuario y la fecha actual.

Crea un script que cuente cuántos procesos tuyos están corriendo (ps -u $USER | wc -l).

🔹 Semana 3 – Condicionales

Conceptos: if, else, elif, [[ ]], operadores de strings y números.

Ejercicios:

Script que verifique si un archivo existe y muestre un mensaje.

Script que chequee si un puerto está abierto usando nc -z.

🔹 Semana 4 – Bucles

Conceptos: for, while, until, break, continue.

Ejercicios:

Script que recorra todos los archivos .log de un directorio y cuente sus líneas.

Script que intente conectarse a un host cada 5 segundos hasta que responda.

🔹 Semana 5 – Arrays y funciones

Conceptos: arrays, diccionarios (en bash 4+), funciones y $@, $#.

Ejercicios:

Script que reciba varios argumentos y los recorra en un bucle.

Función que calcule el factorial de un número.

🔹 Semana 6 – Expresiones regulares y manipulación de texto

Conceptos: grep, sed, awk, cut, sort, uniq.

Ejercicios:

Script que busque en un log todas las líneas con “ERROR” y las guarde en otro archivo.

Script que tome un CSV y extraiga solo la segunda columna.

🔹 Semana 7 – Manejo de procesos

Conceptos: jobs, &, fg, bg, kill, sleep.

Ejercicios:

Script que ejecute un comando en background y lo mate después de 10 segundos.

Script que lance varios procesos en paralelo y espere a que terminen (wait).

🔹 Semana 8 – Manejo de errores y debugging

Conceptos: set -e, set -u, set -o pipefail, trap, bash -x.

Ejercicios:

Script que falle al faltar una variable obligatoria.

Script que capture señales (SIGINT) y limpie recursos antes de salir.

🔹 Semana 9 – Automatización del sistema

Conceptos: cron, systemd, ssh, scp.

Ejercicios:

Script que se ejecute cada día para hacer backup de un directorio en /tmp.

Script que copie archivos automáticamente a un servidor remoto.

🔹 Semana 10 – Integración con utilidades externas

Conceptos: curl, jq, tar, gzip.

Ejercicios:

Script que consuma una API REST y muestre un valor JSON específico.

Script que comprima y mueva archivos antiguos a una carpeta de backups.

🔹 Semana 11 – Buenas prácticas

Conceptos: shellcheck, convenciones de estilo, modularidad con source.

Ejercicios:

Refactoriza un script viejo dividiéndolo en funciones.

Pásalo por shellcheck y corrige errores/advertencias.

🔹 Semana 12 – Proyecto final

Proyecto: Escribe un script robusto para monitorear servicios.

Debe aceptar parámetros (ej: lista de hosts).

Validar que los servicios estén arriba (ej: ping/puertos).

Generar un log de errores.

Enviar una alerta (por mail, Slack o Telegram usando una API).

## Consejos extra

Practica en tu día a día: cada tarea manual → piensa si puedes automatizarla.

Guarda todos tus scripts en un repo de GitHub (te servirá como portafolio).

Lee código ajeno: los scripts de /etc/init.d o proyectos open source son oro puro.

#  Recursos de estudio para volverte “ninja” en Bash
🔹 Nivel Básico (Semanas 1–4)

Libros / Guías

GNU Bash Reference Manual (oficial)
 → la biblia de Bash.

The Linux Command Line de William Shotts → excelente para empezar desde cero.

Cursos / Tutoriales

Linux Survival
 → interactivo y gratuito.

Tutorial de Bash en TLDP
 → completo y en texto.

Práctica

OverTheWire Bandit
 → retos de terminal para aprender jugando.

🔹 Nivel Intermedio (Semanas 5–8)

Libros / Guías

Learning the bash Shell (O’Reilly) → buen equilibrio entre teoría y práctica.

Advanced Bash-Scripting Guide
 → clásico con ejemplos.

Cursos / Videos

Udemy: Linux Shell Scripting: A Project-Based Approach to Learning (práctico y con proyectos).

FreeCodeCamp en YouTube: Bash Scripting Full Course (4 horas, gratis).

Práctica

Escribir scripts para problemas cotidianos (monitoreo, backups, logs).

Reto: convierte un proceso manual de tu trabajo en un script reutilizable.

🔹 Nivel Avanzado (Semanas 9–12)

Libros / Guías

Shell Scripting: Expert Recipes for Linux, Bash and more (Packt) → casos reales de automatización.

Bash Pitfalls
 → lista de errores comunes y cómo evitarlos.

Cursos / Videos

Pluralsight: Shell Scripting with Bash (más enfocado en automatización de sistemas).

Egghead.io: mini-lecciones rápidas sobre scripting en Linux.

Práctica Avanzada

Usa ShellCheck
 para analizar y mejorar tu código.

Proyectos open-source en GitHub: busca scripts en repos de DevOps para leer y entender buenas prácticas.

Crea un script de monitoreo completo que use APIs externas y manejo de errores.

🔹 Recursos generales (para cualquier nivel)

Cheat Sheets

DevHints Bash Cheatsheet
 → rápida referencia.

ExplainShell
 → te explica línea por línea cualquier comando.

Foros / Comunidad

Stack Overflow
 → la mayoría de tus dudas ya están respondidas.

Reddit: /r/bash
 y /r/linuxadmin
.


🗺️ Mapa de Proyectos en Bash
🔹 Nivel 1 – Proyectos básicos (Semanas 1–4)

Objetivo: ganar fluidez con la terminal, variables y estructuras de control.

Gestor de notas simple

Script que permita agregar, listar y borrar notas en un archivo de texto.

Usa case para un menú interactivo.

Backup rápido

Script que copie todos los archivos .txt de un directorio a una carpeta /backup/fecha/.

Redirecciones de errores y logs.

Contador de palabras

Script que reciba un archivo y cuente cuántas veces aparece cada palabra.

Usa tr, sort, uniq -c.

🔹 Nivel 2 – Proyectos intermedios (Semanas 5–8)

Objetivo: practicar arrays, funciones, regex, sed/awk y manejo de procesos.

Buscador de logs

Script que busque en archivos .log las líneas con ERROR, WARNING o INFO.

Permitir filtro por fecha y exportar resultados a CSV.

Monitoreo de procesos

Script que muestre los procesos de un usuario cada X segundos.

Si detecta un proceso específico, lo reinicia o envía una alerta.

Gestor de usuarios (modo CLI)

Script con funciones para agregar, eliminar y listar usuarios del sistema.

Usa awk para procesar /etc/passwd.

Debe validar permisos de root.

🔹 Nivel 3 – Proyectos avanzados (Semanas 9–12)

Objetivo: integrar utilidades externas, manejo de errores, automatización real.

Script de despliegue automático

Crea un script que:

Reciba como parámetro un proyecto (ej: app web).

Comprima con tar y copie a un servidor remoto (scp).

Ejecute comandos vía ssh para reiniciar el servicio.

Debe registrar logs y fallos.

Monitoreo de servicios con alertas

Chequea cada X segundos si un servicio está activo (ej: nginx, mysql).

Guarda historial en un log.

Si falla, envía alerta a Slack/Telegram con curl y jq.

Programador de tareas (mini-cron)

Script que ejecute comandos definidos en un archivo tasks.txt.

Cada línea tiene: HH:MM comando.

El script debe correr en background y lanzar los comandos en la hora indicada.

🔹 Nivel 4 – Proyecto final (consolidación)

Objetivo: juntar todo lo aprendido en un solo script robusto.

Herramienta DevOps de administración

Script con menú principal (case) que permita:

Monitoreo: revisar estado de servicios y puertos.

Backups: comprimir directorios y subirlos a un servidor remoto.

Logs: buscar errores en tiempo real en logs (tail -f).

Usuarios: crear/eliminar cuentas con validaciones.

Requisitos:

Uso de funciones modulares.

Manejo de errores (set -euo pipefail, trap).

Logs detallados.

Configuración en un archivo externo (config.conf).

⚡ Recomendación

Lleva todos estos proyectos en un repo de GitHub (con commits claros).

Documenta con un README.md cada script (objetivo, cómo usarlo, ejemplos).

Esto te sirve como portafolio profesional y práctica real.