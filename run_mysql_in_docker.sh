CON_NAME="kronos-mysql"
CON_ID=$(sudo docker ps -a -f "name=${CON_NAME}" --format "{{.ID}}")
if [ "x${CON_ID}" == "x" ]
then
    sudo docker run --name ${CON_NAME} -p 3360:3306 -e MYSQL_ROOT_PASSWORD=PassWord -d mysql:5.7.28
else
    sudo docker start ${CON_NAME}
fi

#create database kronos_db CHARACTER SET utf8 COLLATE utf8_general_ci
