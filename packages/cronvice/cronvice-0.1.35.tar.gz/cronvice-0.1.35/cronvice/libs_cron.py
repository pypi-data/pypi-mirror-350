#!/usr/bin/env python3
from fire import Fire
from crontab import CronTab  # install python-crontab
from console import fg, bg
import shutil
import os
import datetime as dt
import shlex
import subprocess as sp
from cronvice import libs_screen
from cronvice import config
from cronvice.config import mycron
import time
import sys



#=========================================================================
#
#-------------------------------------------------------------------------

def reschedule_to_1m(tag, every="1m"):
    """
    """
    print("D... deleting job first", tag)
    del_job(tag) # ment to remove 31.2. job
    print(f"D... adding job second: tag== {tag}  for every /{every}/")
    add_job(tag, every)



#=========================================================================
#
#-------------------------------------------------------------------------

def set_to_never(tag):
    """
    """
    ACT = False
    #file_path = os.path.abspath(__file__)
    file_path = os.path.abspath(sys.modules['__main__'].__file__)

    # RMTG = f"screen -dmS {tag} " #SPACE IMPORTANT
    RMTG = f"{file_path}"
    for job in config.mycron:
        #print(f"/{job.command}/..")
        if job.command.find(RMTG) > 0 and job.command.endswith(f" r {tag}") > 0: # no space
            print(f"i... setting to never /{RMTG}/{tag}/ ")#... {job}")
            #config.mycron.remove(job)
            #config.mycron.remove(job)
            job.day.on(31)
            job.hour.on(23)
            job.minute.on(59)
            job.month.on('FEB')
            ACT = True
    if ACT:
        config.mycron.write()
    else:
        print("X... nothing set")

#=========================================================================
#
#-------------------------------------------------------------------------

def just_list_cron( running=None):
    """
    aas it says. But I like to have clean list....
    """
    env = os.environ.copy()
    CMD = "crontab -l"
    args = shlex.split(CMD)
    # CRASH ON NO CRONTAB DEFINED
    ok = False
    ret = ""
    try:
        ret = sp.check_output(args)#Popen(args, env=env, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
        ok = True
    except:
        pass
    if not ok:
        print("X... no crontab")
        return
    ret = ret.decode("utf8").strip().split("\n")
    ret = [ x.strip() for x in ret if str(x).find("#") != 0 ]
    ret = [ x.strip() for x in ret if len(str(x).strip(" ")) != 0  ]
    #

    #print(running)
    for i in ret:
        #process.poll()
        j = i.split(" ")
        # split time and command and comment
        tima = "_".join(j[:5])
        txta = " ".join(j[5:]).split("#")[0]
        # clean long commands
        txta = txta.replace("DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus", "")
        # this is not going to be used anymore
        txta = txta.replace("/usr/bin/python3", "").strip(" ")
        txtb = " ".join(j[5:]).split("#")[-1]
        # print
        tag = fg.default
        if running is not None and txta.split()[2] in running:
            tag = fg.green
        print(f" {tag}{tima:16s} {txta:50s} # {txtb} ", fg.default)



#=========================================================================
#
#-------------------------------------------------------------------------

def just_showlist_cron():
    """
    aas it says
    """
    env = os.environ.copy()
    CMD = "crontab -l"
    args = shlex.split(CMD)
    ret = sp.check_output(args)#Popen(args, env=env, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    ret = ret.decode("utf8").strip().split("\n")
    ret = [ x.strip() for x in ret if str(x).find("#") != 0 ]
    #for i in ret:
    #    #process.poll()
    #    print(i)
    crfile = f"/tmp/crontablinst_{config.get_current_user()}"
    with open(crfile, 'w') as f:
        f.write("\n".join(ret))
    CMD = f"cat {crfile}; read"
    if libs_screen.is_session_desktop():
        args = shlex.split(f"xterm -e bash -c '{CMD}'")
        process = sp.Popen(args,  stdout=sp.DEVNULL, stderr=sp.DEVNULL)
        process.poll()
    else:
        args = shlex.split(f"bash -c '{CMD}'")
        res = sp.call(args)



