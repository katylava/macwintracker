#!/usr/bin/env bash

user=`whoami`
bid='com.katylavallee.wintracker'
dest="~/Library/Application Support/$bid"
[ -z $1 ] && intvl='3' || intvl=$1


cd "${0##*/}"
[ ! -d "${dest}" ] && mkdir "${dest}"
cp -f wintracker.py "${dest}/"
cp -f $bid.plist ~/Library/LaunchAgents

cd ~/Library/LaunchAgents
sed -i "s/{{USER}}/$user/" $bid.plist
sed -i "s/{{INTERVAL}}/$intvl/" $bid.plist

launchctl load $bid.plist
