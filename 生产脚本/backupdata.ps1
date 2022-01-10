#! /bin/pwsh
$now=get-date -Format "yyyy-MM-dd"
# 创建新的文件夹路径
New-Item -Path "d:\backupdata\$now" -Type Directory
set-location "d:\backupdata\$now"
# 进入文件夹路径备份数据库 ， Windows环境需要提前给mysql设置环境变量
mysqldump -uroot -pa0dy2vQI --all-databases > mysql.sql
# 打包备份minio的数据
Compress-Archive "d:\minio\" miniodata.zip