#!/bin/sh


for z in /tmp/BEA/*.zip; do
    unzip -v $z | grep csv | awk '{print $NF}' | while read zf; do
        if unzip -p $z $zf | grep '[A-Za-z]""[A-Za-z]' | grep -v grep; then
            echo $z $zf
        fi
    done
done
