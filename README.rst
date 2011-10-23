Description
===========

Mac-only script for tracking active window. Records application name, window title,
current chat status (because I usually specify what I'm working on via my status), and,
*when possible*, extra data such as a URL or file path.  Logs results as JSON,
which you can parse however you pleaseth.


Installation
============

**Requires** `py-appscript <http://appscript.sourceforge.net/py-appscript/install.html>`_

Install ::

    $ git clone git://github.com/katylava/macwintracker.git
    $ cd macwintracker
    $ ./setup.sh <interval>

The active window will be logged every <interval> seconds.
You can run setup.sh again to change it.

To stop wintracker ::

    $ cd ~/Library/Application\ Support/com.katylavallee.wintracker
    $ ./uninstall.sh


How It Works
============

A launchd agent runs the main tracking script on load and pipes the output to a logfile. Another
launchd agent rotates and dedupes the logs once a day.

Output is stored as JSON in ~/Library/Logs/com.katylavallee.wintracker.
Parse at will.


Adding support for more applications
====================================

I'm adding applications as needed. If you fork the project and add apps
you use, submit a pull request.


Future
======

* Tools for parsing the log data... any ideas?
* Instead of putting logic for all applications in wintracker.py, create a plugin system
* Add parameters to setup script to allow user to configure log rotation interval