#=========================================================================
#
#-------------------------------------------------------------------------


def remove_fullpath(fullpath, item):
    """
    leave just lastpath/tag
    """
    return item.replace(fullpath + '/', '', 1)

#=========================================================================
#
#-------------------------------------------------------------------------



def get_comment(tag):
    if len(config.ALL_COMMENTS) == 0:
        find_second_level_executables()
    if tag in config.ALL_COMMENTS:
        return config.ALL_COMMENTS[tag]
    else:
        return None


#=========================================================================
#
#-------------------------------------------------------------------------


def fill_current_DTS():
    """
    extract time interval from cron and fill DICT
    use the real installation site of this code todetect!
    """
    #global config.INSIDE_DTS
    mycron.read()
    #config.debug_write(f"Warning:   cron is read len=={len(mycron)} ", "LC")

    file_path = os.path.abspath(sys.modules['__main__'].__file__)
    for job in mycron:
        tag2 = str(job).split(file_path)[-1].strip().split(" ")[1].strip()
        #print( f"{tag2:13s}", ">>>", job.slices)
        config.INSIDE_DTS[tag2] = job.slices
        #if tag2.find("flash") >= 0:
        #    config.debug_write(f"Warning:  flash {config.INSIDE_DTS[tag2]} ", "LC")
    #print(dt.datetime.now())

#=========================================================================
#
#-------------------------------------------------------------------------


def get_DT(tag):
    """
    extract time interval from cron
    """
    #if len(config.INSIDE_DTS) == 0:
    #fill_current_DTS()
    #global config.INSIDE_DTS
    if not tag in config.INSIDE_DTS:
        print(f"X... no cron data for this site-code")
        print(f"X... unknown tag {tag} for DT column:", config.INSIDE_DTS.keys())
        return None
    DT = str(config.INSIDE_DTS[tag]).strip().split(" ")
    res = ""
    if DT[0] == "*":
        pass #res = f"{res} 0m"
    else:
        res = f"{res} {DT[0]}m"

    if DT[1] == "*":
        pass #res = f"{res} 0h"
    else:
        res = f"{res} {DT[1]}h"

    if DT[2] == "*":
        pass #res = f"{res} 0d"
    else:
        res = f"{res} {DT[2]}d"

    res = res.replace("*", "").strip()
    if len(res) == 0:
        res = "1m"
    #if tag.find("flash") >= 0:
    #    config.debug_write(f"info...:  flash {config.INSIDE_DTS[tag]} # {res}", "LC")
    return res


#=========================================================================
#
#-------------------------------------------------------------------------


def get_fullpath(tag):
    if len(config.ALL_PATHS) == 0:
        find_second_level_executables()
    if tag in config.ALL_PATHS:
        return config.ALL_PATHS[tag]
    else:
        return None


#=========================================================================
#
#-------------------------------------------------------------------------


def extract_one_comment(file_path):
    #print("D... opening", file_path)
    with open(file_path) as f:
        shebang = f.readline().strip()
        #print("D... shebang == ", shebang)
        if shebang.find("#") == 0:
            comment = f.readline().strip()
            #print("D... comment == ", comment)
            if comment.find("#") == 0:
                return comment
            else:
                return None
        else:
            return None


#=========================================================================
#
#-------------------------------------------------------------------------


def find_second_level_executables():
    """
    parse all execs in second level of directory
    """
    directory = config.CONFIG['services']
    directory = os.path.expanduser(directory)

    config.debug_write('parsing SECOND.LEVEL=services', "CR")
    #with open("/tmp/cronvice.log", "a") as f:
    #    f.write(f"i... {dt.datetime.now()} ... in find_second_level ... services is @ {directory} \n")

    if not os.path.exists(directory):
        print("X... configuration of services' directory is incorrect")
        print("X... BAD DIRECTORY", directory)
        print("X... SEE CONFIG AT", config.CONFIG['filename'] )
        sys.exit(1)

    executables = []
    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        if os.path.isdir(subdir_path):
            for file in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, file)
                if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                    executables.append(file_path)
                    tag = file_path.split("/")[-1] # TAG
                    COM = extract_one_comment(file_path)
                    config.ALL_COMMENTS[tag] = COM
                    config.ALL_PATHS[tag] = file_path
    return executables

