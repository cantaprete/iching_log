#!/bin/zsh

SAMPLES=100000

echo "time,hex,type" > control-sample.csv

for i in {1..$SAMPLES};
do
    iching -w -c >> control-sample.csv ;
    echo -n -e "\r$i"
done
