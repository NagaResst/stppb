#!/bin/bash
function cmd5() {
  if [ "${1##*.}"x = "md5"x ]
    then
      :
  elif test -d $1
    then
      :
  else
    echo "正在计算$1的MD5"
    md5sum $1 > $1.md5
  fi
}

inotifywait -mrq --format  '%w%f' -e close_write,move /home/data/ | while read -r file
# 监听目录内文件的“写入关闭”、“移动”行为 并将结果传递给while执行
do
if [ "${file##*.}"x = "md5"x ]
    #判断文件名后缀
    then
      :
  else
    dir=$(dirname $file)
    # 分离传入结果的路径和文件名
    nf=$(echo $file | awk '{gsub(/\/.*\//,"",$1); print}')
    cd $dir || :
    # date
    # echo $file
    cmd5 $nf
  fi
done