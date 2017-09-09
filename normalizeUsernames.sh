#!/bin/bash

cat usernames | tr '[:upper:]' '[:lower:]' | sort -f -u > usernames.new
mv usernames.new usernames
