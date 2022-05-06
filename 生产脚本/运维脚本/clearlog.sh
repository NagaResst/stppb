tee /etc/cron.daily/clearlog.sh <<-'EOF'
#! /bin/bash
find /usr/local/webserver/tomcat-9.0.54/logs -type f -name "*.log" -mtime +180 -exec rm -f {} \;
find /usr/local/webserver/provisioning/logs/server1 -type f -name "*.log" -mtime +180 -exec rm -f {} \;
EOF
chmod +x /etc/cron.daily/clearlog.sh
systemctl restart crond
