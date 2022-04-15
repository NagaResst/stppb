#!/bin/bash
#先获取一共有多少个端口需要进行测试 需要在同目录下创建文件 list.txt  一行一个 ip+空格+端口  例如 127.0.0.1 80
total="$(wc -l list.txt|awk '{print $1}')"
#开始准备进行轮询
times=1
echo "总数有${total}个,现在开始施工！"
while (($times<=$total))
do
ip=$(sed -n "${times}p" list.txt |awk '{print $1}' )
port=$(sed -n "${times}p" list.txt |awk '{print $2}' )
echo "正在执行第${times}个"
result=$(echo -e '\x1dclose\x0d' | timeout --signal=9 2 telnet ${ip} ${port} 2>/dev/null | grep "]" | wc -l)
if [ $result -eq 1 ];then
      echo "$ip的$port端口已开启"
else
      echo "$ip的$port端口未开启"
fi
let "times++"
done
echo "施工完毕"