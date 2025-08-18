#!/usr/bin/env bash

set -euo pipefail
IFS=$'\n\t'

# Validar dependencias
command -v jq >/dev/null 2>&1 || { echo >&2 "[ERROR] jq no está instalado. Aborta."; exit 1; }
command -v aws >/dev/null 2>&1 || { echo >&2 "[ERROR] AWS CLI no está instalado. Aborta."; exit 1; }

# Configuraciones
REGION="us-west-2"
INSTANCE_ID="arn:aws:connect:us-west-2:707028784120:instance/cfc23b50-a229-4931-aae8-431bcaf54dd7"
LOCALE_ID="es_419"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
OUTPUT_DIR="output-bot-id"
TEMPLATE_FILE="devops/asociarbotamazon.yaml"
BOTS_ID="devops/$OUTPUT_DIR"

mkdir -p "$OUTPUT_DIR"

echo "Listando bots disponibles..."
bot_ids=$(aws lexv2-models list-bots \
  --region "$REGION" \
  --query "botSummaries[].botId" \
  --output text)

echo "Bots encontrados: $bot_ids"

# Recorrer cada bot
for bot_id in $bot_ids; do
  echo "Procesando bot: $bot_id"

  alias_info=$(aws lexv2-models list-bot-aliases \
    --bot-id "$bot_id" \
    --region "$REGION" \
    --query "botAliasSummaries[0]" \
    --output json)

  alias_id=$(echo "$alias_info" | jq -r '.botAliasId')
  alias_name=$(echo "$alias_info" | jq -r '.botAliasName')

  if [[ "$alias_id" == "null" || "$alias_name" == "null" ]]; then
    echo "No se encontró alias para bot $bot_id. Se omite."
    continue
  fi

  # Verificar si el alias apunta a DRAFT
  current_version=$(aws lexv2-models describe-bot-alias \
    --bot-id "$bot_id" \
    --bot-alias-id "$alias_id" \
    --region "$REGION" \
    --query "botVersion" \
    --output text)

  if [[ "$current_version" == "DRAFT" ]]; then
    echo "Alias $alias_name apunta a DRAFT. Se publicará nueva versión..."
    bot_version=$(aws lexv2-models create-bot-version \
      --bot-id "$bot_id" \
      --region "$REGION" \
      --bot-version-locale-specification "{\"$LOCALE_ID\":{\"sourceBotVersion\":\"DRAFT\"}}" \
      --query "botVersion" \
      --output text)

    echo "Esperando a que la versión $bot_version esté disponible..."
    aws lexv2-models wait bot-version-available \
      --bot-id "$bot_id" \
      --bot-version "$bot_version" \
      --region "$REGION"

    # Intentar actualización con reintentos si falla por propagación
    max_retries=5
    attempt=1
    success=false

    while [[ $attempt -le $max_retries ]]; do
    echo "🔁 Intento $attempt: actualizando alias $alias_name a versión $bot_version..."

    if aws lexv2-models update-bot-alias \
            --bot-id "$bot_id" \
            --bot-alias-id "$alias_id" \
            --bot-alias-name "$alias_name" \
            --bot-version "$bot_version" \
            --region "$REGION"; then
            echo "Alias actualizado exitosamente"
            success=true
            break
    else
            echo "Falló la actualización. Esperando y reintentando..."
            sleep $((attempt * 5))  # espera progresiva: 5s, 10s, 15s...
    fi

        attempt=$((attempt + 1))
    done

    if [[ "$success" != true ]]; then
    echo "No se pudo actualizar el alias $alias_name después de $max_retries intentos"
    exit 1
    fi

    echo "Actualizando alias $alias_name para que apunte a la versión $bot_version..."

    aws lexv2-models update-bot-alias \
      --bot-id "$bot_id" \
      --bot-alias-id "$alias_id" \
      --bot-alias-name "$alias_name" \
      --bot-version "$bot_version" \
      --region "$REGION"

  
  else
    echo "Alias $alias_name ya apunta a la versión publicada $current_version"
  fi

  bot_alias_arn="arn:aws:lex:$REGION:$ACCOUNT_ID:bot-alias/$bot_id/$alias_id"
  json_output_path="$OUTPUT_DIR/${bot_id}.json"

  jq -n \
    --arg connect "$INSTANCE_ID" \
    --arg integration "$bot_alias_arn" \
    '{ConnectInstanceArn: $connect, IntegrationArn: $integration}' \
    > "$json_output_path"

  echo "JSON generado: $json_output_path"
done

# Verificar existencia de la plantilla
if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo "Error: No se encontró la plantilla '$TEMPLATE_FILE'" >&2
  exit 1
fi

# Obtener archivos JSON
shopt -s nullglob
json_files=("$BOTS_ID"/*.json)
if [[ ${#json_files[@]} -eq 0 ]]; then
  echo "No hay archivos .json en '$BOTS_ID'" >&2
  exit 0
fi

# Iterar sobre cada archivo JSON generado
for param_file in "${json_files[@]}"; do
  echo "Procesando stack con parámetros: $param_file"

  if ! jq empty "$param_file" &>/dev/null; then
    echo "Error: $param_file no es un JSON válido" >&2
    continue
  fi

  stack_name="cf-stack-bot-$(basename "$param_file" .json)"
  echo "Desplegando stack: $stack_name"

  if ! aws cloudformation deploy \
    --template-file "$TEMPLATE_FILE" \
    --stack-name "$stack_name" \
    --parameter-overrides $(jq -r 'to_entries | map("\(.key)=\(.value)") | .[]' "$param_file") \
    --capabilities CAPABILITY_NAMED_IAM \
    --region "$REGION"; then
      echo "[ERROR] Falló el despliegue del stack $stack_name" >&2
      continue
  fi

  stack_status=$(aws cloudformation describe-stacks \
    --stack-name "$stack_name" \
    --region "$REGION" \
    --query 'Stacks[0].StackStatus' --output text)

  if [[ "$stack_status" != "CREATE_COMPLETE" && "$stack_status" != "UPDATE_COMPLETE" ]]; then
    echo "[ERROR] Stack $stack_name terminó en estado: $stack_status" >&2
    continue
  fi

  echo "Stack $stack_name desplegado con éxito"
done
