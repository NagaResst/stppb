tee /root/script/checkhealth.sh <<- 'EOF'
#! /usr/bin/bash
result=$(curl -s http://localhost:9401/healthmonitoring/checkhealth)
if [[ $result != 'true' ]]
then
  systemctl restart pars-config
  echo "$(date) [warn] service <data> is down , have restart service." >> /root/script/checklog.log
else
  echo "$(date) [info] service <data> is running" >> /root/script/checklog.log
fi
EOF
chmod +x /root/script/checkhealth.sh
echo "*/5 * * * * root bash /root/script/checkhealth.sh" >> /etc/crontab
systemctl restart crond