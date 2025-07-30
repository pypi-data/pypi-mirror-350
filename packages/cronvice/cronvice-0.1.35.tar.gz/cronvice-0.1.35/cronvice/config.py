#!/usr/bin/env python3
from cronvice.version import __version__
from fire import Fire

import json
import os
import sys
from crontab import CronTab  # install python-crontab
import os
import getpass
import datetime as dt

# ----- port here. 5000 is flask; is moved to 8000 by gunicorn; to 80 by nginx
CONFIG={'filename':'~/.config/cronvice/cfg.json',
        'history':'~/.config/cronvice/history',
        'services':'~/02_GIT/services/cloud_myservice',
        'interpretter': "~/.venv/myservicenv/bin/python3",
        'screentag':'_CX',
        'quit':False         #
}

#SCREEN_TAG = "_CX"

# --- to save some monkey traversing, keep global info here
ALL_COMMENTS = {}
ALL_PATHS = {}
# just for crons
INSIDE_DTS = {}
# keep info on start() and process.poll() PROCESS[name] [ obj/time/dt ]
PROC_OBJ = {}
#INSIDE_LAST_RUN = {}  notnot
#INSIDE_PROC_OBJ = {} notnot

# HERE I HAVE MYCRON DEFINED!!!!!!!!!!
mycron = CronTab(user=True) #CronTab(user='root')

# ----things that go into cron
MYENV = "DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus"
# INTERPRETTER = "/usr/bin/python3" # I will use CONFIG['venv']
# ............ INTERPRETTER = "~/.venv/myservicenv/bin/python3"

#================================== all global variables are recommended to store here
global_variables_here = None

# object_list = ['df1'] # this will be in `objects`
#================================== all global variables are recommended to store here

CFG_DEBUG = True # I will keep this for config....
#CFG_DEBUG = False
myPromptSession = None
DEBUG = False # I will keep this one for all rest
# ========================================= some general terminal OPS


def get_current_user():
    return getpass.getuser()

def debug_write(msg, place2L="  "):
    now = dt.datetime.now()
    with open(f"/tmp/cronvice_{get_current_user()}.log", "a") as f:
        f.write(f"{now} ... @{place2L} ... {msg}\n")

def get_terminal_columns():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80  # Default fallback width


def move_cursor(y, x):
    """
    for x it doesnt work
    """
    print(f"\033[{y:d};{x:d}H")

#===========================================================
#===========================================================
#===========================================================

def verify_config(filename = ""):
    '''used inside, verification of bak json version'''
    global CONFIG
    if filename != "":
        CONFIG['filename'] = filename
    cfg = CONFIG['filename']
    #if CFG_DEBUG:print("D... verifying config from",cfg)
    ok = False
    try:
        if os.path.isfile( os.path.expanduser(cfg)):
            with open(os.path.expanduser(cfg), "r") as f:
                dicti = json.load(f)
        ok = True
        if CFG_DEBUG:print("D... config verified")
    except:
        if CFG_DEBUG:
            print("D... verification config FAILED")
    return ok

def get_config_file():
    ''' returns the filename where config is stored'''
    global CONFIG
    return CONFIG['filename']
def show_config( cdict=None , filename = ""):
    '''used inside, shows current config dictionary OR other dict'''
    global CONFIG
    if filename != "":
        CONFIG['filename'] = filename
    if cdict==None:
        print( json.dumps(CONFIG, indent=1) )
    else:
        print( json.dumps(cdict, indent=1) )


def cfg_to_bak(filenamebk="", filename = ""):
    '''used inside, rename config (before save)'''
    global CONFIG
    if filename != "":
        CONFIG['filename'] = filename

    cfg = None
    if filenamebk=="":
        cfg = CONFIG['filename']
    else:
        cfg = filenamebk

    cfgbak = cfg + ".bak"
    #print("D... cfg:",cfg)
    #print("D... cfgbak:",cfgbak)
    if CFG_DEBUG:
        print("D... creating a backup config:", cfgbak )
    if not os.path.isfile( os.path.expanduser(cfg)):
        print(f"X... config {cfg} doesnt exist (yet?, OK)")
        return True

    ### rozXXXX
    try:
        os.rename(os.path.expanduser(cfg),
                  os.path.expanduser(cfgbak))
        result = True
    except:
        print("X... couldnt rename old:", cfg,"no bak file created")
        result = False
    return result


