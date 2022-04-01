#! /bin/python3
# -*- coding:UTF-8 -*-
# {
#   "install_path": "/home",
# 	"modify_bootstrap": "True",
# 	"nacos_addr": "192.168.100.100:8848",
# 	"nacos_namespace": "namespace-test-namespace",
# 	"nacos_user": "username",
# 	"nacos_passwd": "password",
# 	"jar_actived": "test",
# 	"seata_addr": "192.168.100.100:8091",
# 	"seata_conf_namespace": "namespace-seata-namespace"
# }

import os
import shutil
import re
import zipfile


class Service(object):
    def __init__(self, filename, path='/home'):
        self.file = filename
        self.service = None
        self.install_path = path
        self.path = path
        self.env = None
        self.boots = 'temp/BOOT-INF/classes/bootstrap.yml'
        self.nacos_addr = None
        self.nacos_user = None
        self.nacos_passwd = None
        self.nacos_namespace = None
        self.active = None
        print('========== Start deploy ==========')
        print("已经识别到文件 " + self.file)

    def distribute_file(self):
        cdir = self.file.split('.')
        self.service = cdir[0]
        try:
            os.makedirs((self.path + '/' + self.service))
        except:
            print("服务部署路径已经存在")
        self.install_path = self.path + '/' + self.service
        self.path = self.install_path + '/' + self.file
        try:
            shutil.copy(self.file, self.path)
        except:
            print("服务文件已经存在，重新部署")
            os.remove(self.path)
            shutil.copy(self.file, self.path)
        print("服务 " + self.service + "文件已经分发。")

    def modify_bootstrap(self):
        with zipfile.ZipFile(self.file, 'r') as zf:
            zf.extractall('temp')
            zf.close()
        with open(self.boots, 'r+') as conn:
            text = conn.read()
            newtext = re.sub(r'server-addr: (.*)', ('server-addr: ' + self.nacos_addr), text)
            newtext = re.sub(r'namespace: (.*)', ('namespace: ' + self.nacos_namespace), newtext)
            newtext = re.sub(r'username: (.*)', ('username: ENC(%s)' + self.nacos_user), newtext)
            newtext = re.sub(r'password: ENC(.*)', ('password: ENC(%s)' % self.nacos_passwd), newtext)
            newtext = re.sub(r'active: (.*)', ('active: (%s)' % self.active), newtext)
            conn.seek(0, 0)
            conn.write(newtext)
            conn.close()
        with zipfile.ZipFile('newfile.jar', 'w', zipfile.ZIP_DEFLATED) as newzf:
            tpath = os.getcwd() + '/temp/'
            for dir_path, dir_name, file_names in os.walk(tpath):
                file_path = dir_path.replace(tpath, '')
                file_path = file_path and file_path + os.sep or ''
                for file_name in file_names:
                    newzf.write(os.path.join(dir_path, file_name), file_path + file_name)
            newzf.close()
        shutil.rmtree('temp')
        os.remove(self.file)
        os.rename('newfile.jar', self.file)
        print("服务%s 的 bootstrap 已经修改完成" % self.service)

    def systemd_units(self):
        unitFile = """[Unit]
Description=%s
After=network.target

[Service]
ExecStart=%s -jar %s 
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=%s
Type=simple
Restart=on-failure
RestartSec=30s

[Install]
WantedBy=multi-user.target""" % (self.service, self.env, self.path, self.service)
        unitsPath = '/var/lib/systemd/system/' + self.service + '.service'
        with open(unitsPath, 'w', encoding='utf-8') as unit:
            unit.write(unitFile)
            unit.close()
            print("服务 " + self.service + " 的unit已经写入")

    def winsw(self):
        service_exec = self.install_path + '/' + self.service + '-service.exe'
        shutil.copy('winsw.exe', service_exec)
        ServiceFile = """<service>
  <id>%s</id>
  <name>%s</name>
  <startmode>Automatic</startmode>
  <workingdirectory>%s</workingdirectory>
  <executable>java</executable>
  <arguments>-jar -Dfile.encoding=utf-8 %s</arguments>
  <log mode="none">
  </log>
</service>
        """ % (self.service, self.service, self.install_path, self.file)
        with open((self.install_path + '/' + self.service + '.xml'), 'w', encoding='utf-8') as windowsService:
            windowsService.write(ServiceFile)
            windowsService.close()
        cupath = os.getcwd()
        os.system('cd %s && %s && cd %s ' % (self.install_path, (self.service + '.exe install'), cupath))
        print("服务 " + self.service + " 的Service已经写入")

    def install_service(self, tos):
        if tos == 'Linux':
            self.systemd_units()
        elif tos == 'Windows':
            self.winsw()
            print("")


def get_system_type():
    if os.name == 'posix':
        javapath0 = str(os.popen('whereis java').readlines())
        javapath = re.findall(r": (.*)\\", javapath0)
        if len(javapath) == 0:
            input('本机没有安装java环境，按回车退出')
            quit()
        return 'Linux', javapath[0]
    elif os.name == 'nt':
        return 'Windows', None


with open(r'install_config.json', 'r') as config_file:
    config = eval(config_file.read())
    print("安装配置已经读取")
    config_file.close()
ostype, env = get_system_type()
need_install_files = os.listdir(os.getcwd())
print("识别到文件" + str(len(need_install_files)) + " 个。")
for file in need_install_files:
    if (file.split('.'))[-1] == 'jar':
        file = Service(file)
        file.path = config['install_path']
        if config['modify_bootstrap'] == "True":
            file.nacos_addr = config['nacos_addr']
            file.nacos_user = config['nacos_user']
            file.nacos_passwd = config['nacos_passwd']
            file.nacos_namespace = config['nacos_namespace']
            file.active = config['jar_actived']
            file.modify_bootstrap()
        file.env = env
        file.distribute_file()
        file.install_service(ostype)
        if ostype == 'Linux':
            os.system('systemctl daemon-reload')
            os.system('systemctl enable --now ' + file.service)
            print("服务 " + file.service + " 已经部署完成。")
print('==================================')
input("所有服务已经部署完毕，请按回车退出")
