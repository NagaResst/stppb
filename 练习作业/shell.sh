#！ /bin/bash

cd /opt/ManageEngine/OpManager/bin
source ./shutdown.sh
sleep 5
while :
do
  if [ `ps -e | grep java | grep -c ''` == 0 ]; then break ; fi
done
cd backup
source  ./BackupDB.sh
cd ..
source ./run.sh &
