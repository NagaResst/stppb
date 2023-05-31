#! /bin/bash
set -e
echo "部署脚本预检查"
if command -v unzip > /dev/null 2>&1; then
    :
else
    echo "需要安装 unzip"
    exit 1
fi

echo "============================================================="
echo "开始部署kafka相关组件"
echo "============================================================="

deploy_path=/home/kafka
echo ">>> 部署路径 $deploy_path"
echo " "
mkdir -p $deploy_path

echo "================="
echo ">>> 开始解压jdk"
tar zxf $(find . -name "jdk-*_linux-x64_bin.tar.gz") -C $deploy_path

export JAVA_HOME=$deploy_path/$(ls $deploy_path |grep jdk )
echo "JDK路径 $JAVA_HOME"

echo ">>> 开始解压zookeeper"
tar zxf $(ls |grep zookeeper) -C $deploy_path

echo ">>> 开始部署Zookeeper配置文件"
zookeeper_path=$deploy_path/$(ls $deploy_path |grep zookeeper )
zookeeper_data=$zookeeper_path/data

mkdir -p $zookeeper_data

echo tickTime=2000 >> $zookeeper_path/conf/zoo.cfg
echo dataDir=$zookeeper_data >> $zookeeper_path/conf/zoo.cfg
echo clientPort=2181 >> $zookeeper_path/conf/zoo.cfg
echo initLimit=5 >> $zookeeper_path/conf/zoo.cfg
echo syncLimit=2 >> $zookeeper_path/conf/zoo.cfg

echo ">>> 解压kafka"
tar zxf $(find . -name "kafka_*-*.tgz") -C $deploy_path
if [ -f kafka-console-ui.zip ]
then
unzip -q kafka-console-ui.zip -d $deploy_path
fi
kafka_path=$deploy_path/$(ls $deploy_path |grep kafka |grep -v console)


echo ">>> 解压debezium连接器"
debezium_path=$kafka_path/connect
mkdir -p $debezium_path
debezium_packages=($(ls |grep debezium))
for tgz in ${debezium_packages[*]}
do
tar zxf $tgz -C $debezium_path
done

echo ">>> 添加连接器配置"
sed -i "s@#plugin.path=@plugin.path=$debezium_path@g" $kafka_path/config/connect-distributed.properties
echo " "
echo "所有文件释放完成"
echo "============================================================"
echo "开始准备配置服务"

tee /usr/lib/systemd/system/zookeeper.service <<- 'EOF'
[Unit]
Description=zookeeper
After=network.target

[Service]
Environment="JAVA_HOME="
ExecStart=workpath/bin/zkServer.sh start
ExecStop=workpath/bin/zkServer.sh stop
Type=forking

[Install]
WantedBy=multi-user.target
EOF

sed -i "s@Environment=\"JAVA_HOME=\"@Environment=\"JAVA_HOME=$JAVA_HOME\"@g" /usr/lib/systemd/system/zookeeper.service
sed -i "s@workpath@$zookeeper_path@g" /usr/lib/systemd/system/zookeeper.service

echo "zookeeper服务化配置文件已配置完成"

tee /usr/lib/systemd/system/kafka.service <<- 'EOF'
[Unit]
Description=kafka
After=network.target

[Service]
Environment="JAVA_HOME="
ExecStart=workpath/bin/kafka-server-start.sh -daemon workpath/config/server.properties
ExecStop=workpath/bin/kafka-server-stop.sh
Type=forking

[Install]
WantedBy=multi-user.target
EOF

sed -i "s@Environment=\"JAVA_HOME=\"@Environment=\"JAVA_HOME=$JAVA_HOME\"@g" /usr/lib/systemd/system/kafka.service
sed -i "s@workpath@$kafka_path@g" /usr/lib/systemd/system/kafka.service

echo "kafka服务化配置文件已配置完成"

tee /usr/lib/systemd/system/debezium.service <<- 'EOF'
[Unit]
Description=debezium
After=network.target

[Service]
Environment="JAVA_HOME="
ExecStart=workpath/bin/connect-distributed.sh -daemon workpath/config/connect-distributed.properties
Type=forking

[Install]
WantedBy=multi-user.target
EOF

sed -i "s@Environment=\"JAVA_HOME=\"@Environment=\"JAVA_HOME=$JAVA_HOME\"@g" /usr/lib/systemd/system/debezium.service
sed -i "s@workpath@$kafka_path@g" /usr/lib/systemd/system/debezium.service

echo "debezium服务化配置文件已配置完成"

echo "重新载入服务化配置"
systemctl daemon-reload 
echo "============================================================="
echo " "
echo "启动zookeeper"
systemctl enable --now zookeeper
echo " "
echo "启动kafka"
systemctl enable --now kafka
echo " "
echo "启动debezium"
systemctl enable --now debezium
echo " "
set +e
i=0
ch=('|' '\' '-' '/')
index=0
while [ $i -le 200 ]
do
    printf "[%c] %s\r" ${ch[$index]} $str
    str="等待服务启动"
    ((i++))
    ((index=i%4))
    sleep 0.1
done
printf "\n"
echo "检查 zookeeper 服务是否存活"
systemctl status zookeeper |grep Active
echo "检查 kafka 服务是否存活"
systemctl status kafka |grep Active
echo "检查 debezium 服务是否存活"
systemctl status debezium |grep Active
