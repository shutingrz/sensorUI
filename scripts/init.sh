#!/bin/sh

SCRIPT_DIR=$(cd $(dirname $0);pwd)
SCHEMA_DIR=${SCRIPT_DIR}/../bin/sensors/db/sql

if [ $# -ne 1 ];then
  cat <<_EOS_
Usage
  $0 databasefile_path
_EOS_
exit -1
fi

if [ ! -x $(which sqlite3) ];then
  echo "sqlite3 not found."
  exit -1
fi

dbfile=$1

# Create Database
rm ${dbfile} >/dev/null 2>&1

if [ ! -e ${dbfile} ];then
  echo ".open ${dbfile}" | sqlite3
fi

option="-noheader -separator ,"
sqlite="sqlite3 ${option} ${dbfile} "

#create table
for schema_file in ${SCHEMA_DIR}/*.sql; do
  echo ${schema_file}
  ${sqlite} < ${schema_file}
done