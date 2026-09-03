Genera una clave SSH para cada cuenta (macOS/Linux; en Windows cambia ~ por %USERPROFILE%):
bash
Copy
# Cuenta 1 (sergiohurtadodfx5)
ssh-keygen -t ed25519 -C "sergio.hurtado@dfx5.com" -f ~/.ssh/id_ed25519_sergio_dfx5

# Cuenta 2 (sahurtado88)
ssh-keygen -t ed25519 -C "sahurtad@gmail.com" -f ~/.ssh/id_ed25519_sahurtado88

# Cuenta 3 (belcrop)
ssh-keygen -t ed25519 -C "extfshurtado@belcorp.biz" -f ~/.ssh/id_ed25519_belcorp

# cuenta4 (bitbucket)
ssh-keygen -t ed25519 -C "sergio.hurtado@dfx5.com" -f ~/.ssh/bitbucket   

# cuenta5 (antamina)
ssh-keygen -t ed25519 -C "sergioh@intelligenix.com" -f ~/.ssh/antamina

# cuenta5 (bhdeks)
ssh-keygen -t rsa -b 4096 -C "sergio.hurtado@dfx5.com" -f ~/.ssh/bhdeks_rsa  

# cuenta5 (grupoefe)
ssh-keygen -t rsa -b 4096 -C "ext_sehurtado@efectiva.com.pe" -f ~/.ssh/grupoefe_rsa  

# Inicia ssh-agent y carga las claves:
## macOS/Linux:

eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_sergio_dfx5
ssh-add ~/.ssh/id_ed25519_sahurtado88
ssh-add ~/.ssh/id_ed25519_belcorp
ssh-add ~/.ssh/bitbucket   
ssh-add ~/.ssh/antamina
ssh-add ~/.ssh/bhdeks_rsa
ssh-add ~/.ssh/grupoefe_rsa

## Windows (PowerShell):

Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
ssh-add $env:USERPROFILE\.ssh\id_ed25519_sergio_dfx5
ssh-add $env:USERPROFILE\.ssh\id_ed25519_sahurtado88
ssh-add $env:USERPROFILE\.ssh\id_ed25519_belcorp
ssh-add $env:USERPROFILE\.ssh\bitbucket

# Copia las claves públicas y añádelas en cada cuenta de GitHub (Settings → SSH and GPG keys → New SSH key), en la cuenta correcta:

cat ~/.ssh/id_ed25519_sergio_dfx5.pub
cat ~/.ssh/id_ed25519_sahurtado88.pub
cat ~/.ssh/id_ed25519_belcorp.pub
cat ~/.ssh/bitbucket.pub
cat ~/.ssh/antamina.pub
cat ~/.ssh/bhdeks_rsa.pub
cat ~/.ssh/grupoefe_rsa.

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
Host github-belcorp
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_belcorp
    IdentitiesOnly yes

# Cuenta 4: bitbucketdfx5
Host bitbucket
    HostName bitbucket.org
    User git
    IdentityFile ~/.ssh/bitbucket
    IdentitiesOnly yes

# Cuenta 5: antamina
Host github-antamina
    HostName github.com
    User git
    IdentityFile ~/.ssh/antamina
    IdentitiesOnly yes

# Cuenta 6: bhdeks
Host ssh.dev.azure.com
  User git
  IdentityFile ~/.ssh/bhdeks_rsa
  IdentitiesOnly yes


# Cuenta 7: grupoefe
Host github-efe
  HostName github.compub
  User git
  IdentityFile ~/.ssh/grupoefe_rsa
  IdentitiesOnly yes


Prueba cada conexión:

ssh -T git@github-sergio
ssh -T git@github-sahurtado
ssh -T git@github-grupoefe
Deberías ver un “Hi ! You’ve successfully authenticated…”.

ssh -T git@ssh.dev.azure.com

## Clona usando el alias del Host correspondiente:

### Repos de la cuenta 1 (sergiohurtadodfx5)
git clone git@github-sergio:sergiohurtadodfx5/REPO_AQUI.git