#=========================================================================
#
#-------------------------------------------------------------------------

def list_services2():
    """
    return  just folder/exec LIST
    """
    exelist = find_second_level_executables()
    fullp = os.path.expanduser(config.CONFIG['services'])
    #print(exelist)
    cut = []
    for i in exelist:
        cut.append( remove_fullpath(fullp, i) )
    return cut

#=========================================================================
#
#-------------------------------------------------------------------------

def list_services1():
    """
    return just exec LIST
    """
    cut = list_services2()
    cut = [ i.split("/")[-1] for i in cut]
    duplicates = [item for item in set(cut) if cut.count(item) > 1]
    if len(duplicates) > 0:
        print(bg.red, fg.white, "X... duplicate filenames: ", duplicates, fg.default, bg.default)
    return cut


#=========================================================================
#
#-------------------------------------------------------------------------


def is_in_allowed(tag):
    """
    is the tag in allowed-list ?
    """
    if tag in list_services1():
        return True
    else:
        return False

#=========================================================================
#
#-------------------------------------------------------------------------
#

def get_now():
    res = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    return res


#=========================================================================
#
#-------------------------------------------------------------------------
#

def list_crons( ):
    """
    just list crons that contain MYENV - the last word is the REALNAME
    """
    global mycron
    alist = []
    for job in mycron:
        sjob = str(job)
        #print(type(sjob))
        if sjob.find(config.MYENV) > 0:
            name = sjob.split(config.MYENV)[-1]
            if "#" in name:
                name = name.split("#")[0].strip()
            name = name.split(" ")[-1]
            #print(sjob, name)
            alist.append(name)
    return alist
#=========================================================================
#
#-------------------------------------------------------------------------
#

def allocate( exe):
    """
    use which , find location of exe, return complete path
    """
    config.debug_write(f"ALLOCATE ... the exe is {exe}", "CR")

    #with open("/tmp/cronvice.log", "a") as f:
    #    f.write(f"i... in ALLOCATE ... the exe is {exe} \n")

    if os.path.exists( exe): # This is total path
        #with open("/tmp/cronvice.log", "a") as f:
        #    f.write(f"i... ret  ... the exe is {exe} \n")
        return exe

    # try to find it ith which
    program_path = shutil.which( exe )
    config.debug_write(f"shutil result is {program_path}", "CR")

    #with open("/tmp/cronvice.log", "a") as f:
    #    f.write(f"i... ret  ... the shutil result is {program_path} \n")

    # try some other locations
    if program_path is None:
        config.debug_write(f"Progpath NONE", "CR")
        #with open("/tmp/cronvice.log", "a") as f:
        #    f.write(f"i... ppath was None  \n")
        home_dir = os.environ.get('HOME')
        #with open("/tmp/cronvice.log", "a") as f:
        #    f.write(f"i... return  ... 1a homedir: {home_dir} \n")
        file_path = os.path.join(home_dir, '.local', 'bin', exe)
        #with open("/tmp/cronvice.log", "a") as f:
        #    f.write(f"i... return  ... 1a  joined {home_dir} - {file_path} \n")
        if os.path.exists(file_path):
            #with open("/tmp/cronvice.log", "a") as f:
            #    f.write(f"i... return  ... 1 {file_path} \n")
            config.debug_write(f"ret {file_path}", "CR")

            return file_path

    # try some other locations
    if program_path is None:
        home_dir = os.environ.get('HOME')
        file_path = os.path.join(home_dir, 'bin', exe)
        if os.path.exists(file_path):
            config.debug_write(f"ret2 {file_path}", "CR")

            #with open("/tmp/cronvice.log", "a") as f:
            #    f.write(f"i... return  ... 2 {file_path} \n")
            return file_path

    return program_path # wil do None eventually


