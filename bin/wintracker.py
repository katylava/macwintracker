#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        except Exception as e:
            import traceback
            sys.stderr.write(
                "\n{}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            traceback.print_exc()
        else:
            line = json.dumps(data, ensure_ascii=False) # line is unicode
            sys.stdout.write("\n")
            sys.stdout.write(line.encode('utf-8'))

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
        data['window'] = normalize(frontwin.name())


    if appname == 'Google Chrome':
        data['url'] = frontwin.active_tab().URL()

    elif appname == 'Mailplane':
        title = normalize(frontapp.currentTitle())
        url = frontapp.currentURL()
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

    elif appname == 'iTerm':
        win = frontapp.current_terminal.current_session.name()
        data['window'] = win
        # can't get processs like you can in terminal, so try to get
        # it from session name
        parts = win.rpartition('(')
        if parts[-2] == '(':
            data['process'] = parts[-1][:-1] # to remove closing paren

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

def normalize(result):
    if result.__repr__() == 'k.missing_value':
        return None
    return result


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog <times> <interval>")
    (options, args) = parser.parse_args()
    watch(*[int(arg) for arg in args])