git clone git@github-sergio:dfx5/PE-Rimac-Eda-Dev.git

git clone git@github-sergio:dfx5/PE-Rimac-EventCatalog.git

git clone git@github-belcorp:tech-belcorp/saleforce-infra-pipeline-app.git

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


wilson.martinez@dfx5.com


# usando gh

🧩 1. Verifica tu configuración actual de gh

Ejecuta:

gh auth status


Esto te mostrará si ya hay alguna sesión activa (por ejemplo, autenticada con una de las cuentas).

Si hay una sesión que no corresponde a la que quieres usar, puedes cerrarla con:

gh auth logout


(o agregar --hostname github.com si quieres especificar).

⚙️ 2. Autenticación separada para cada host SSH

Como tienes dos hosts diferentes definidos en SSH (github-sergio y github-sahurtado), puedes decirle a gh que se autentique con cada uno de ellos usando su propio contexto.

Ejecuta los siguientes comandos (uno por cuenta):

Cuenta 1: sergiohurtadodfx5
GITHUB_HOST=github-sergio gh auth login

Cuenta 2: sahurtado88
GITHUB_HOST=github-sahurtado gh auth login


🔹 Durante el proceso de gh auth login, selecciona:

SSH como método de autenticación.

Cuando te pregunte el host, usa exactamente el alias (github-sergio o github-sahurtado).

Esto creará entradas separadas en ~/.config/gh/hosts.yml para cada identidad.

🧠 3. Uso en repositorios

Cuando clones o trabajes con repositorios, debes usar las URLs con el alias correspondiente:

Ejemplo para la cuenta 1:
git clone git@github-sergio:sergiohurtadodfx5/mi-repo.git

Ejemplo para la cuenta 2:
git clone git@github-sahurtado:sahurtado88/otro-repo.git


Así Git y gh sabrán qué identidad SSH y qué autenticación de GitHub usar.

🧰 4. (Opcional) Comprobación de conexión SSH

Puedes probar que cada identidad funciona correctamente:

ssh -T git@github-sergio
ssh -T git@github-sahurtado


Deberías ver mensajes como:

Hi sergiohurtadodfx5! You've successfully authenticated...
Hi sahurtado88! You've successfully authenticated...

# COpia entre cdodecommits
## Opción A : helper “genérico” + AWS_PROFILE por sesión
Cambia tu .gitconfig para usar el helper sin perfil fijo:
ini
Copy
[credential]
    helper =
    UseHttpPath = true
    helper = !aws codecommit credential-helper $@
En la terminal, alterna de cuenta con AWS_PROFILE:
Para clonar desde la Cuenta A:
bash
Copy
export AWS_PROFILE=accountA
git clone --mirror https://git-codecommit.<region-origen>.amazonaws.com/v1/repos/mi-repo-origen
cd mi-repo-origen.git
Para empujar a la Cuenta B:
bash
Copy
export AWS_PROFILE=accountB
git push --mirror https://git-codecommit.<region-destino>.amazonaws.com/v1/repos/mi-repo-destino
Ventajas: simple y explícito. Evita que un remoto use el perfil equivocado.


# mirror Github

1️⃣ Clona el repositorio original en modo mirror

Esto copia todas las ramas, tags, refs, hooks (todo).

git clone --mirror https://github.com/ORIGEN/REPO.git


Ejemplo:

git clone --mirror https://github.com/empresa-a/proyecto.git


Esto crea una carpeta llamada:

proyecto.git

2️⃣ Entra al repositorio clonado
cd proyecto.git

3️⃣ Crea el repositorio destino en la otra cuenta

En GitHub (cuenta B):

Nuevo repositorio

Vacío

NO README

NO .gitignore

NO license

Ejemplo destino:

https://github.com/usuario-b/proyecto.git

4️⃣ Empuja el mirror al repositorio destino
git push --mirror https://github.com/DESTINO/REPO.git


Ejemplo:

git push --mirror https://github.com/usuario-b/proyecto.git