#=========================================================================
#
#-------------------------------------------------------------------------
#

def view_cron( short=False):
    global mycron
    SCRDMS = f"/usr/bin/screen -dmS " #SPACE IS IMPORANT
    sessions = libs_screen.list_screen_sessions() # PREPARE
    #print(sessions)
    for job in mycron:
        txt = job.command
        if txt[0] == "#": continue
        if short:
            if txt.find(SCRDMS) > 0:
                ATAG = txt.split(SCRDMS )[1].split()[0]
                BCMD = " ".join(txt.split(SCRDMS )[1].split()[1:])

                IIS = is_in_screen(ATAG, sessions)
                if IIS:
                    col = f"{fg.green}* "
                else:
                    col = f"{fg.red}x "
                print( f" {col}{ATAG:12s}{fg.default} - {BCMD}" )
            #else:
            #    print(" - ")
        else:
            print(txt)


#=========================================================================
#
#-------------------------------------------------------------------------
#

def is_in_cron(cron, tag):
    """
    Not usefull with  cronvice in  crontab
    """

    #file_path = os.path.abspath(__file__)
    file_path = os.path.abspath(sys.modules['__main__'].__file__)

    RMTG = f"{file_path}"
    for job in cron:
        if job.command.find(RMTG) > 0 and job.command.endswith(f" r {tag}") > 0: # no SPACE
            return True
    return False


#=========================================================================
#
#-------------------------------------------------------------------------
#

def del_job(  tag): #REAL
    """
    delete with the screen
    """
    ACT = False
    #file_path = os.path.abspath(__file__)
    file_path = os.path.abspath(sys.modules['__main__'].__file__)

    # RMTG = f"screen -dmS {tag} " #SPACE IMPORTANT
    RMTG = f"{file_path}"
    for job in config.mycron:
        #print(f"/{job.command}/..")
        if job.command.find(RMTG) > 0 and job.command.endswith(f" r {tag}") > 0: # no space
            print(f"i... removing /{RMTG}/{tag}/ ")#... {job}")
            config.mycron.remove(job)
            ACT = True
    if ACT:
        config.mycron.write()
    else:
        print("X... nothing deleted")



#=========================================================================
#
#-------------------------------------------------------------------------
#

# def add_job_anycommand( cron, tag):
#     """
#     first attempt to add any command, basically
#     """

#     if is_in_cron(cron, tag):
#         print(f"X... already present {tag}")
#         return
#     ENV = config.MYENV #"DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus"
#     SCR = f"/usr/bin/screen -dmS {tag} " #SPACE IS IMPORANT
#     #make code sequence with &&
#     #CODE = f"echo i...running {tag} && /home/ojr/.local/bin/notifator b hello_{tag} && echo i...running {tag} && sleep 30"
#     MAINCODE = 'notifator'
#     MAINCODE = allocate(MAINCODE)
#     CODE = f"{MAINCODE} b hello_{tag}_{get_now()} && sleep 30"
#     # encapsulate to ''
#     CODE = f"bash -c '{CODE}'"
#     CMD = f"{ENV} {SCR} {CODE}"


#     print("i... adding job", tag)

#     job = cron.new(command=CMD)
#     job.minute.every(1)
#     #job.set_command("new_script.sh")
#     job.set_comment("test of notifator")
#     cron.write()




#=========================================================================
#
#-------------------------------------------------------------------------
#


def is_int(n):
    if str(n).find(".")>=0:  return False
    if n is None:return False
    try:
        float_n = float(n)
        int_n = int(float_n)
    except ValueError:
        return False
    else:
        return float_n == int_n



