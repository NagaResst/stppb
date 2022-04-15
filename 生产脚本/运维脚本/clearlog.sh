tee /etc/cron.daily/clearlog.sh <<-'EOF'
#! /bin/bash
path=()
for i in ${path[*]}
do
  find $i -type f -name "*.log" -mtime +30 -exec rm -rf {} \;
done
EOF
chmod +x /etc/cron.daily/clearlog.sh
systemctl restart crond
