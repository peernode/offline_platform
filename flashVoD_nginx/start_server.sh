#!/bin/bash 

echo "start nginx!"
/usr/sbin/nginx -c /common/flashp2p/offline_platform/flashVoD_nginx/conf/nginx.conf

echo "start uwsgi!"
(cd /common/flashp2p/offline_platform/flashVoD && uwsgi flashVoD.ini)

echo "start server end..."
