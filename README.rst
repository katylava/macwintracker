Status
======

wintracker is currently working for me, but only tracks every 11 seconds instead of 3 (the interval
I set in the launchd plist).  My system.log says stuff like ::

  Apr  7 13:52:00 Exhilarator com.apple.launchd.peruser.506[296] (com.katylavallee.wintracker): Throttling respawn: Will start in 4 seconds
  Apr  7 13:52:03 Exhilarator com.apple.launchd.peruser.506[296] (com.katylavallee.wintracker): Throttling respawn: Will start in 1 seconds
  Apr  7 13:52:07 Exhilarator com.apple.launchd.peruser.506[296] (com.katylavallee.wintracker): Throttling respawn: Will start in 7 seconds
  Apr  7 13:52:09 Exhilarator com.apple.launchd.peruser.506[296] (com.katylavallee.wintracker): Throttling respawn: Will start in 6 seconds
  Apr  7 13:52:12 Exhilarator com.apple.launchd.peruser.506[296] (com.katylavallee.wintracker): Throttling respawn: Will start in 3 seconds
  Apr  7 13:52:18 Exhilarator com.apple.launchd.peruser.506[296] (com.katylavallee.wintracker): Throttling respawn: Will start in 7 seconds
  Apr  7 13:52:21 Exhilarator com.apple.launchd.peruser.506[296] (com.katylavallee.wintracker): Throttling respawn: Will start in 5 seconds
  Apr  7 13:52:24 Exhilarator com.apple.launchd.peruser.506[296] (com.katylavallee.wintracker): Throttling respawn: Will start in 2 seconds
  Apr  7 13:52:29 Exhilarator com.apple.launchd.peruser.506[296] (com.katylavallee.wintracker): Throttling respawn: Will start in 7 seconds

I assume it has something to do with how launchd works, which is a bit of mystery to me.

Description
===========

Mac-only script for tracking active window. Records application name, window title,
current chat status (because I usually specify what I'm working on via my status), and,
*when possible*, extra data such as a URL or file path.  Logs results as JSON,
which you can parse however you pleaseth.


Installation
============

Install ::

    $ git clone git://github.com/katylava/macwintracker.git ~/Library/Application\ Support/com.katylavallee.wintracker
    $ cd ~/Library/Application\ Support/com.katylavallee.wintracker
    $ ./setup.sh <interval>

The active window will be logged every <interval> seconds.
You can run setup.sh again to change it.

To stop wintracker ::

    $ launchctl unload ~/Library/LaunchAgents/com.katylavallee.wintracker

Requires appscript.

Consuming Output
================

Results are stored as JSON in ~/Library/Logs/com.katylavallee.wintracker
Parse at will.


Adding support for more applications
====================================

I'm adding applicatitns as needed. If you fork the project and add apps
you use, submit a pull request.


Future
======

Add a command-line utility which accepts a regular expression such as "^Project A.*" and a
datetime range and outputs a duration.
