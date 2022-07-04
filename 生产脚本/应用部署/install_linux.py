#! /bin/python3
# -*- coding:UTF-8 -*-
# {
#   "install_path": r"/home",
#   "modify_bootstrap": "True",
#   "nacos_addr": "192.168.100.100:8848",
#   "nacos_namespace": "namespace-test-namespace",
#   "nacos_user": "ENC(username)",
#   "nacos_passwd": "ENC(password)",
#   "jar_actived": "test",
#   "seata_addr": "192.168.100.100:8091",
#   "seata_conf_namespace": "namespace-seata-namespace"
# }

import os
import re
import shutil
import zipfile


class Service(object):
    def __init__(self, filename, path='/home'):
        self.file = filename
        self.service = None
        self.install_path = path
        self.path = path
        self.env = None
        self.boots = 'BOOT-INF/classes/bootstrap.yml'
        self.nacos_addr = None
        self.nacos_user = None
        self.nacos_passwd = None
        self.nacos_namespace = None
        self.active = None
        self.ost = None
        print('========== Start deploy ==========')
        print("已经识别到文件 " + self.file)

    def initialize(self, install_config):
        self.path = install_config['install_path']
        cdir = self.file.split('.')
        self.service = cdir[0]
        self.env = env
        if config['modify_bootstrap'] == "True":
            self.nacos_addr = install_config['nacos_addr']
            self.nacos_user = install_config['nacos_user']
            self.nacos_passwd = install_config['nacos_passwd']
            self.nacos_namespace = install_config['nacos_namespace']
            self.active = install_config['jar_actived']
            self.modify_bootstrap()

    def distribute_file(self):
        try:
            os.makedirs((self.path + '/' + self.service))
        except IOError:
            print("服务部署路径已经存在")
        self.install_path = self.path + '/' + self.service
        self.path = self.install_path + '/' + self.file
        try:
            shutil.copy(self.file, self.path)
        except IOError:
            print("服务文件已经存在，重新部署")
            os.remove(self.path)
            shutil.copy(self.file, self.path)
        try:
            shutil.copy(self.boots, self.install_path)
        except IOError:
            print("服务文件已经存在，重新部署")
            os.remove(self.boots)
            shutil.copy(self.boots, self.install_path)
        print("服务 " + self.service + "文件已经分发。")

    def modify_bootstrap(self):
        with zipfile.ZipFile(self.file, 'r') as zf:
            zf.extract(self.boots)
            zf.close()
        with open(self.boots, 'r+', encoding='utf-8') as conn:
            text = conn.read()
            conn.close()
        text = re.sub(r'server-addr: (.*)', ('server-addr: ' + self.nacos_addr), text)
        text = re.sub(r'namespace: (.*)', ('namespace: ' + self.nacos_namespace), text)
        text = re.sub(r'username: (.*)', ('username: ' + self.nacos_user), text)
        text = re.sub(r'password: ENC(.*)', ('password: %s' % self.nacos_passwd), text)
        text = re.sub(r'active: (.*)', ('active: %s' % self.active), text)
        with open(self.boots, 'w', encoding='utf-8') as conn:
            conn.write(text)
            conn.close()
        print("服务%s 的 bootstrap 已经修改完成" % self.service)

    def systemd_units(self):
        unitFile = """[Unit]
Description=%s
After=network.target

[Service]
ExecStart=%s -jar %s --spring.cloud.bootstrap.location=%s
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=%s
Type=simple
Restart=on-failure
RestartSec=30s

[Install]
WantedBy=multi-user.target
""" % (self.service, self.env, self.file, (self.install_path + '/bootstrap.yml'), self.service)
        unitsPath = '/var/lib/systemd/system/' + self.service + '.service'
        with open(unitsPath, 'w', encoding='utf-8') as unit:
            unit.write(unitFile)
            unit.close()
            print("服务 " + self.service + " 的unit已经写入")

    def install_service(self):
        self.systemd_units()
        shutil.rmtree('BOOT-INF')


def get_system_type():

    javapath0 = str(os.popen('whereis java').readlines())
    javapath = re.findall(r": (.*)\\", javapath0)
    if len(javapath) == 0:
        input('本机没有安装java环境，按回车退出')
        quit()
    return 'Linux', javapath[0]


def load_config(load_file='install_config.json'):
    with open(load_file, 'r') as config_file:
        deploy_config = eval(config_file.read())
        print("安装配置已经读取")
        config_file.close()
    return deploy_config


def load_deploy_list():
    need_install_files = os.listdir(os.getcwd())
    deploy_list = []
    for deploy_file in need_install_files:
        filesname = deploy_file.split('.')
        if filesname[-1] == 'jar':
            deploy_list.append(deploy_file)
    print("识别到文件" + str(len(deploy_list)) + " 个。")
    return deploy_list


config = load_config('install_config.json')
ostype, env = get_system_type()
need_deploy_list = load_deploy_list()
if len(need_deploy_list) == 0:
    input("没有找到需要部署的文件，请按回车退出")
    quit()
for file in need_deploy_list:
    file = Service(file)
    file.initialize(config)
    file.ost = ostype
    file.distribute_file()
    file.install_service()
    if ostype == 'Linux':
        os.system('systemctl daemon-reload')
        os.system('systemctl enable --now ' + file.service)
        print("服务 " + file.service + " 已经部署完成。")
print('==================================')
input("所有服务已经部署完毕，请按回车退出")