def add_job(  tag, every="1m"): #REAL
    """
    cron:  * * * * * display dbus python3 path/to/cronvice!!! r  tag
    """
    if is_in_cron(config.mycron, tag):
        print(f"X... already present {tag}")
        return

    if not is_in_allowed(tag):
        print(f"X... this job is not allowed {tag}")
        return


    ENV = config.MYENV #"DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus"

    #file_path = os.path.abspath(__file__)
    file_path = os.path.abspath(sys.modules['__main__'].__file__)

    #return

    #SCR = f"/usr/bin/screen -dmS {tag} " #SPACE IS IMPORANT
    ###make code sequence with &&

    #MAINCODE = 'notifator'
    #MAINCODE = allocate(MAINCODE)
    MAINCODE = file_path
    INTERPRETTER = config.CONFIG['interpretter']
    # with uv not this ................ ------------------------ VENV
    CODE = ""
    #INTERPRETTER = "~/.venv/myservicenv/bin/python3"
    INTERPRETTER = os.path.expanduser(INTERPRETTER)
    if os.path.exists(INTERPRETTER):
        CODE = f"{INTERPRETTER} {MAINCODE} r {tag}"
    else:
        CODE = f"{MAINCODE} r {tag}"
    # ************************* doesnt work, I must activate the envirohnment ****
    # ************************* doesnt work, I must activate the envirohnment ****
    # ************************* doesnt work, I must activate the envirohnment ****
    CODE = f"{MAINCODE} r {tag}"
    # ----------------------------------------------------------
    #### encapsulate to ''
    #CODE = f"bash -c '{CODE}'"
    #CMD = f"{ENV} {SCR} {CODE}"
    CMD = f"{ENV} {CODE}"

    print("i... adding job", tag)

    job =config.mycron.new(command=CMD)

    length = "".join(every[0:-1])
    print(f"D...   int==/{length}/  char==/{every[-1]}/")
    if is_int(length):
        length = int(length)
    else:
        length = 1


    if every[-1] == "m":
        print("i... minute")
        job.minute.every(length)
    elif every[-1] == "h":
        print("i... hour")
        if length == 1:
            job.minute.every(59)
        else:
            job.hour.every(length)
    elif every[-1] == "d":
        if length == 1:
            print("i... day")
            job.hour.every(23)
            job.minute.every(59)
        else:
            job.day.every(length)
    else:
        print("X... unknown time unit for cron /m-h-d/ :", every)
        return
    #job.set_command("new_script.sh")
    job.set_comment("cronvice job")
    config.mycron.write()


#=========================================================================
#
#-------------------------------------------------------------------------
#

def see_job(  tag):
    """
    xxxxxxxxx empty check NOT USED!!!!!!!!!!!!!!!!
    """
    if is_in_cron(config.mycron, tag):
        print(f"X... already present {tag}")
        return
    if not is_in_allowed(tag):
        print(f"X... this job is not allowed {tag}")
        return
    ENV = config.MYENV #"DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus"

    #file_path = os.path.abspath(__file__)
    file_path = os.path.abspath(sys.modules['__main__'].__file__)

    MAINCODE = file_path
    #INTERPRETTER = config.INTERPRETTER

    INTERPRETTER = config.CONFIG['interpretter']
    # with uv not this ................ ------------------------ VENV
    #INTERPRETTER = "~/.venv/myservicenv/bin/python3"
    INTERPRETTER = os.path.expanduser(INTERPRETTER)
    if os.path.exists(INTERPRETTER):
        CODE = f"{INTERPRETTER} {MAINCODE} r {tag}"
    else:
        CODE = f"{MAINCODE} r {tag}"
    ####### encapsulate to ''
    ###CODE = f"bash -c '{CODE}'"
    ###CMD = f"{ENV} {SCR} {CODE}"
    #CMD = f"{ENV} {CODE}"

    #print("i... adding job", tag)
    print(CMD)
    #job =config.mycron.new(command=CMD)
    #job.minute.every(1)
    ####job.set_command("new_script.sh")
    #job.set_comment("test of notifator")
    #config.mycron.write()




#=========================================================================
#
#-------------------------------------------------------------------------
#
########################################################################

