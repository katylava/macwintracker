#!/usr/bin/env bash

launchdIntvl=30
user=`whoami`
bid='com.katylavallee.wintracker'
dest=~/Library/Application\ Support/$bid
pypath=`python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`
pythex=`which python`
[ -z $1 ] && intvl='3' || intvl=$1
limit=$(($launchdIntvl/$intvl))

cd "$(dirname $0)"
[ ! -d "${dest}" ] && mkdir "${dest}"
cp -f wintracker.py "${dest}/"
cp -f $bid.plist ~/Library/LaunchAgents

cd ~/Library/LaunchAgents
sed -i "s/{{USER}}/$user/" $bid.plist
sed -i "s/{{LIMIT}}/$limit/" $bid.plist
sed -i "s/{{LAUNCHDINTVL}}/$launchdIntvl/" $bid.plist
sed -i "s/{{INTERVAL}}/$intvl/" $bid.plist
sed -i "s:{{PYTHONPATH}}:$pypath:" $bid.plist
sed -i "s:{{PATH}}:${PATH//\:/\\:}:" $bid.plist
sed -i "
1 {
c\
#!$pythex
}" "${dest}/wintracker.py"

launchctl load $bid.plist
