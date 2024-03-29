#!/usr/bin/env bash


set -e


if [ ! -f "$BUGCODE_HOME/.bugcode/config/server.ini" ]; then
    if [ -z "$PGSQL_USER" ] || [ -z "$PGSQL_PASSWD" ] || [ -z "$PGSQL_HOST" ] || [ -z "$PGSQL_DBNAME" ] ; then
        echo "$(date) Missing database configuration..."
        exit 1
    fi
    CREATE_TABLES=1
    CREATE_ADMIN=1
    echo "$(date) Creating server.ini"
    mkdir -p $BUGCODE_HOME/.bugcode/config
    mkdir -p $BUGCODE_HOME/.bugcode/storage
    mkdir -p $BUGCODE_HOME/.bugcode/logs
    mkdir -p $BUGCODE_HOME/.bugcode/session
    touch $BUGCODE_HOME/.bugcode/logs/alembic.log
    cp /docker_server.ini $BUGCODE_HOME/.bugcode/config/server.ini
    CONNECTION_STRING="connection_string = postgresql+psycopg2:\/\/$PGSQL_USER:$PGSQL_PASSWD@$PGSQL_HOST\/$PGSQL_DBNAME"
    sed -i "s/connection_string = .*/$CONNECTION_STRING/"  $BUGCODE_HOME/.bugcode/config/server.ini
    if [ ! -z "$REDIS_SERVER" ]; then
      REDIS_STRING="redis_session_storage = $REDIS_SERVER"
      sed -i "s/#redis_session_storage = .*/$REDIS_STRING/"  $BUGCODE_HOME/.bugcode/config/server.ini
    fi
else
    echo "$(date) Using existing server.ini"
    CREATE_TABLES=0
    CREATE_ADMIN=0
    sleep 3
fi

if [ $CREATE_TABLES -eq 1 ]; then
    echo "Waiting for postgres on $PGSQL_HOST"
    while ! nc -z $PGSQL_HOST 5432; do
      sleep 0.5
    done
    echo "$(date) Creating tables on database $PGSQL_DBNAME..."
    bugcode-manage create-tables
fi
if [ $CREATE_ADMIN -eq 1 ]; then
    if [ -z "$BUGCODE_PASSWORD" ]; then
      BUGCODE_PASSWORD=$(tr -dc 'A-Za-z0-9!"#$%&'\''()*+,-./:;<=>?@[\]^_{|}~' </dev/urandom |head -c 13 ; echo)
    fi
    echo "$(date) Creating superuser..."
    bugcode-manage create-superuser --username bugcode --password $BUGCODE_PASSWORD --email "user@email.com"
    echo "Admin user created with username: bugcode password: $BUGCODE_PASSWORD"
fi

echo "Update swagger..."
bugcode-manage openapi-swagger --server https://$FQDN

echo "$(date) Running migrations ..."
bugcode-manage migrate

echo "$(date) Starting Bugcode server with workers..."
bugcode-server --with-workers --bind 0.0.0.0
