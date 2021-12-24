#!/usr/bin/env sh

set -ex

if [ "${@:0:3}" = "gun" ];then
    python manage.py collectstatic --noinput
fi

exec "$@"
