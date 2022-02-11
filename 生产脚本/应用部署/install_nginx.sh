#! /bin/bash
cd /tmp
yum install gcc pcre-devel zlib-devel openssl openssl-devel -y
# curl -O 下载1.20.2版本的源码包
tar -zxvf nginx-1.20.2.tar.gz
cd nginx-1.20.2
./configure  --prefix=/home/nginx  --with-compat --with-file-aio --with-threads --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-stream --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module
make && make install
cat << EOF > /usr/lib/systemd/system/nginx.service
[Unit]
Description=Nginx
After=network.target

[Service]
Type=forking
ExecStart=/home/nginx/sbin/nginx
ExecReload=/home/nginx/sbin/nginx -s reload
ExecStop=/home/nginx/sbin/nginx -s quit
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now nginx
ln -s /home/nginx/sbin/nginx /usr/bin/nginx
systemctl status nginx