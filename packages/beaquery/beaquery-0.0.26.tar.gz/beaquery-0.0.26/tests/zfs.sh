#!/bin/sh


for z in /tmp/BEA/*.zip; do
    echo $z
    unzip -v $z | grep csv | awk '{print $NF}' | while read zf; do
        echo $zf
        echo  $zf | grep "[' :)(]"
    done
done
