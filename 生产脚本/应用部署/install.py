#! /bin/python3
# {
#   "install_path": "/home",
# 	"env": ["java", "nacos", "redis", "nginx"],
# 	"service": ["bbway-cloud-gateway", "user-center-service", "bbway-cloud-cas"],
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
        self.boots = 'BOOT-INF/classes/bootstrap.yml'
        self.nacos_addr = None
        self.nacos_user = None
        self.nacos_passwd = None
        self.nacos_namespace = None
        print("已经识别到文件 " + self.file)

    def distribute_file(self):
        cdir = self.file.split('.')
        self.service = cdir[0]
        os.mkdir(self.path + '/' + self.service)
        self.install_path = self.path + '/' + self.service
        self.path = self.install_path + '/' + self.file
        shutil.copy(self.file, self.path)
        # shutil.move(self.file, self.service)
        print("服务 " + self.service + "文件已经分发。")

    def modify_bootstrap(self):
        with zipfile.ZipFile(self.file, 'a') as zf:
            zf.extract(self.boots, '.')
            with open(self.boots, 'r+') as conn:
                text = conn.read()
                newtext = re.sub(r'server-addr: (.*)', ('server-addr: ' + self.nacos_addr), text)
                newtext = re.sub(r'namespace: (.*)', ('namespace: ' + self.nacos_namespace), newtext)
                newtext = re.sub(r'username: (.*)', ('username: ' + self.nacos_user), newtext)
                newtext = re.sub(r'password: ENC(.*)', ('password: ENC(%s)' % self.nacos_passwd), newtext)
                conn.seek(0, 0)
                conn.write(newtext)
                conn.close()
            zf.write(self.boots)
            zf.close()

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
        with open(unitsPath, 'w') as unit:
            unit.write(unitFile)
            unit.close()

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
        with open((self.install_path + '/' + self.service + '-service.xml'), 'w') as windowsService:
            windowsService.write(ServiceFile)
            windowsService.close()
        cupath = os.getcwd()
        os.system('cd %s && %s && cd %s ' % (self.install_path, (self.service + '-service.exe install'), cupath))

    def install_service(self, tos):
        if tos == 'Linux':
            self.systemd_units()
            print("服务 " + self.service + " 已经写入")
        elif tos == 'Windows':
            self.winsw()
            print("")


def get_system_type():
    if os.name == 'posix':
        javapath0 = str(os.popen('whereis java').readlines())
        javapath = re.findall(r": (.*)\\", javapath0)
        return 'Linux', javapath[0]
    elif os.name == 'nt':
        return 'Windows', None


with open(r'install_config.json', 'r', encoding="utf-8") as config_file:
    config = eval(config_file.read())
    print("安装配置已经读取")
    config_file.close()
ostype, env = get_system_type()
if ostype == 'Linux':
    os.system('rpm -ivh *zip*.rpm')
need_install_files = os.listdir()
print("识别到文件" + str(len(need_install_files)) + " 个。")
for file in need_install_files:
    file = Service(file)
    file.path = config['install_path']
    if config['modify_bootstrap'] == "True":
        file.nacos_addr = config['nacos_addr']
        file.nacos_user = config['nacos_user']
        file.nacos_passwd = config['nacos_passwd']
        file.nacos_namespace = config['nacos_namespace']
        file.modify_bootstrap()
    file.env = env
    file.distribute_file()
    file.install_service(ostype)
    if ostype == 'Linux':
        os.system('systemctl daemon-reload')
        os.system('systemctl enable --now ' + file.service)
        print("服务 " + file.service + " 已经部署完成。")
print("所有服务已经部署完毕，请按任意键退出")
