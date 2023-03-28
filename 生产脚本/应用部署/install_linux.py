#! /bin/python3
# -*- coding:UTF-8 -*-


import os
import re
import shutil


class Service(object):
    def __init__(self, filename, path='/opt'):
        self.file = filename
        self.service = filename.split('.')[0]
        self.install_path = path + '/service'
        self.path = None
        self.env = None
        print("已经识别到文件 " + self.file)

    def distribute_file(self):
        # 创建部署路径
        try:
            os.makedirs(self.install_path)
        except:
            print("服务部署路径已经存在")
        # 初始化文件部署路径
        self.path = self.install_path + '/' + self.file
        try:
            shutil.copy(self.file, self.path)
        except:
            print("服务文件已经存在，覆盖安装")
            os.remove(self.path)
            shutil.copy(self.file, self.path)
        print("服务 " + self.service + "文件已经分发。")

    def systemd_units(self):
        unitFile = """[Unit]
Description=%s
After=network.target

[Service]
EnvironmentFile=-%s/cloud.conf
ExecStart=%s -jar %s 
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=%s
Type=simple
Restart=on-failure
RestartSec=30s

[Install]
WantedBy=multi-user.target
""" % (self.service, self.install_path, self.env, self.file, self.service)
        unitsPath = '/var/lib/systemd/system/' + self.service + '.service'
        with open(unitsPath, 'w', encoding='utf-8') as unit:
            unit.write(unitFile)
            unit.close()
            print("服务 " + self.service + " 的unit已经写入")

    def install_service(self):
        self.systemd_units()


def get_system_type():
    javapath0 = str(os.popen('whereis java').readlines())
    javapath = re.findall(r": (.*)\\", javapath0)[0].split(' ')
    if len(javapath) == 0:
        input('本机没有安装java环境，按回车退出')
        quit()
    else:
        return javapath[0]


def load_deploy_list():
    need_install_files = os.listdir(os.getcwd())
    deploy_list = []
    for deploy_file in need_install_files:
        filesname = deploy_file.split('.')
        if filesname[-1] == 'jar':
            deploy_list.append(deploy_file)
    print("识别到文件" + str(len(deploy_list)) + " 个。")
    return deploy_list


# program start

install_path = '/opt'

os.system('setenforce 0')
os.system("sed -i \"s/SELINUX=enforcing/SELINUX=disabled/g\" /etc/selinux/config")

env = get_system_type()

need_deploy_list = load_deploy_list()

if len(need_deploy_list) == 0:
    input("没有找到需要部署的文件，请按回车退出")
    quit()

services = []
services_name = ''

for file in need_deploy_list:
    file = Service(file, install_path)
    file.env = env
    file.distribute_file()
    file.install_service()
    services.append(file.service)

for s in services:
    services_name = services_name + ' ' + s

with open((install_path + '/service/cloud.conf'), 'w', encoding='UTF-8') as service_config_file:
    config = """spring_cloud_nacos_config_serveraddr=
spring_cloud_nacos_config_namespace=
#spring_cloud_nacos_config_username=
spring_cloud_nacos_config_password=
spring_cloud_nacos_discovery_serveraddr=
spring_cloud_nacos_discovery_namespace=
#spring_cloud_nacos_discovery_username=
spring_cloud_nacos_discovery_password=
spring_profiles_active=
"""
    service_config_file.write(config)
    service_config_file.close()

with open('/etc/logrotate.d/bbway.conf', 'w', encoding='UTF-8') as logrotate_config_file:
    config = install_path + "/logs" + r"""/*.log {
copytruncate
compress
delaycompress
missingok
notifempty
daily
rotate 30
dateext
dateyesterday
dateformat .%Y.%m.%d
}"""
    logrotate_config_file.write(config)
    logrotate_config_file.close()

with open('/etc/rsyslog.d/bbway.conf', 'w', encoding='UTF-8') as rsyslog_config_file:
    config = r"""template(name="bbway-log" type="string"
        string="%HOSTNAME% %msg%\n")
"""
    for s in services:
        config = config + """if ($programname == '%s') then {
    action(type="omfile" file="%s/logs/%s.log" template="bbway-log")
    stop
}""" % (s, install_path, s)
        if s != services[-1]:
            config = config + ' else '
    rsyslog_config_file.write(config)
    rsyslog_config_file.close()

os.system('systemctl restart rsyslog')

os.system('systemctl daemon-reload')
os.system('systemctl enable --now ' + services_name)

print('==================================')
print("所有服务已经部署完毕。")
exit(code=0)
