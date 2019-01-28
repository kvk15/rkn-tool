#!/bin/bash
file="/tmp/check"
chmod a+w $file


echo "Paste column URL/IP, for break empety lines"
while read line
do
    # break if the line is empty
    [ -z "$line" ] && break
    echo "$line" | grep -Eo 'http?.://[^ >]+' >> $file
done
cat $file | wc -l
cat $file | while read line
do
    echo "$line"
    curl --connect-timeout 10 -vsI "$line" 2>&1 >/dev/null | grep --color -E "(Loca)|(Rec)|(reset)|(timed out)|(resolve)|(communicate)"
    echo " "
done ;

rm -rf $file
