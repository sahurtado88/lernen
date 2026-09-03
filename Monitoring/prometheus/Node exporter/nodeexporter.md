# Node exporter en EC2

wget https://github.com/prometheus/node_exporter/releases/download/v1.10.2/node_exporter-1.10.2.linux-amd64.tar.gz
tar xvfz node_exporter-1.10.2.linux-amd64.tar.gz
cd node_exporter-1.10.2.linux-amd64
./node_exporter

# Configuring your Prometheus instances
Your locally running Prometheus instance needs to be properly configured in order to access Node Exporter metrics. The following prometheus.yml example configuration file will tell the Prometheus instance to scrape, and how frequently, from the Node Exporter via localhost:9100:


global:
  scrape_interval: 15s

scrape_configs:
- job_name: node
  static_configs:
  - targets: ['localhost:9100']

# Node exporter as a service

## crear grupo

sudo groupadd --system prometheus

## crear user

sudo useradd -s /sbin/nologin --system -g prometheus prometheus

## crear carpeta

sudo mkdir /var/lib/node/

sudo mv node_exporter /var/lib/node/

## crear servicio

copiar este archivo en la ruta /etc/systemd/system/node.service

[Unit]
Description=Prometheus Node Exporter
Documentation=https://prometheus.io/docs/introduction/overview/
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=prometheus
Group=prometheus
ExecReload=/bin/kill -HUP $MAINPID
ExecStart=/var/lib/node/node_exporter

SyslogIdentifier=prometheus_node_exporter
Restart=always

[Install]
WantedBy=multi-user.target

## asociar usuario con ruta y permisos

sudo chown -R prometheus:prometheus /var/lib/node

sudo chown -R prometheus:prometheus /var/lib/node/*

sudo chmod -R 775 prometheus:prometheus /var/lib/node

sudo chmod -R 775 prometheus:prometheus /var/lib/node/*


## iniciar servicio

sudo systemctl daemon-reload

sudo systemctl start node

sudo systemctl enable node

sudo systemctl status node