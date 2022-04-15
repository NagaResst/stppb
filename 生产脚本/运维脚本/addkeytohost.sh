#! /bin/bash
set -e
ips=(ip ip2)
user="root"
passwd=""

#检查是否拥有sshpass可以用来自动推送公钥  如果没有sshpass需要手动输入密码
if ! type sshpass >/dev/null 2>&1
then
  havepw="n"
  read -r -p "本机没有sshpass 是否安装（y/n）  " installsshpass
  if [ ${installsshpass} == "y" ]
  then
    # 安装sshpass需要依赖yum  如果yum无法使用请手动安装sshpass
    yum install sshpass -y && havepw="y"
  fi
else
  havepw="y"
fi

#检查本机是否有密钥，如果没有就创建一个
if [ -f ~/.ssh/id_rsa ]
then
  :
else
  ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa -b 2048 > /dev/null
  echo "已经为本机创建密钥"
fi

#推送密钥 如果没有sshpass并且passwd变量为空值则需要手动输入密码
if [[ ${havepw} == "n" ]] && [[ ${passwd} == "" ]]
then
  for ip in ${ips[*]}
  do
    echo "请输入${ip}的密码"
    ssh-copy-id  -o StrictHostKeyChecking=no ${user}@${ip} && echo "已经将密钥成功推送到对端设备"
  done
#有sshpass 并且已经预设了passwd变量则使用变量推送公钥
elif [[ ${havepw} == "y" ]] && [[ ${passwd} != "" ]]
then
    for ip in ${ips[*]}
  do
    sshpass -p ${passwd} ssh-copy-id  -o StrictHostKeyChecking=no ${user}@${ip} && echo "已经将密钥成功推送到${ip}"
  done
else
  :
fi
