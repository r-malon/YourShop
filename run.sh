#!/bin/sh
local_ip=$(ip -o route get to 1.1.1.1 | sed -n 's/.*src \([0-9.]\+\).*/\1/p')
flask run -h $local_ip
exit
