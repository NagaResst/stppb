#!/bin/bash
function diroffile() {
  if test -d $1
    then cd $1
      echo "当前目录"`pwd`
      # rm -f *.md5
      # echo "已清理MD5文件"
      cddir
  elif [ "${1##*.}"x = "md5"x ]
    then
      :
  else
    echo "正在计算$1的MD5"
    md5sum $1 > $1.md5
  fi
}
function cddir() {
  for obj in $(ls)
    do
    diroffile $obj
    done
    cd ..
}

cddir
