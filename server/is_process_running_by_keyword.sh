#!/bin/sh
if [ `ps aux | grep $1 | grep -v grep | grep -v $0 | wc -l` = "0" ]
then
  exit 1
else
  exit 0
fi