CON_NAME="kronos-mysql"
CON_ID=$(sudo docker ps -a -f "name=${CON_NAME}" --format "{{.ID}}")
MYSQL_ROOT_PASS="PassWord"
MYSQL_VERSION='5.7.28'
MYSQl_PORT='3360'

if [ "x${CON_ID}" == "x" ]
then
    sudo docker run --name ${CON_NAME} -p ${MYSQl_PORT}:3306 -e MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASS} -d mysql:${MYSQL_VERSION}
else
    sudo docker start ${CON_NAME}
fi

# we are need to install mysql-client to restore DB
mysql -u root -p${MYSQL_ROOT_PASS} -h 127.0.0.1 -P ${MYSQl_PORT} -e "create database if not exists kronos_db CHARACTER SET utf8 COLLATE utf8_general_ci"
