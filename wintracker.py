#!/usr/bin/env python

from appscript import app, its
import time
from subprocess import Popen, PIPE

SYSTEM_EVENTS = app(id="com.apple.systemEvents")

def watch(times=100, intvl=10):
    for i in range(1, times):
        try:
            data = log_frontmost()
            # instead of 'print', pipe to stdout
            print data
        except Exception as e:
            # instead of 'print', pipe to stderr
            print e
        try:
            time.sleep(intvl)
        except KeyboardInterrupt:
            print 'done'
            return


def log_frontmost():
    frontproc = SYSTEM_EVENTS.processes[its.frontmost == True][0]
    scriptable = frontproc.has_scripting_terminology()
    appname = frontproc.name()
    if scriptable:
        frontapp = app(frontproc.name())
        appname = frontapp.name()

    data = {'ts':time.time(), 'appname':appname, 'window':appname, 'file':None, 'status':get_chat_status()}

    if not scriptable: return data

    try:
        frontwin = frontapp.active_window()[0]
    except:
        try:
            frontwin = frontapp.windows[its.index==1][0]
        except:
            try:
                frontwin = frontapp.windows[its.frontmost==True][0]
            except:
                frontwin = None

    if frontwin:
        data['window'] = frontwin.name()

    if appname == 'Notational Velocity':
        frontproc.menu_bars[0].menus['Edit'].menu_items['Copy URL'].click()
        data['file'] = get_clipboard_data()

    elif appname == 'Google Chrome':
        data['file'] = frontwin.active_tab().URL()

    elif appname == 'Microsoft Word':
        data['file'] = frontapp.active_document.path()

    elif appname == 'Microsoft Excel':
        data['file'] = frontapp.active_workbook.path()

    elif appname == 'Adium':
        data['file'] = frontapp.active_chat.name()

    return data


def get_chat_status():
    if 'Adium' in [p.name() for p in SYSTEM_EVENTS.processes()]:
        status = app('Adium').global_status()
        return '%s -- %s' % (status.title(), status.status_message())
    else:
        return None


def get_clipboard_data():
    p = Popen(['pbpaste'], stdout=PIPE)
    retcode = p.wait()
    data = p.stdout.read()
    return data


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog <times> <interval>")
    (options, args) = parser.parse_args()
    watch(*[int(arg) for arg in args])

