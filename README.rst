Description
===========

Mac-only script for tracking active window. Records application name, window title,
current chat status (because I usually specify what I'm working on via my status), and,
*when possible*, URL or file path.  Logs results as JSON, which you can parse however
you pleaseth.


Installation
============

Requires py-appscript and simplejson.

$ git clone ... ~/Library/Application\ Support/com.katylavallee.wintracker

# set StartInterval in the plist to the number of seconds you want between capturing frontmost window

$ cd ~/Library/LaunchAgents
$ ln -s ~/Library/Application\ Support/com.katylavallee.wintracker/com.katylavallee.wintracker.plist
$ launchctl load com.katylavallee.wintracker.plist


Consuming Output
================

Results are stored as JSON in ~/Library/Logs/com.katylavallee.wintracker
Parse at will.


Adding support for more applications
====================================

I'm adding applicatitns as needed. If you fork the project and add apps
you use, submit a pull request.
