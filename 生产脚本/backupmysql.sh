#!/bin/bash
datenow=`date +%Y-%m-%d`
mysqlpd='password'
dip='ip address'
dport='port'
spath='/path/'
backupdb=(databases1 [databases2])

mkdir -p $spath/$datenow
for db in ${backupdb[*]}
do
  mysqldump -uroot -h$dip -p$mysqlpd --max_allowed_packet=512M $db | gzip > $db.sql.gz
done
