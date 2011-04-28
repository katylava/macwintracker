Description
===========

Mac-only script for tracking active window. Records application name, window title,
current chat status (because I usually specify what I'm working on via my status), and,
*when possible*, extra data such as a URL or file path.  Logs results as JSON,
which you can parse however you pleaseth.


Installation
============

Install ::

    $ git clone git://github.com/katylava/macwintracker.git
    $ cd macwintracker
    $ ./setup.sh <interval>

The active window will be logged every <interval> seconds.
You can run setup.sh again to change it.

To stop wintracker ::

    $ cd ~/Library/Application\ Support/com.katylavallee.wintracker
    $ ./uninstall.sh

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

* Add a command-line utility which accepts a regular expression such as "^Project A.*" and a
  datetime range and outputs a duration.
* Don't log duplicate lines (if performance won't suffer much for it)
* Add a launchd log rotator


Sample Output
=============

These are not in order, just a few interesting ones I grabbed from my logs ::

    {"status": "Available (Available)", "process": "Python", "window": "~/Code/Scripts/com.katylavallee.wintracker \u2014 Python", "ts": 1302128139.8369579, "appname": "Terminal"}
    {"status": "Available (Available)", "process": "bash", "window": "~/Library/Logs/com.katylavallee.wintracker \u2014 bash", "ts": 1302128149.927207, "appname": "Terminal"}
    {"status": "Available (Available)", "url": "http://stackoverflow.com/questions/5573538/launchd-executes-python-script-but-import-fails/5573798#5573798", "window": "launchd executes python script, but import fails - Stack Overflow", "ts": 1302200640.6808341, "appname": "Google Chrome"}
    {"status": "Available (Available)", "window": "wintracker_err.log,system.log", "ts": 1302201983.510272, "appname": "Console"}
    {"status": "projectA (Available)", "process": "less", "window": "~/Library/Logs", "ts": 1302633220.793612, "appname": "Terminal"}
    {"status": "projectA (Available)", "url": "nv://find/WORK/?SN=agtzaW1wbGUtbm90ZXINCxIETm90ZRiu_KsCDA&NV=f3%2B%2Fd6EXSVmpIuIihKF9JQ%3D%3D", "window": "Notation", "ts": 1302633153.4456601, "appname": "nvALT"}
    {"status": "brb (Away)", "window": "LaunchBar", "selection": "Start Screen Saver", "ts": 1302629931.1745031, "appname": "LaunchBar"}
    {"status": "Available (Available)", "window": "Mailplane for Work", "appname": "Mailplane", "url": "mailplane://katy.lavallee%40blahblahblah.com/#mbox/12f48354ddedcc4a", "title": "DFWIMA Awards", "ts": 1302626976.5536239}
    {"status": "Available (Available)", "window": "Contacts", "ts": 1302621669.4440269, "chat": "#farstar", "appname": "Adium"}
