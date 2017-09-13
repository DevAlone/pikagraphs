#!/usr/env bash

while read line
do
	bash addUsername.sh $line
done < $1
