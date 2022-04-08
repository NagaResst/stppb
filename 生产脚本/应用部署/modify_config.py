#! /bin/python3
# -*- coding:UTF-8 -*-

import os
import zipfile
import yaml


class Service(object):
    def __init__(self, filename):
        self.file = filename
        self.service = None
        self.boots = 'BOOT-INF/classes/bootstrap.yml'
        self.nacos_addr = 'ip'
        self.nacos_user = 'ENC(username)'
        self.nacos_passwd = 'ENC(password)'
        self.nacos_namespace = 'namespace-nacos-namespace'
        self.active = 'prod'
        print('========== Start modify ==========')
        print("已经识别到文件 " + self.file)

    def modify_bootstrap(self):
        cdir = self.file.split('.')
        self.service = cdir[0]
        with zipfile.ZipFile(self.file, 'r') as zf:
            zf.extract(self.boots)
            zf.close()
        print(self.file + "解包完成")
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


def load_deploy_list():
    need_install_files = os.listdir(os.getcwd())
    deploy_list = []
    for deploy_file in need_install_files:
        filesname = deploy_file.split('.')
        if filesname[-1] == 'jar':
            deploy_list.append(deploy_file)
    print("识别到文件" + str(len(deploy_list)) + " 个。")
    return deploy_list


need_deploy_list = load_deploy_list()
if len(need_deploy_list) == 0:
    input("没有找到需要修改的文件，请按回车退出")
    quit()
for file in need_deploy_list:
    file = Service(file)
    file.modify_bootstrap()
    print("服务 " + file.service + " 已经修改完成。")
print('==================================')
input("所有服务已经部署完毕，请按回车退出")
