#!/bin/bash

cat usernames | sort -f -u > usernames.new
mv usernames.new usernames
