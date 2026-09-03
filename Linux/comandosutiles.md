# Crear direcrotios y subdirectorios 

mkdir -p myapp/{src/componentes,asests,test/tets.py,test/load.py} 

# Borrar un directorio vacío
rmdir nombre_del_directorio

rmdir carpeta

⚠️ Solo funciona si la carpeta está completamente vacía.

# Borrar un directorio con contenido
rm -r nombre_del_directorio

Ejemplo:
rm -r carpeta

# ☠️ Borrar sin pedir confirmación (forzado)
rm -rf nombre_del_directorio


-r → recursivo
-f → force (no pregunta nada)

Ejemplo:

rm -rf carpeta


⚠️ Esto borra TODO sin confirmación. No pasa por la papelera.

🛑 Recomendación segura

Si no estás 100% seguro:

rm -ri carpeta


Te pedirá confirmación archivo por archivo.

# ver rama en el prompt

autoload -Uz vcs_info
precmd() { vcs_info }

setopt prompt_subst
PROMPT='%F{green}%n%f %F{blue}%2~%f %F{yellow}${vcs_info_msg_0_}%f $ '
zstyle ':vcs_info:git:*' formats '%b'

NOTA PROMPT='%F{green}%n%f %F{blue}%2~%f %F{yellow}${vcs_info_msg_0_}%f $ '  muestra dos direcotrios arriba
PROMPT='%F{green}%n%f %F{blue}%~%f %F{yellow}${vcs_info_msg_0_}%f $ ' muestra directorio desde raiz
