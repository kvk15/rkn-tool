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
    echo -e "\e[0m$line"
    curl --connect-timeout 10 -vsI "$line" 2>&1 >/dev/null | grep -E "(Loca)|(Rec)|(reset)|(timed out)|(resolve)|(communicate)"
    if [ $? -ne 1 ]; then
        echo -e "\e[32mBlocked"
    else
        echo -e "\e[31mUnblocked"
    fi
    echo " "
done ;

rm -rf $file
