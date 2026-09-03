# go install sigs.k8s.io/kind@v0.31.0
go: downloading sigs.k8s.io/kind v0.31.0
go: downloading github.com/spf13/cobra v1.8.0
go: downloading al.essio.dev/pkg/shellescape v1.5.1
go: downloading github.com/pkg/errors v0.9.1
go: downloading github.com/spf13/pflag v1.0.5
go: downloading github.com/mattn/go-isatty v0.0.20
go: downloading github.com/pelletier/go-toml v1.9.5
go: downloading github.com/BurntSushi/toml v1.4.0
go: downloading github.com/evanphx/json-patch/v5 v5.6.0
go: downloading go.yaml.in/yaml/v3 v3.0.4
go: downloading sigs.k8s.io/yaml v1.4.0
go: downloading golang.org/x/sys v0.6.0

# export PATH="$(go env GOPATH)/bin:$PATH"
kind version

# ahcerlo permantnet 

echo 'export PATH="$(go env GOPATH)/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Levantar kind

 kind create cluster --name rbac --image kindest/node:v1.34.0