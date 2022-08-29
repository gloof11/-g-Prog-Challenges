#!/bin/bash

if [ "$#" -ne 3 ]; then
	echo "LPORT image container_name"
	exit
fi

containerName=$3
imageName=$2

docker run -p $1:8000 --name $containerName $imageName

if [ "$?" != "0" ]; then
	docker start $containerName
	docker attach $containerName
fi
