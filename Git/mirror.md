# Sincronizar Azure DevOps → GitHub usando SSH

## Objetivo:
```
Azure DevOps repo:
iac-external-platform-core
rama: iac

↓ sincroniza hacia ↓

GitHub repo:
dfx5-ms-aws-bhd
rama: feature/terraform
```

# Paso a Paso


1. Clonar el repositorio de Azure DevOps
```
git clone https://dev.azure.com/bhdleon/BHD-IT-CLOUDOPSySRE/_git/iac-external-platform-core

cd iac-external-platform-core
```
2. Cambiar a la rama origen
```
git checkout iac
```
Verificar:
```
git branch
```
Debe aparecer:
```
* iac
```
3. Agregar el repositorio GitHub usando SSH

Agregar remote:
```
git remote add github git@github-sergio:dfx5/dfx5-ms-aws-bhd.git
```
4. Verificar remotes
```
git remote -v
```
Debe verse algo parecido a:
```
origin  https://dev.azure.com/bhdleon/BHD-IT-CLOUDOPSySRE/_git/iac-external-platform-core (fetch)

origin  https://dev.azure.com/bhdleon/BHD-IT-CLOUDOPSySRE/_git/iac-external-platform-core (push)

github  git@github-sergio:dfx5/dfx5-ms-aws-bhd.git (fetch)

github  git@github-sergio:dfx5/dfx5-ms-aws-bhd.git (push)

```
5. Hacer el primer push hacia GitHub
```
git push github iac:feature/terraform --force
```

Esto significa:

rama local:      iac

rama remota GH:  feature/terraform

6. Verificar en GitHub

Validar que exista la rama:
```
feature/terraform
```
en:
```
dfx5-ms-aws-bhd
```
7. Automatizar sincronización desde GitHub Actions

Crear archivo:
```
.github/workflows/sync-from-azure.yml
```
Contenido:
```
name: Sync from Azure Repo

on:
  workflow_dispatch:
  schedule:
    - cron: "*/15 * * * *"

permissions:
  contents: write

jobs:
  sync:
    runs-on: ubuntu-latest

    steps:
      - name: Clone Azure repo branch iac
        run: |
          git clone --branch iac --single-branch \
            https://Sergio:${{ secrets.AZURE_DEVOPS_PAT }}@dev.azure.com/bhdleon/BHD-IT-CLOUDOPSySRE/_git/iac-external-platform-core \
            source

      - name: Push to GitHub feature/terraform
        run: |
          cd source

          git config user.name "github-actions-sync"
          git config user.email "github-actions-sync@users.noreply.github.com"

          git remote add github https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/dfx5/dfx5-ms-aws-bhd.git

          git push github HEAD:refs/heads/feature/terraform --force
```

8. Crear PAT en Azure DevOps

Ir a:
```
Azure DevOps PATs

Crear un Personal Access Token con permiso:

Code → Read

Copiar el token.
```
9. Crear secret en GitHub

Ir al repo GitHub:
```
Settings
→ Secrets and variables
→ Actions
→ New repository secret

Crear:

AZURE_DEVOPS_PAT

Valor:

<tu PAT de Azure DevOps>

```

10. Ejecutar workflow manualmente

Ir a:
```
GitHub
→ Actions
→ Sync from Azure Repo
→ Run workflow
```
O esperar ejecución automática cada 15 minutos.

Resultado final

Cada cambio en:

Azure DevOps
rama iac

se copiará automáticamente a:

GitHub
rama feature/terraform
Consideraciones importantes
El --force

Este comando sobrescribe la rama destino:

git push --force

Por eso:

Azure DevOps será la fuente oficial.
No debes hacer commits manuales en:
feature/terraform

porque se perderán en la próxima sincronización.

## Comando manual rápido de sincronización

Si quieres sincronizar manualmente:
```
git checkout iac

git pull origin iac

git push github iac:feature/terraform --force
```