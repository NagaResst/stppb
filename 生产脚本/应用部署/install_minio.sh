#! /bin/bash
groupadd minio
useradd minio -g minio -s /bin/nologin

cd /home/minio && wget https://dl.min.io/server/minio/release/linux-amd64/minio && chmod +x minio
mkdir -p /home/minio/data

cat << EOF > /usr/lib/systemd/system/minio.service
[Unit]
Description= MinIO Server : A Network File Server
After=network.target

[Service]
User=minio
Group=minio
EnvironmentFile=-/home/minio/minio.conf
Environment=MINIO_ROOT_USER=$MINIO_ROOT_USER
Environment=MINIO_ROOT_PASSWORD=$MINIO_ROOT_PASSWORD
ExecStartPre=/bin/bash -c "[ -n \"${MINIO_VOLUMES}\" ] || echo \"Variable MINIO_VOLUMES not set in /etc/default/minio\""
ExecStart=/home/minio/minio server $MINIO_OPTS --address ":${MINIO_PORT}" --console-address ":${MINIO_CONSOLE_PORT}"  $MINIO_VOLUMES
Type=simple
Restart=on-failure
RestartSec=30s

[Install]
WantedBy=multi-user.target
EOF

cat << EOF > /home/minio/minio.conf
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_VOLUMES="/home/minio/data"
MINIO_OPTS=""
MINIO_CONSOLE_PORT=9001
MINIO_PORT=9000
EOF


systemctl daemon-reload
systemctl enable --now minio