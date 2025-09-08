Genera una clave SSH para cada cuenta (macOS/Linux; en Windows cambia ~ por %USERPROFILE%):
bash
Copy
# Cuenta 1 (sergiohurtadodfx5)
ssh-keygen -t ed25519 -C "sergio.hurtado@dfx5.com" -f ~/.ssh/id_ed25519_sergio_dfx5

# Cuenta 2 (sahurtado88)
ssh-keygen -t ed25519 -C "sahurtad@gmail.com" -f ~/.ssh/id_ed25519_sahurtado88

# Cuenta 3 (belcrop)
ssh-keygen -t ed25519 -C "extfshurtado@belcorp.biz" -f ~/.ssh/id_ed25519_belcorp

# Inicia ssh-agent y carga las claves:
## macOS/Linux:

eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_sergio_dfx5
ssh-add ~/.ssh/id_ed25519_sahurtado88
ssh-add ~/.ssh/id_ed25519_belcorp

## Windows (PowerShell):

Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
ssh-add $env:USERPROFILE\.ssh\id_ed25519_sergio_dfx5
ssh-add $env:USERPROFILE\.ssh\id_ed25519_sahurtado88
ssh-add $env:USERPROFILE\.ssh\id_ed25519_belcorp

# Copia las claves públicas y añádelas en cada cuenta de GitHub (Settings → SSH and GPG keys → New SSH key), en la cuenta correcta:

cat ~/.ssh/id_ed25519_sergio_dfx5.pub
cat ~/.ssh/id_ed25519_sahurtado88.pub
cat ~/.ssh/id_ed25519_belcorp.pub


Configura ~/.ssh/config con alias separados:

# Cuenta 1: sergiohurtadodfx5
Host github-sergio
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_sergio_dfx5
    IdentitiesOnly yes

# Cuenta 2: sahurtado88
Host github-sahurtado
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_sahurtado88
    IdentitiesOnly yes

# Cuenta 3: sahbelcorpurtado88
Host github-sahurtado
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_belcorp
    IdentitiesOnly yes


Prueba cada conexión:

ssh -T git@github-sergio
ssh -T git@github-sahurtado
Deberías ver un “Hi ! You’ve successfully authenticated…”.

## Clona usando el alias del Host correspondiente:

### Repos de la cuenta 1 (sergiohurtadodfx5)
git clone git@github-sergio:sergiohurtadodfx5/REPO_AQUI.git

git clone git@github-sergio:dfx5/PE-Rimac-Eda-Dev.git

git clone git@github-sergio:dfx5/PE-Rimac-EventCatalog.git

### Repos de la cuenta 2 (sahurtado88)
git clone git@github-sahurtado:sahurtado88/REPO_AQUI.git


# Configura nombre y email por repo (recomendado) para evitar mezclar identidades:

## Dentro de un repo de la cuenta 1
git config user.name "sergiohurtadodfx5"
git config user.email "sergio.hurtado@dfx5.com"

##  Dentro de un repo de la cuenta 2
git config user.name "sahurtado88"
git config user.email "sahurtad@gmail.com"

##  Dentro de un repo de la belcorp
git config user.name "extfshurtado_belcorp"
git config user.email "extfshurtado@belcorp.biz"

# Adicional 

Si ya tienes repos clonados con git@github.com:..., cambia el remote para que use el alias correcto. Por ejemplo, en un repo de la cuenta 1:

git remote set-url origin git@github-sergio:sergiohurtadodfx5/REPO_AQUI.git

Tips rápidos: si ves “Permission denied (publickey)”, confirma que subiste la .pub correcta a la cuenta correcta, que ssh-agent tiene cargada la clave (ssh-add -l), y que estás usando el alias adecuado en la URL remota. Si quieres, dime uno o dos repos específicos y te paso los comandos de clone ya listos. ¿Trabajas en macOS, Linux o Windows? Te ajusto los pasos a tu sistema.

git remote set-url origin git@github-sergio:dfx5/pe-cajaica-chatbot-backend.git

git remote set-url origin git@github-sahurtado:sahurtado88/learn.git

git remote set-url origin git@github-belcorp:tech-belcorp/saleforce-infra-mlops-iac.git
