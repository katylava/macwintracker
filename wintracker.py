#!/usr/bin/env python

from appscript import app, its
import time
from subprocess import call, Popen, PIPE

SYSTEM_EVENTS = app(id="com.apple.systemEvents")

def watch(times=100, intvl=10):
    for i in range(1, times):
        log_frontmost()
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

    data = {'ts':time.time(), 'appname':appname, 'window':appname, 'status':get_chat_status()}

    if not scriptable: return data

    try:
        frontwin = frontapp.active_window()
    except:
        try:
            frontwin = frontapp.windows[its.index==1]
        except:
            try:
                frontwin = frontapp.windows[its.frontmost==True]
            except:
                frontwin = None

    if frontwin:
        try:
            data['window'] = frontwin.name()
        except:
            pass

    if appname == 'Notational Velocity':
        try:
            call('arch', '-i386', 'osascript', 'getNotationalVelocitySelection.scpt')
            data['note'] = get_clipboard_data()
        except:
            pass
    elif appname == 'Google Chrome':
        try:
            data['url'] = frontapp.windows[its.index==1].active_tab().URL()
        except:
            pass
    elif appname == 'Microsoft Word':
        try:
            data['document'] = frontapp.active_document.path()
        except:
            pass
    elif appname == 'Microsoft Excel':
        try:
            data['document'] = frontapp.active_workbook.path()
        except:
            pass
    elif appname == 'Adium':
        try:
            data['window'] = frontapp.active_chat.name()
        except:
            pass

    print data


def get_chat_status():
    if 'Adium' in [p.name() for p in SYSTEM_EVENTS.processes()]:
        status = app('Adium').global_status()
        return '%s -- %s' % (status.title(), status.status_message())
    else:
        return ''


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