👉 Esto:

Reemplaza todo el contenido del repo destino

Sincroniza ramas, tags y refs

5️⃣ (Opcional) Automatizar el mirror

Si quieres mantenerlo sincronizado periódicamente:

git remote set-url --push origin https://github.com/usuario-b/proyecto.git
git fetch -p origin
git push --mirror


O con cron / GitHub Actions si lo necesitas.

https://chatgpt.com/c/696032f7-82b4-832e-aaa3-cf419e9d0af8



Server=data01.asid.antamina.com

# Rama local push a rama remota

Tengo una rama en local llamada dev como puedo hacer un push a una rama remota llamada dev-source

Si tu rama local se llama dev y quieres hacer push a una rama remota llamada dev-source, puedes hacerlo directamente indicando el mapeo:

```
git push origin dev:dev-source
```

Qué significa

origin → el remoto

dev → tu rama local

dev-source → la rama que se creará o actualizará en el remoto

Git enviará el contenido de dev hacia origin/dev-source.

- Si quieres que quede configurado para futuros pushes

Para que git push normal funcione después:
```
git push -u origin dev:dev-source
```
Esto crea el tracking entre:

local: dev

remoto: origin/dev-source

Luego podrás usar simplemente:

git push

Verificar

Puedes revisar las ramas remotas con:

git branch -r

o

git ls-remote --heads origin

# TAGuear ram


# si tengo cmabios en mi repo local pero quiero traer los cmabios del repo remoto que debo hacer

Depende de qué quieres hacer con tus cambios locales. Hay tres casos comunes:

1️⃣ Quieres guardar tus cambios locales y luego traer los del remoto

Usa stash.

git stash
git pull
git stash pop

Qué hace:

git stash guarda temporalmente tus cambios.

git pull trae los cambios del remoto.

git stash pop vuelve a aplicar tus cambios.

Puede haber conflictos si tocaste las mismas líneas.

2️⃣ Quieres confirmar tus cambios antes de traer los del remoto

Haz commit y luego pull.

git add .
git commit -m "mis cambios"
git pull

Si hay diferencias, git puede pedirte merge o rebase.

3️⃣ Quieres descartar tus cambios locales y quedarte con lo remoto

⚠️ Esto borra tus cambios.

git reset --hard
git pull

💡 Resumen rápido

Situación	Comando
Guardar cambios sin commit	git stash → git pull → git stash pop
Guardar cambios con commit	git add → git commit → git pull
Eliminar cambios locales	git reset --hard → git pull

El flujo más usado en muchos equipos es git pull --rebase.
Sirve para traer cambios del remoto sin crear commits de merge innecesarios y mantener el historial más limpio.

🔹 Flujo típico con rebase
1️⃣ Haces tus cambios locales
git add .
git commit -m "mis cambios"
2️⃣ Traes los cambios del remoto con rebase
git pull --rebase

Lo que hace Git:

Guarda temporalmente tus commits.

Descarga los commits del remoto.

Vuelve a aplicar tus commits encima de los nuevos.

El historial queda lineal.

🔹 Si tienes cambios sin commit

Primero guárdalos:

git stash
git pull --rebase
git stash pop
🔹 Si hay conflictos durante el rebase

Git se detendrá y debes resolverlos.

Arreglas el archivo.

Luego:

git add archivo_corregido
git rebase --continue

Si quieres cancelar:

git rebase --abort
🔹 Configurar Git para usar rebase siempre en pull

Así no necesitas escribirlo cada vez:

git config --global pull.rebase true

💡 Regla práctica simple

Trabajando solo → git pull

Trabajando en equipo → git pull --rebase


# llevar un tag a a una version

• Entonces no hagas reset --hard. Si quieres que develop termine con el contenido de theta pero sin perder la historia, haz un merge que
  conserve el árbol de theta.

  La forma más segura es esta:

  git switch -c recover-sigma sigma
  git merge -s ours develop -m "merge: preserve develop history, keep theta content"
  git switch develop
  git merge recover-sigma