def start(tag, duotag): #REAL
    """
    starts screen in BG with environment...... ;  Screen Tag Added
    """
    config.debug_write(f'start TAG="{tag}" -------------------> "START"', "CR")

    #with open("/tmp/cronvice.log", "a") as f:
    #    f.write(f"i... in START ... the tag is {tag} \n")
    #ENV = "DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus"
    ENV = ""
    # Set environment variables
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    env["DBUS_SESSION_BUS_ADDRESS"] = "unix:path=/run/user/1000/bus"

    SCR = f"/usr/bin/screen -dmS {tag}{config.CONFIG['screentag']} " #SPACE IS IMPORANT
    ################################## ENV SCR and CODE ###############################
    #make code sequence with &&

    #MAINCODE = 'notifator'
    #with open("/tmp/cronvice.log", "a") as f:
    #    f.write(f"i... in START ... the main is {MAINCODE} \n")
    #
    #MAINCODE = allocate(MAINCODE)

    MAINCODE = f"{os.path.expanduser(config.CONFIG['services'])}/{duotag}"
    EXECUDIR = MAINCODE.split("/")[:-1]
    EXECUDIR = "/".join(EXECUDIR)
    config.debug_write(f"start / {MAINCODE}/", "CR")

    #with open("/tmp/cronvice.log", "a") as f:
    #    f.write(f"i... in START ...   {MAINCODE} \n")
    CODE = f" cd {EXECUDIR} && {MAINCODE}  && sleep 1"
    #CODE = f"{MAINCODE} b hello_{tag}_{get_now()} && sleep 30"
    #####################################################################################
    # encapsulate to ''
    CODE = f"bash -c '{CODE}'"
    CMD = f"{ENV} {SCR} {CODE}"
    args = shlex.split(CMD)
    #print(args)
    #with open("/tmp/cronvice.log", "a") as f:
    #    f.write(f"i... in START ...and... the args is {args} \n")
    #config.INSIDE_LAST_RUN[tag] = dt.datetime.now()
    process = sp.Popen(args, env=env, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    process.poll()
    config.PROC_OBJ[tag] = {}
    config.PROC_OBJ[tag]['obj'] = process
    config.PROC_OBJ[tag]['time'] = dt.datetime.now()
    config.PROC_OBJ[tag]['dt'] = None
    config.debug_write(f"LAUNCHED {config.PROC_OBJ[tag]} ErrCode={process.poll()} ######", "CR")


#=========================================================================
#
#-------------------------------------------------------------------------

def run_job( tag): # REAL
    """
    if it is in cron and screen not running......
    """
    config.debug_write(f'run TAG=="{tag}"    ---------------------->run_job?', "CR")
    #with open("/tmp/cronvice.log", "a") as f:
    #    f.write(f"i... in run_job ...and... the tag is {tag} \n")


    # if I test first if it is running, no need to lookup secondlevelservices
    #config.debug_write(f"Warning: 1", "CR")
    sessions = libs_screen.list_screen_sessions() # PREPARE but NOOrun secondslevelservices too
    print("i... in runjob")
    #config.debug_write(f"Warning: 2", "CR")
    if libs_screen.is_in_screen(tag, sessions):
        #config.debug_write(f"Warning: 3", "CR")

        config.debug_write(f"................................. already running", "CR")
        print(f"X...  {fg.yellow} already running {tag} {fg.default} ")
        return
    else:
        print(f"X...  {fg.green} NOT running {tag} {fg.default} ")


    if is_in_allowed(tag): # this calls secondlevelserices
        #with open("/tmp/cronvice.log", "a") as f:
        #    f.write(f"i... in run_job ...and... # sessions is {len(sessions)} \n")
        config.debug_write(f"run GO for start", "CR")
        print(f"i... {fg.orange} Starting {tag} .... {fg.default}" )
        li2 = list_services2()
        #print(li2)
        for item in li2:
            folder, executable = item.split('/')
            if executable == tag:
                print(folder, item, tag)
                start(tag, item)


#=========================================================================
#
#-------------------------------------------------------------------------
#

def mod_job(cron, tag):
    del_job(cron, tag)
    add_job(cron, tag)

if __name__ == "__main__":
    Fire({"a": add_job,
          "r": run_job,
          "d": del_job
          })
