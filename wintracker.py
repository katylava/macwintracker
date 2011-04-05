#!/usr/bin/env python

import time, sys
import simplejson as json
from appscript import app, its
from subprocess import Popen, PIPE

SYSTEM_EVENTS = app(id="com.apple.systemEvents")

def watch(times=100, intvl=10):
    for i in range(1, times):
        try:
            data = log_frontmost()
            print json.dumps(data)
        except Exception as e:
            print >>sys.stderr, 'ERROR:', e
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

    frontwin = None
    try:
        frontwin = frontapp.active_window()[0].get()
    except:
        try:
            frontwin = frontapp.windows[its.index==1][0].get()
        except:
            try:
                frontwin = frontapp.windows[its.frontmost==True][0].get()
            except:
                pass

    if frontwin:
        data['window'] = frontwin.name()

    if appname == 'Notational Velocity':
        frontproc.menu_bars[0].menus['Edit'].menu_items['Copy URL'].click()
        data['url'] = get_clipboard_data()

    elif appname == 'Google Chrome':
        data['url'] = frontwin.active_tab().URL()

    elif appname == 'Microsoft Word':
        data['file'] = frontapp.active_document.path()

    elif appname == 'Microsoft Excel':
        data['file'] = frontapp.active_workbook.path()

    elif appname == 'Microsoft PowerPoint':
        data['file'] = '%s:%s' % (frontapp.active_presentation.path(), data['window'])

    elif appname == 'Adium':
        data['chat'] = frontapp.active_chat.name()

    elif appname == 'LaunchBar':
        data['selection'] = frontapp.selection_as_text()

    elif appname == 'Terminal':
        data['process'] = frontwin.selected_tab.processes()[-1]

    return data


def get_chat_status():
    if 'Adium' in [p.name() for p in SYSTEM_EVENTS.processes()]:
        status = app('Adium').global_status()
        message = status.status_message()
        title = status.title()
        stype = status.status_type().name.title()
        rettext = "%s (%s)" % (title, stype)
        if message and message != title:
            rettext -  "%s -- %s" % (rettext, message)
        return rettext
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

