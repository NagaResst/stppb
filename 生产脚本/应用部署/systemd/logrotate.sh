tee /etc/logrotate.d/service.conf <<- 'EOF'
/path/*.log {
copytruncate
compress
delaycompress
create 0550 owner group
missingok
notifempty
daily
rotate 30
dateext
dateyesterday
dateformat .%Y.%m.%d
}
EOF