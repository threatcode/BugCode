#!/usr/bin/env bash
#

set -e

if [ -e $PGSQL_PASSWD ];then
	PGSQL_PASSWD=`cat $PGSQL_PASSWD`
fi

if [ -z "$PGSQL_USER" ]; then
	PGSQL_USER="bugcode_postgresql"
fi

if [ -z "$PGSQL_PASSWD" ]; then
	#cat is for cases when bugcode runs as a docker service
	PGSQL_PASSWD=`cat $PGSQL_PASSWD`
fi

if [ -z "$PGSQL_HOST" ]; then
	PGSQL_HOST="localhost"
fi

if [ -z "$PGSQL_PGSQL_DBNAME" ]; then
	PGSQL_DBNAME="bugcode"
fi

if [ -z "$LISTEN_ADDR" ]; then
	LISTEN_ADDR="127.0.0.1"
fi

echo "Restoring config file"
if [ ! -f "/home/bugcode/.bugcode/config/server.ini" ]; then
    mv /server.ini /home/bugcode/.bugcode/config/.
    CONNECTION_STRING="connection_string = postgresql+psycopg2:\/\/$PGSQL_USER:$PGSQL_PASSWD@$PGSQL_HOST\/$PGSQL_DBNAME"
    sed -i "s/connection_string = .*/$CONNECTION_STRING/"  /home/bugcode/.bugcode/config/server.ini
fi

export BUGCODE_HOME=/home/bugcode
echo "Trying to connect to database ..."
bugcode-manage create-tables
bugcode-manage migrate

export BUGCODE_HOME=/home/bugcode
/opt/bugcode/bin/bugcode-server
