#!/bin/sh

if [ -d /zroot/portal ] ; then
    cp /home/jails.apache/.zfs-source/usr/local/etc/apache24/* /zroot/portal/usr/local/etc/apache24/
    echo "[38;5;196m! WARNING ! - Please restart portal with : '/usr/sbin/jexec portal /usr/sbin/service apache24 restart'[0m"
fi
