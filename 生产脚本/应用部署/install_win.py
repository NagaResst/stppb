#! /bin/python3
# -*- coding:UTF-8 -*-
# {
#   "install_path": "/home",
# 	"modify_bootstrap": "True",
# 	"nacos_addr": "192.168.100.100:8848",
# 	"nacos_namespace": "namespace-test-namespace",
# 	"nacos_user": "ENC(username)",
# 	"nacos_passwd": "ENC(password)",
# 	"jar_actived": "test",
# 	"seata_addr": "192.168.100.100:8091",
# 	"seata_conf_namespace": "namespace-seata-namespace"
# }

import os
import shutil
# import re
import zipfile
import yaml


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
        # self.env = env
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
        install_config = yaml.load(text, yaml.FullLoader)
        install_config['spring']['cloud']['nacos']['config']['server-addr'] = self.nacos_addr
        install_config['spring']['cloud']['nacos']['config']['namespace'] = self.nacos_namespace
        install_config['spring']['cloud']['nacos']['config']['username'] = self.nacos_user
        install_config['spring']['cloud']['nacos']['config']['password'] = self.nacos_passwd
        install_config['spring']['cloud']['nacos']['discovery']['server-addr'] = self.nacos_addr
        install_config['spring']['cloud']['nacos']['discovery']['namespace'] = self.nacos_namespace
        install_config['spring']['cloud']['nacos']['discovery']['username'] = self.nacos_user
        install_config['spring']['cloud']['nacos']['discovery']['password'] = self.nacos_passwd
        install_config['spring']['profiles']['active'] = self.active
        text = yaml.dump(install_config)
        with open(self.boots, 'w', encoding='utf-8') as conn:
            conn.write(text)
            conn.close()
        print("服务%s 的 bootstrap 已经修改完成" % self.service)

    def winsw(self):
        service_exec = self.install_path + '/' + self.service + '.exe'
        shutil.copy('winsw.exe', service_exec)
        ServiceFile = """<service>
  <id>%s</id>
  <name>%s</name>
  <startmode>Automatic</startmode>
  <workingdirectory>%s</workingdirectory>
  <executable>java</executable>
  <arguments>-jar -Dfile.encoding=utf-8 --spring.cloud.bootstrap.location=%s %s</arguments>
  <log mode="none">
  </log>
</service>
        """ % (self.service, self.service, self.install_path, (self.install_path + '/bootstrap.yml'), self.file)
        with open((self.install_path + '/' + self.service + '.xml'), 'w', encoding='utf-8') as windowsService:
            windowsService.write(ServiceFile)
            windowsService.close()
        cupath = os.getcwd()
        os.system('cd %s && %s && cd %s ' % (self.install_path, (service_exec + ' install'), cupath))
        print("服务 " + self.service + " 的Service已经写入")

    def install_service(self):
        self.winsw()
        shutil.rmtree('BOOT-INF')


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
need_deploy_list = load_deploy_list()
if len(need_deploy_list) == 0:
    input("没有找到需要部署的文件，请按回车退出")
    quit()
for file in need_deploy_list:
    file = Service(file)
    file.initialize(config)
    file.distribute_file()
    print("服务 " + file.service + " 已经部署完成。")
print('==================================')
input("所有服务已经部署完毕，请按回车退出")
