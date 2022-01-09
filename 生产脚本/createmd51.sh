#!/bin/bash
function cmd5() {
  # 检索当前文件的后缀不是md5， 那么就计算他的MD5并替换掉原来的值
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
# 对当前文件夹的每个文件都执行一次MD5计算
function lsfile() {
  for obj in $(ls)
    do
    cmd5 $obj
    done
    echo "计算结束"
}

lsfile
