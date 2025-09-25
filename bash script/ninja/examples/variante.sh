#!/bin/bash
# Script avanzado con timestamps en errores

DIRECTORIO=${1:-$(pwd)}
LOG_SALIDA="listado_$(date +%Y%m%d_%H%M%S).log"
LOG_ERRORES="errores_$(date +%Y%m%d_%H%M%S).log"

{
    echo "=== LISTADO DE ARCHIVOS ==="
    echo "Fecha: $(date)"
    echo "Directorio: $DIRECTORIO"
    echo "=========================="
    ls -la "$DIRECTORIO"
    echo "Comando ejecutado: ls -la $DIRECTORIO"
} >> $LOG_SALIDA 2>> $LOG_ERRORES

echo "📋 Logs generados:"
echo "   Salida: $LOG_SALIDA"
echo "   Errores: $LOG_ERRORES"