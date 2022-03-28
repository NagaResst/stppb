#! /bin/python3
import os
import shutil


class Service(object):
    def __init__(self, filename, service_name=None, filepath=None, envpath=None):
        self.file = filename
        self.service = service_name
        self.path = filepath
        self.env = envpath
        print("已经识别到文件 " + self.file)

    def get_system_type(self):
        if os.name == 'posix':
            env_dist = os.environ
            self.env = env_dist['JAVA_HOME'] + '/bin/java'
            return 'Linux'
        elif os.name == 'nt':
            return 'Windows'

    def distribute_file(self):
        cdir = self.file.split('.')
        self.service = cdir[0]
        os.mkdir(self.service)
        shutil.move(self.file, self.service)
        self.path = os.getcwd() + self.service + self.file
        print("服务 " + self.service + "文件已经分发。")

    def systemd_units(self):
        unitFile = """
        [Unit]
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
        WantedBy=multi-user.target
        """ % (self.service, self.env, self.path, self.service)
        unitPath = '/var/lib/systemd/system/' + self.service + '.service'
        with open(unitPath, 'w') as unit:
            unit.write(unitFile)
            unit.close()

    def winsw(self):
        None

    def install_service(self):
        osType, java = self.get_system_type()
        if osType == 'Linux':
            self.systemd_units()
            print("服务 " + self.service + "已经注册")
            return osType
        elif osType == 'Windows':
            self.winsw()
            print("")
            return osType


files = os.listdir()
print("识别到文件" + str(len(files)) + " 个。")
for file in files:
    file = Service(file)
    file.distribute_file()
    osT = file.install_service()
    if osT == 'Linux':
        os.system('systemctl daemon-reload')
        os.system('systemctl enable --now ' + file.service)
        print("服务 " + file.service + " 已经部署完成。")
print("所有服务已经部署完毕，请按任意键退出")
