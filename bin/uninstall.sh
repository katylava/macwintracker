#!/usr/bin/env bash

bid='com.katylavallee.wintracker'
dest=~/Library/Application\ Support/$bid

running=`launchctl list | grep $bid`
[ ! -z "${running}" ] && launchctl unload ~/Library/LaunchAgents/$bid.plist
running=`launchctl list | grep ${bid}LogRotate`
[ ! -z "${running}" ] && launchctl unload ~/Library/LaunchAgents/${bid}LogRotate.plist

rm -f ~/Library/LaunchAgents/$bid.plist
rm -f ~/Library/LaunchAgents/${bid}LogRotate.plist
rm -fr "${dest}"
