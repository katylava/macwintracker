*CURRENT NOT WORKING*
This is up on github so I can get help making it work.


Description
===========

Mac-only script for tracking active window. Records application name, window title,
current chat status (because I usually specify what I'm working on via my status), and,
*when possible*, extra data such as a URL or file path.  Logs results as JSON,
which you can parse however you pleaseth.


Installation
============

Install:
    $ git clone ... ~/Library/Application\ Support/com.katylavallee.wintracker
    $ cd <clone>
    $ ./setup.sh <interval>

The active window will be logged every <interval> seconds.
You can run setup.sh again to change it.

To stop wintracker:
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
