#!/bin/bash

# Script: listar_archivos.sh
# Descripción: Lista archivos de un directorio y guarda todo en logs

# Variables
DIRECTORIO=${1:-$(pwd)}  # Usa el directorio pasado como parámetro o el actual
LOG_SALIDA="listado_archivos.log"
LOG_ERRORES="errores.log"
FECHA=$(date '+%Y-%m-%d %H:%M:%S')

echo "=== INICIO DEL LISTADO - $FECHA ===" >> $LOG_SALIDA
echo "Directorio: $DIRECTORIO" >> $LOG_SALIDA
echo "----------------------------------------" >> $LOG_SALIDA

# Comando principal: listar archivos con detalles
ls -la "$DIRECTORIO" >> $LOG_SALIDA 2>> $LOG_ERRORES

# Verificar si hubo errores
if [ $? -eq 0 ]; then
    echo "✅ Listado completado exitosamente" >> $LOG_SALIDA
else
    echo "❌ Error al listar el directorio - Ver $LOG_ERRORES" >> $LOG_SALIDA
fi

echo "----------------------------------------" >> $LOG_SALIDA
echo "" >> $LOG_SALIDA

# Mostrar resultado en pantalla también
echo "📁 Listado guardado en: $LOG_SALIDA"
echo "🚨 Errores guardados en: $LOG_ERRORES"

# === EJEMPLOS DE USO CON HISTORY ===
echo ""
echo "💡 Comandos útiles para repetir con history:"
echo "   history | grep 'ls -la'     # Buscar comandos ls anteriores"
echo "   !!                          # Repetir último comando"
echo "   !ls                         # Repetir último comando que empezó con 'ls'"
echo "   !123                        # Repetir comando número 123 del history"

# Guardar este script en el history para fácil repetición
echo "bash $0 /ruta/directorio" >> ~/.bash_history