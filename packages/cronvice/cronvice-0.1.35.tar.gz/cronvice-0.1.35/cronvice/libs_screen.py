#!/usr/bin/env python3

from fire import Fire
from console import fg, bg
import shutil
import os
import datetime as dt
import shlex
import subprocess as sp
#import config
from cronvice import config

#=========================================================================
#
#-------------------------------------------------------------------------
#

def is_session_desktop():
    if os.environ.get('SSH_TTY'):
        return False #"SSH Terminal Session"
    elif os.environ.get('DISPLAY'):
        return True#"Desktop Session"
    else:
        return False#"Unknown Session"

#=========================================================================
#
#-------------------------------------------------------------------------
#

def enter_screen(scrname, term=""):
    """
    it enters when run from here
    """
    sessions = list_screen_sessions()
    # ADD .local/bin
    env = os.environ.copy()
    env['PATH'] = env.get('PATH', '') + ':' + os.path.expanduser('~/.local/bin')
    #print(sessions)
    #print(scrname)
    if is_in_screen(scrname, sessions):
        CMD = f"screen -x {scrname}"
        if is_session_desktop() and term != "same":
            args = shlex.split(f"xterm -e bash -c '{CMD}'")
            process = sp.Popen(args,  stdout=sp.DEVNULL, stderr=sp.DEVNULL, env=env)
            process.poll()
        else:
            args = shlex.split(f"bash -c '{CMD}'")
            res = sp.call(args, env=env)

#=========================================================================
#
#-------------------------------------------------------------------------
#

def stop_screen(scrname):
    """
    it enters when run from here
    """
    sessions = list_screen_sessions()
    # ADD .local/bin
    env = os.environ.copy()
    env['PATH'] = env.get('PATH', '') + ':' + os.path.expanduser('~/.local/bin')
    #print(sessions)
    #print("-", scrname, "-")
    if is_in_screen(scrname, sessions):
        CMD = f"screen -X -S {scrname} quit"
        if is_session_desktop():
            args = shlex.split(f"xterm -e bash -c '{CMD}'")
            process = sp.Popen(args,  stdout=sp.DEVNULL, stderr=sp.DEVNULL, env=env)
            process.poll()
        else:
            args = shlex.split(f"bash -c '{CMD}'")
            res = sp.call(args, env=env)
    else:
        print("X.. no such screen:", scrname)



#=========================================================================
#
#-------------------------------------------------------------------------
#

def list_screen_sessions():
    """
    return the existing screen sessions; used in enter and stop....
    """
    try:
        result = sp.run(['screen', '-ls'], capture_output=True, text=True, check=True)
        #print(result.stdout)
        res = result.stdout.strip().split('\n')[1:-1]
        #print(res) # many
        return res
    except sp.CalledProcessError as e:
        #print(f"x... screen ls - error occurred: {e}")
        pass
    return None


#=========================================================================
#
#-------------------------------------------------------------------------
#

def tidy_screen_sessions( sessions):
    """
    tidy uo  the list of existing screen sessions; decodes also time
    """
    if sessions is None:return None
    #print('tidy', sessions) #many
    running = []
    for i in sessions:
        #print(i)
        line = i.strip().split("\t")
        xtime = line[1].strip("(").strip(")")
        xtime = dt.datetime.strptime(xtime, "%d/%m/%y %H:%M:%S")
        #tses.append(f"{line[0]}  {xtime}")
        xlong = dt.datetime.now() - xtime
        name_to_app = line[0].split(".")[-1]
        # remove _CX
        if name_to_app.find( config.CONFIG['screentag'] ) > 0:
            print(f"{line[0]:20s} -  {xtime}  -  {xlong}")
            name_to_app = name_to_app.split( config.CONFIG['screentag'] )[0]
            running.append(name_to_app )
        #print('runinng', running)
    return running



#=========================================================================
#
#-------------------------------------------------------------------------
#

def is_in_screen(TAG, sessions):
    """
    if tag in screen list => True
    """
    if sessions is None:return False
    for i in sessions:
        #print(i, TAG, i.find(TAG) )
        if i.find(f"{TAG}{config.CONFIG['screentag']}") > 0:
            return True
    return False

#=========================================================================
#
#-------------------------------------------------------------------------
#


def del_job_anycommand( cron, tag):
    """
    older
    """
    ACT = False
    RMTG = f"screen -dmS {tag} " #SPACE IMPORTANT
    for job in cron:
        if job.command.find(RMTG) > 0:
            print(f"i... removing /{RMTG}/ ")#... {job}")
            cron.remove(job)
            ACT = True
    if ACT:
        cron.write()

if __name__ == "__main__":
    Fire({"e": enter_screen
        }
         )
