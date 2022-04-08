#!/bin/bash
function dir_of_file() {
  if test -d $1
    then cd $1 || :
    # 当前枚举的对象如果是目录，就进入目录清除所有MD5文件重新计算
      echo "当前目录"$(pwd)
      rm -f *.md5
      echo "已清理MD5文件"
      # 继续枚举所有文件或目录
      cddir
  elif [ "${1##*.}"x = "md5"x ]
    then
      # 如果是MD5文件就什么都不做
      :
  else
    # 既不是目录，也不是MD5文件，那么就需要计算该文件的MD5值
    echo "正在计算$1的MD5"
    md5sum $1 > $1.md5
  fi
}
function cddir() {
  for obj in $(ls)
    do
    dir_of_file $obj
    done
    cd ..
}
cd /home/data || exit
cddir