def bak_to_cfg(filenamebk="", filename = ""):
    '''used inside, rename back the bak version'''
    global CONFIG
    if filename != "":
        CONFIG['filename'] = filename

    if filenamebk=="":
        cfg = CONFIG['filename']
    else:
        cfg = filenamebk

    cfgbak = cfg + ".bak"
    if CFG_DEBUG:
        print("D... testing if backup config exists:", cfgbak)
    if os.path.isfile( os.path.expanduser(cfgbak)):
        if CFG_DEBUG:
            print("D... BACUP config exists:",cfgbak, "... renaming to:", cfg)
        os.rename(os.path.expanduser(cfgbak),
                  os.path.expanduser(cfg))
        if CFG_DEBUG:print("D... config is recovered from:", cfgbak)
    else:
        if CFG_DEBUG:
            print("D... bak config did not exist:", cfgbak,"no bak file recovery")


def save_config(filenamesv="", filename = ""): # duplicit... filename overrides
    '''FRONT function, save config to filename'''
    global CONFIG
    if filename != "":
        CONFIG['filename'] = filename

    if filenamesv=="":
        cfg = CONFIG['filename']
    else:
        cfg = filenamesv

    if CFG_DEBUG: print("D... calling cfg_to_bak:", cfg)
    if not cfg_to_bak(cfg):
        sys.exit(1)

    if CFG_DEBUG: print("D... writing config:", cfg)

    ### rozxxx
    dir2create = os.path.dirname( cfg )
    #print("D...",dir2create)
    if not os.path.isdir( os.path.expanduser(dir2create )):
        if CFG_DEBUG: print(f"D... trying to create directory {dir2create} if needed")
        result = False
        os.mkdir( os.path.expanduser(dir2create ))

    with open(os.path.expanduser(cfg), "w+") as f:
        f.write(json.dumps(CONFIG, indent=1))
        if CFG_DEBUG:print("D... config was written:", cfg)

    if verify_config(filename):
        if CFG_DEBUG:
            print("D... verified by verify_config ... ok ... ending here")
        return True
    #====ELSE RECOVER BAK
    return bak_to_cfg()



def load_config(filename=""):
    '''FRONT function, load config file'''
    global CONFIG
    if filename != "":
        CONFIG['filename'] = filename
    cfg = CONFIG['filename']
    cfg = cfg+".from_memory"
    if CFG_DEBUG:
        print("D... calling save_config:")
    save_config( cfg )

    cfg = CONFIG['filename']
    if CFG_DEBUG:print("D... loading config from",cfg)

    if not verify_config(filename):
        print("X... FAILED on verifications")
        return False

    if CFG_DEBUG:
        print("D... passed verification of:",cfg)
    dicti = CONFIG

    if CFG_DEBUG:
        print("D... directly loading json:",cfg)
    if os.path.isfile( os.path.expanduser(cfg)):
        with open(os.path.expanduser(cfg), "r") as f:
            dicti = json.load(f)

    # rewriting in memory
    if sorted(dicti.keys()) == sorted(CONFIG.keys()):
        if CFG_DEBUG:
            print("D... memory and disk identical:")
    else:
        if CFG_DEBUG:
            print("X... memory and disk differ:")
        # show_config(CONFIG)
        # there may be more lines in the CODE after upgrade.
        for k in CONFIG.keys(): # search CODE version
            if not (k in dicti.keys()):
                print("D... key not on DISK:", k )
                dicti[k] = CONFIG[k]


    CONFIG = dicti
    if CFG_DEBUG:
        print("D... final CONFIG:")
    #show_config(filename)
    if CFG_DEBUG:
        print("D... end load")


def loadsave(filename = ""):
    '''FRONT function, if DISK is earlier version than CODE, this may update DISK'''
    if filename != "":
        CONFIG['filename'] = filename

    load_config(filename)
    save_config() #?



#==========================================================



def func(debug = False):

    print("D... in unit config function func DEBUG may be filtered")
    print("i... in unit config function func - info")
    print("X... in unit config function func - ALERT")
    return True

def test_func():
    print("i... TESTING function func")
    assert func() == True

if __name__ == "__main__":
    print("i... in the __main__ of config of cronvice")
    Fire()
