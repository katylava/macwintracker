#!/usr/bin/env bash

user=`whoami`
bid='com.katylavallee.wintracker'
dest=~/Library/Application\ Support/$bid
pypath=`python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`
pythex=`which python`
[ -z $1 ] && intvl='3' || intvl=$1

cd "$(dirname $0)"
[ ! -d "${dest}" ] && mkdir "${dest}"
cp -f bin/* "${dest}/"
cp -f launchagents/* ~/Library/LaunchAgents

cd ~/Library/LaunchAgents
sed -i "s/{{USER}}/$user/" $bid*.plist
sed -i "s:{{PATH}}:${PATH//\:/\\:}:" $bid*.plist
sed -i "s:{{PYTHONPATH}}:$pypath:" $bid*.plist
sed -i "s/{{INTERVAL}}/$intvl/" $bid.plist
sed -i "
1 {
c\
#!$pythex
}" "${dest}/wintracker.py"
sed -i "
1 {
c\
#!$pythex
}" "${dest}/jsonlogdedupe.py"



cd "$(dirname $0)"
./uninstall.sh
launchctl load $bid.plist
launchctl load ${bid}LogRotate.plist
