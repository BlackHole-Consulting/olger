#!/usr/bin/env bash

if [ $# == 0 ]; then
    echo "Usage: $0 data-json mission_name"
    echo "* param1 example: 192.168.0.1-255"
    echo "* param2 example: home"
fi


node scripts/graphpdf.js $1 | dot -Tpdf > ./reports/$2/report$2.pdf
node scripts/graphpdf.js $1 > ./data.dot && xdot ./reports/$2/data$2.dot  
