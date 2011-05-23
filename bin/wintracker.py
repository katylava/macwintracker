#!/usr/bin/env python

import time, sys, json
from datetime import datetime
from subprocess import Popen, PIPE
from appscript import app, its
from jsonlogdedupe import compare


CURRENT_OBJECT = {}

def sysevents():
    # needs to be refreshed frequently, so get it fresh every time
    return app(id="com.apple.systemEvents")

def watch(intvl=10):
    while True:
        try:
            data = log_frontmost(intvl)
            print json.dumps(data)
        except Exception as e:
            print >>sys.stderr, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ' ERROR:', e
        try:
            time.sleep(intvl)
        except KeyboardInterrupt:
            print 'done'
            break
    return 0


def log_frontmost(resolution=10):
    frontproc = sysevents().processes[its.frontmost == True][0]
    scriptable = frontproc.has_scripting_terminology()
    appname = frontproc.name()
    frontwin = None
    ts = time.time()

    data = {
        'time_start': ts,
        'time_end':   ts + resolution,
        'appname':   appname,
        'window':    '',
        'status':    get_chat_status()
    }

    if scriptable:
        frontapp = app(frontproc.name())
        try:
            frontwin = frontapp.active_window().pop()
        except:
            pass
        if not frontwin:
            try:
                frontwin = frontapp.windows[its.index==1].get().pop()
            except:
                pass
        if not frontwin:
            try:
                frontwin = frontapp.windows[its.frontmost==True].get().pop()
            except:
                pass
        if not frontwin:
            try:
                frontwin = frontapp.windows().pop()
            except:
                pass
    else:
        try:
            data['window'] = ','.join([w for w in frontproc.windows.name() if isinstance(w, unicode)])
        except:
            pass


    if frontwin:
        data['window'] = frontwin.name()

    if appname in ['Notational Velocity','nvALT']:
        frontproc.menu_bars[0].menus['Edit'].menu_items['Copy URL'].click()
        data['url'] = get_clipboard_data()

    elif appname == 'Google Chrome':
        data['url'] = frontwin.active_tab().URL()

    elif appname == 'Mailplane':
        title = frontapp.currentTitle()
        url = frontapp.currentURL()
        if title.__str__() == 'k.missing_value':
            title = None
        data.update({'title':title,'url':url})

    elif appname == 'Microsoft Word':
        data['file'] = '%s:%s' % (frontapp.active_document.path(), data['window'])

    elif appname == 'Microsoft Excel':
        data['file'] = '%s:%s' % (frontapp.active_workbook.path(), data['window'])

    elif appname == 'Microsoft PowerPoint':
        data['file'] = '%s:%s' % (frontapp.active_presentation.path(), data['window'])

    elif appname == 'Adium':
        data['chat'] = frontapp.active_chat.name()

    elif appname == 'LaunchBar':
        data['selection'] = frontapp.selection_as_text()

    elif appname == 'Terminal':
        data['process'] = frontwin.selected_tab.processes()[-1]

    elif appname == 'iTunes':
        data['state'] = frontapp.player_state().name.title()
        if data['state'] != 'Stopped':
            data['playlist'] = frontapp.current_playlist.name()

    elif appname == 'Numbers':
        data['file'] = frontwin.document.path()

    elif appname == 'Skitch':
        try:
            data['title'] = frontproc.windows.text_fields.value()[0][0]
        except:
            pass


    global CURRENT_OBJECT
    if compare(CURRENT_OBJECT, data, ['time_start','time_end']):
        data['time_start'] = CURRENT_OBJECT['time_start']
    CURRENT_OBJECT = data

    return data


def get_chat_status():
    if 'Adium' in [p.name() for p in sysevents().processes()]:
        status = app('Adium').global_status()
        message = status.status_message()
        title = status.title()
        stype = status.status_type().name.title()
        rettext = "%s (%s)" % (title, stype)
        if message and message != title:
            rettext =  "%s -- %s" % (rettext, message)
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

