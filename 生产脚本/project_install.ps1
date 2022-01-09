#! /bin/pwsh
# powershell语言的可读性很高，就不写注释了
##########  安装JAVA   ##############

.\jre-8u311-windows-x64.exe /s


##########  安装并启动mysql   ##############
Expand-Archive -Path "./mysql-5.7.35-winx64.zip" -DestinationPath ./..
Set-Location ..
Rename-Item -Path "mysql-5.7.35-winx64" -NewName "mysql"
Set-Location mysql
$mysqlini = @"

"@
$mysqlini | Out-File "my.ini" -Encoding utf8
Set-Location bin
$passwd = mysqld --initialize-insecure --user=mysql
$passwd
$passwd -match 'root@localhost: (?<password>.*)'
$Matches.password
mysqld install


##########  安装并启动nacos   ##############



##########  安装并启动nginx   ##############
Expand-Archive -Path "./nginx-1.20.1.zip" -DestinationPath ./..
Set-Location ..
Rename-Item -Path "nginx-1.20.1" -NewName "nginx"
Set-Location nginx
Copy-Item "../WinSW.NET4.exe" -Destination .
Rename-Item -Path "WinSW.NET4.exe" -NewName "Nginx-Server.exe"
$nginxService = @"
<service>

<\service>
"@
$nginxService | Out-File "Nginx-Server.xml" -Encoding utf8
Set-Location conf
Remove-Item nging.conf
$nginxConf=@"
#user  nobody;
worker_processes  auto;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    server {
        listen       80;
        server_name  localhost;

        #access_log  logs/host.access.log  main;

        location / {
            root   html;
            index  index.html index.htm;
        }


        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}

"@
$nginxConf | Out-File "nignx.conf"
Set-Location ..
./Nginx-Server.exe install
Start-Service Nginx-Server
Set-Location ..


##########  安装并启动minio   ##############
New-Item -Name minio -Type Directory
Set-Location minio
New-Item -Name "miniodata" -Type Directory
Copy-Item "../minio.exe" -Destination .
Copy-Item "../WinSW.NET4.exe" -Destination .
Rename-Item -Path "WinSW.NET4.exe" -NewName "Minio-Server.exe"
$minioService = @"
<service>

<\service>
"@
$minioService | Out-File "Minio-Server.xml" -Encoding utf8
./Minio-Server.exe install
Start-Service Minio-Server
Set-Location ..


##########  安装服务          ##############
#$appName = dir
#foreach ($item in $appName)
#{
#    Set-Location $item
#    $serviceName = $item.name
#    ./${$serviceName}.exe install
#    Set-Location ..
#}

Set-Location
./.exe install
Set-Locationf ..

