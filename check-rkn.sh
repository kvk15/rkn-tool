#!/bin/bash
file="/tmp/check"
chmod a+w $file
rm -rf  ~/html/*
cat /dev/null > $file
cat /dev/null > ~/wlog


echo "Paste column URL/IP, for break empety lines"
while read line
do
    # break if the line is empty
    [ -z "$line" ] && break
    echo "$line"|awk -F, {'print $1'} >> $file
done
cat $file | wc -l
cat $file | while read line
do
    echo "$line"
    curl --connect-timeout 10 -vsI "$line" 2>&1 >/dev/null | grep -E "(Loca)|(Rec)|(reset)|(timed out)"
    echo " "
done ;


