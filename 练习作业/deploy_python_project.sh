#! /usr/bin/bash

BASE_PATH=$(dirname $(readlink -f $0))
PYTHON_VENV=.venv/bin/python
PIP_MIRROR="-i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com"
PROJECT_PATH="no_path"

#if type git >/dev/null 2>&1; then
#  :
#else
#  yum install git -y >> /dev/null || echo "git 安装失败， 请检查网络连接"
#fi

function vid2densepose() {
  PROJECT_PATH=vid2densepose

  [ -f .${PROJECT_PATH}.path ] && INSTALL_PATH=$(cat .${PROJECT_PATH}.path) || INSTALL_PATH=${BASE_PATH}/${PROJECT_PATH}
  PYTHON_VENV=${INSTALL_PATH}/.venv/bin/python

  if [[ $2 == "install" ]]; then
    echo "开始部署项目"
    echo "添加python虚拟环境支持"
    apt autoremove -y --purge needrestart >> /dev/null
    apt install -y python3.10-venv >> /dev/null
    # build_python
#    read -r -p "请输入项目部署目录 (默认为当前目录): " INSTALL_PATH
    INSTALL_PATH=$3
    [ -z "$INSTALL_PATH" ] && INSTALL_PATH=${BASE_PATH}/${PROJECT_PATH} || INSTALL_PATH=${INSTALL_PATH}/${PROJECT_PATH}
    echo "创建项目目录 ${INSTALL_PATH}"
    mkdir -p ${INSTALL_PATH} && cd ${INSTALL_PATH}
    echo "${INSTALL_PATH}" > $BASE_PATH/.${PROJECT_PATH}.path
    echo "创建虚拟环境"
    python3.10 -m venv ${INSTALL_PATH}/.venv
    PYTHON_VENV=${INSTALL_PATH}/.venv/bin/python

    if [ -d ${INSTALL_PATH}/${PROJECT_PATH} ] ;then
      echo "项目已存在, 跳过下载，开始运行环境预检查"
      package_check
    else
      echo "开始下载项目"
      cd ${INSTALL_PATH} && git clone https://github.com/Flode-Labs/vid2densepose.git || echo "项目下载失败,请检查网络连接是否可以访问github"
      [ -d ./${PROJECT_PATH} ] && cd ${PROJECT_PATH} && git clone https://github.com/facebookresearch/detectron2.git && cd .. && package_check
    fi

  elif [[ $2 == "uninstall" ]]; then
    uninstall

  elif [[ $2 == "app.py" ]]; then
    ${PYTHON_VENV} ${INSTALL_PATH}/${PROJECT_PATH}/app.py

  else
    ${PYTHON_VENV} ${INSTALL_PATH}/${PROJECT_PATH}/main.py $2 $3 $4 $5
  fi
}

function package_check() {
  if [ -f $BASE_PATH/.${PROJECT_PATH}.path ]; then
    INSTALL_PATH=$(cat $BASE_PATH/.${PROJECT_PATH}.path)
  else
    INSTALL_PATH=${BASE_PATH}/${PROJECT_PATH}
  fi
  echo "开始安装依赖包"
  ${PYTHON_VENV} -m pip install wheel
  [ -f ${INSTALL_PATH}/${PROJECT_PATH}/requirements.txt ] && cat ${INSTALL_PATH}/$PROJECT_PATH/requirements.txt | xargs -L 1 ${PYTHON_VENV} -m pip install
  echo "依赖包安装完成"
}

function uninstall() {
  if [ -f .${PROJECT_PATH}.path ]; then
    INSTALL_PATH=$(cat .${PROJECT_PATH}.path)
  else
    INSTALL_PATH=${BASE_PATH}/${PROJECT_PATH}
  fi
  rm -rf ${INSTALL_PATH}
  rm -f .${PROJECT_PATH}.path
  echo "卸载完成"
}

function build_python() {
  if [ -d /usr/local/python-3.8.19 ]; then
    echo "发现python运行环境"
  else
    echo "开始编译python运行环境"
    yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make libffi-devel openssl-devel openssl11 openssl11-devel >> /dev/null
    cd /usr/local/src
    wget https://www.python.org/ftp/python/3.8.19/Python-3.8.19.tgz && tar -zxvf Python-3.8.19.tgz >> /dev/null && cd Python-3.8.19
    if [ -f configure ]; then
      # python 3.10.14 需要 openssl 1.1.1
      # export CFLAGS=$(pkg-config --cflags openssl11)
      # export LDFLAGS=$(pkg-config --libs openssl11)
      ./configure --prefix=/usr/local/python-3.8.19
      make -j $(nproc)  || echo "编译失败" ; rm -rf /usr/local/src/Python-3.8.19
      make install
      mv /usr/bin/python3 /usr/bin/python3.bak
      ln -s /usr/local/python-3.8.19/bin/python3 /usr/bin/python3
      echo "编译完成"
    fi
  fi
}

$1 $*