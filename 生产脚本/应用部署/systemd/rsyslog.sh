tee /etc/rsyslog.d/service.conf <<- 'EOF'
template(name="service-log" type="string"
         string="%HOSTNAME% %msg%\n")
if ($programname == 'apiserver') then {
   action(type="omfile" file="/home/logs/apiserver.log" template="service-log")
   stop                   
} else if ($programname == 'scheduler') then {
   action(type="omfile" file="/home/logs/scheduler.log" template="service-log")
   stop
} else if ($programname == 'manager') then {
   action(type="omfile" file="/home/logs/manager.log" template="service-log")
   stop
} else if ($programname == 'etcd') then {
   action(type="omfile" file="/home/logs/etcd.log" template="service-log")
   stop
}
EOF


setenforce 0
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config

systemctl restart rsyslog