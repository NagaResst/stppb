tee /etc/cron.daily/clearlog.sh <<-'EOF'
#! /bin/bash
path=
find $path -type f -name "*.log" -mtime +30 exec rm -rf {} \;
EOF
chmod +x /etc/cron.daily/clearlog.sh
systemctl restart crond