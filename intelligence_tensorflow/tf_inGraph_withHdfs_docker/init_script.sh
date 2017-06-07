#!/usr/bin/env bash

gosu stratio bash -c "mkdir /tmp/65010"
gosu stratio bash -c "export KRB5CCNAME=FILE:/tmp/65010/krb5cc_65010"
echo "export KRB5CCNAME=FILE:/tmp/65010/krb5cc_65010" >> /home/stratio/.bashrc
gosu stratio bash -c "kinit -V stratio -t /home/stratio/stratio.keytab"

echo "10.200.0.74 hdfs-namenode1.labs.stratio.com" >> /etc/hosts

gosu stratio bash -c "KERB_TICKET_CACHE_PATH=/tmp/65010/krb5cc_65010 python3.5 /tmp/init_inGraph_tf.py $1 $2 $3 $4 $5 $6"
