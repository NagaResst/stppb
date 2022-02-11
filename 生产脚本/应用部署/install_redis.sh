#! /bin/bash
cd /tmp
#curl -O 下载源码包
tar -zxvf redis-5.0.14.tar.gz
cd redis-5.0.14
make install PREFIX=/home/redis
cp redis.conf /home/redis/
cp sentinel.conf /home/redis/
sed -i 's/bind 127.0.0.1/bind 0.0.0.0/g' /home/redis/redis.conf
sed -i 's/protected-mode yes/protected-mode no/g' /home/redis/redis.conf
sed -i 's/daemonize no/daemonize yes/g' /home/redis/redis.conf
# 预设密码，将你需要设置的密码加入下方的语句中
sed -i 's/# requirepass foobared/requirepass /g' /home/redis/redis.conf
cat << EOF > /usr/lib/systemd/system/redis.service

[Unit]
Description=redis-server
After=network.target

[Service]
Type=forking
ExecStart=/home/redis/bin/redis-server /home/redis/redis.conf
PrivateTmp=true

[Install]
WantedBy=multi-user.target

EOF
cat << EOF > /usr/lib/systemd/system/redis-sentinel.service

[Unit]
Description=redis-sentinel
After=network.target

[Service]
Type=forking
ExecStart=/home/redis/bin/redis-server /home/redis/sentinel.conf
PrivateTmp=true

[Install]
WantedBy=multi-user.target

EOF
systemctl daemon-reload
systemctl enable --now redis
systemctl status redis

