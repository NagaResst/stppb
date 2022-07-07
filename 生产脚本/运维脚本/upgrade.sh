#!/bin/bash
set -e
date_now=$(date +%Y-%m-%d)
backend_app_path='/usr/local/webserver/apache-tomcat-*'
frontend_app_path='/usr/local/webserver'
frontend_ips=(ip1 ip2)
backend_ips=(ip1 ip2)
backup_path="/usr/local/webserver/backup"


function check() {
  result=$(curl -s $1:8080)
  expect='{"success":false,"errorCode":"E10207","errorMessage":"用户登陆PRIVATETOKEN无效"}'
  if [ "$result" == "$expect" ]
  then
    echo "$1的项目应用运行成功"
  else
    echo "请检查$1的日志"
  fi
}


read -r -p "本次发版是否启用验证过程，输入w等待，输入n不等待" wait_or_no
# 取消下行注释可以设定是否总是启用验证
# wait_or_no='n'
for ip in ${backend_ips[*]}
do
  echo "进行${ip}的后端发版的准备工作"
  ssh root@$ip "sh $backend_app_path/bin/shutdown.sh"
  echo "已经停止项目的运行,正在进行发版的准备。"
  ssh root@$ip "mkdir -p $backup_path/$date_now/ ; mv $backend_app_path/webapps/ROOT.war $backup_path/$date_now/$(date +%Y-%m-%d_%R).war ; rm -rf $backend_app_path/webapps/* "
  echo "开始发版"
  scp ~/ROOT.war root@$ip:$backend_app_path/webapps/
  echo "项目发版完成，正在启动应用"
  ssh root@$ip "sh $backend_app_path/bin/startup.sh"

  if [ $wait_or_no == "w" ] || [ $wait_or_no == "W" ]|| [ $wait_or_no == "y" ]|| [ $wait_or_no == "Y" ]
  then
    check $ip
  else
    :
  fi
done

for ip in ${frontend_ips[*]}
do
  echo "开始备份旧版前端文件"
  ssh $ip "mkdir -p $backup_path/$date_now/ ; mv $frontend_app_path/*iwms-frontend-deploy $backup_path/$date_now/"
  echo "开始进行新版本的${ip}前端发版"
  scp ~/$(ll | grep iwms-client-production | awk '{print $9}') $ip:frontend_app_path/
  ssh $ip "cd $frontend_app_path && tar -zxvf *iwms-client-production*.tar"
  ssh $ip "rm -f *iwms-client-production*.tar"
  echo "前端${ip}发版完成"
done

echo "发版工作完成！"
