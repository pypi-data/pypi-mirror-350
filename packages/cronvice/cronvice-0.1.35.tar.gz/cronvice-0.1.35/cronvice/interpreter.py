#!/usr/bin/env python3
"""
  THe goal is to have a general interpretter that:
   - makes some shell actions
   - performs some operations on objects OR file
"""
#
#  I want to use cmd_parser and call the functions with parameters BY "string cmdline parame"" like Fire()
#
#
from fire import Fire
import sys
from cronvice.version import __version__
from cronvice import config
from cronvice.config import  move_cursor
#from cronvice.config import  DEBUG
#
from cronvice import cmd_parser
import os
#
#
#
import subprocess as sp
from console import fg,bg
import glob
import shlex
import re


# =========  all commands are in 2 main groups ===========-----------------
#  1      shell (just pass to shell)
#  2      local - each one needs to have its own module defined  fn_*.py
#-------------------------------------
# ---------------LOCAL COMMANDS ARE IN 2 MAIN GROUPS ==========
#  2a     argument is none OR a FILE
#  2b     argument is an object
# -------------------------------------------------------------
# SHELL COMMANDS with files as parameters (ll is extended here)
KNOWN_COMMANDS_SHELL_FS = ['ls','ll','fdfind','head','tail','cat']
# other shell commands
KNOWN_COMMANDS_SHELL_OTHER = ['ag']
# call functions@fn_modules -  objects as parameters -  must be defined
# KNOWN_COMMANDS_LOCAL = ['lo','show','zoom','unzoom','connect','reset']
KNOWN_COMMANDS_LOCAL_OTHER = ['reset']
#  content of FUNCTIONs -------- fn_.py in the project
#  load  - FS
#  lo
#  print  - OBJ
#  show - OBJ
KNOWN_COMMANDS_LOCAL_OBJ = []# ['show']
# call functions@fn_modules - files as parameters
KNOWN_COMMANDS_LOCAL_FS = []# ['load']
#


def find_known_commands_type(file_path):
    """
    check the fn_py file and find out which type it is  OBJ or FS
    """
    pattern = re.compile(r'^\s*KNOWN_COMMANDS_LOCAL_TYPE\s*=\s*"(FS|OBJ|OTHER)"')
    #print("D...  checking KCLT @ ", file_path)
    with open(file_path, 'r') as file:
        for line in file:
            #if line.find("KNOWN_COMMANDS")>=0: print(" ...       ",line.strip())
            match = pattern.match(line)
            if match:
                return match.group(1) #line.strip()
    return None



# ************************************************************************ running at start!!!!!!!!!
# ************************************************************************ running at start!!!!!!!!!
# ************************************************************************ running at start!!!!!!!!!
# ************************************************************************ running at start!!!!!!!!!
def init_interpretter():
    # ---- good for completions AND ALSO NEW FUNCTIONS!!! in ACTUAL FOLDER
    #---this doesnt work
    if config.DEBUG:
        print("____________________________________________________________________interpretter")
    allfiles = glob.glob("*")

    # ---- AVAILABLE FUCTIONS ----------== COMMANDS == maybe ONLY ONCE PER RUN
    # --- a trick, I look for other local fn_py
    all_pyfiles = cmd_parser.listpy( also_local=True, DEBUG=False)
    for i in all_pyfiles:
        #print("D...   all_pyfiles:",i)
        # if i[:3] == "fn_" and i[-3:]==".py": # Prefix is already defined
        #print("D...  looking for functions:",i)
            #print(i[-3:]==".py")
        name = os.path.basename(i)
        #print(name)
        name = name.lstrip("fn_")
        name = name.rstrip(".py")
        #print(f"A... adding {fg.yellow} {name} {fg.default}")
        res = find_known_commands_type(i)
        if res is None:
            print(f"X... {fg.red} 'KNOWN_COMMANDS_LOCAL_TYPE = ' is missing in {i} {fg.default} ")
            continue
        elif res =="FS":
            KNOWN_COMMANDS_LOCAL_FS.append(name)
        elif res =="OBJ":
            KNOWN_COMMANDS_LOCAL_OBJ.append(name)
        elif res =="OTHER":
            KNOWN_COMMANDS_LOCAL_OTHER.append(name)
        else:
            print(f"X... {fg.red} PROLBEM???  'KNOWN_COMMANDS_LOCAL_TYPE = ' @ {i} {fg.default} ", res)

    if config.DEBUG:
        print("i... Object commands:",KNOWN_COMMANDS_LOCAL_OBJ)
        print("i... File   commands:",KNOWN_COMMANDS_LOCAL_FS)
        print("i... Other  commands:",KNOWN_COMMANDS_LOCAL_OTHER)

     # --------------------------------------------------------
    # update AVAILABLE -  FILES and OBJECTS.
    # --------------------------------------------------------
    #============================================= prepare for completions =======================
    # ============================================================================= summary
    KNOWN_COMMANDS = KNOWN_COMMANDS_SHELL_FS + \
        KNOWN_COMMANDS_SHELL_OTHER + \
        KNOWN_COMMANDS_LOCAL_FS +\
        KNOWN_COMMANDS_LOCAL_OTHER + \
        KNOWN_COMMANDS_LOCAL_OBJ


    # now create nested completion dict  EVERY COMMAND HAS AUTOCOMPLETE
    KNOWN_COMMANDS_DICT = {}
    for i in KNOWN_COMMANDS:
        KNOWN_COMMANDS_DICT[i]=None

    # now create special completion for filemanagement
    #   ??this is created only once when here....need to be moved
    for i in KNOWN_COMMANDS_SHELL_FS+KNOWN_COMMANDS_LOCAL_FS:
        KNOWN_COMMANDS_DICT[i] = {}
        for j in allfiles:
            KNOWN_COMMANDS_DICT[i][j] = None

    #
    # completely useless here, but I keep it for the symetry and keyboard_remote_start
    #
    allobjects =  [] #['obj1']
    # now create special completion for memory OBJECTS
    for i in KNOWN_COMMANDS_LOCAL_OBJ:
        KNOWN_COMMANDS_DICT[i] = {}
        for j in allobjects:
            KNOWN_COMMANDS_DICT[i][j] = None
    #========================================================== completions created...............

    #print(KNOWN_COMMANDS_DICT)



def respond(inp):
    """
    orphaned function.....
    """
    done = False
    while not done:
        res = mmapwr.mmread_n_clear( mmapwr.MMAPRESP ) # read response
        print(f".../{inp}/==/{res}/..")
        if res==inp:
            break
        time.sleep(1)


def exclude(cmd=""):
    """
    certain protection from malicious shell string...
    """
    bad = False
    if cmd.find("&")>=0:  bad = True
    if cmd.find("|")>=0:  bad = True
    if cmd.find("'")>=0:  bad = True
    if cmd.find('$')>=0:  bad = True
    if cmd.find('%')>=0:  bad = True
    if cmd.find('#')>=0:  bad = True
    if cmd.find('!')>=0:  bad = True
    if cmd.find('(')>=0:  bad = True
    if cmd.find(')')>=0:  bad = True
    if cmd.find(';')>=0:  bad = True
    #if cmd.find('"')>=0:  die() # for sed

    if bad:
        print( f"{fg.white}{bg.red}X... not allowed char in {cmd}", fg.default,bg.default)
    return bad


#==========================================================
# this does classically expansion - more files.....
#==========================================================
def interpolate_star( parlis ):
    """
    Full cmd.split() ... only files, not directories; NOT USED
    """
    cmd2 = []
    newcmd = []
    newcmd.append(parlis[0])
    for i in parlis:
        cmd2.append(i)
    for i in range(1,len(cmd2)):
        print(">>>",cmd2[i] )
        if '*' in cmd2[i]:
            for j in glob.glob( cmd2[i] ):
                if not os.path.isdir(j):
                    newcmd.append(j)
        else:
            newcmd.append(cmd2[i])
    return newcmd
#==========================================================
# this does creates iteratoin through *  - more files.....
#==========================================================
def iterate_star( parstring ):
    """
    kw2.... only files, not directories; USED FOR LOCAL_FSl NOTUSED TOOO
    """
    #def replace_wildcard_with_files(string_A):
    parts = shlex.split(parstring)
    expanded_parts = []
    for part in parts:
        if '*' in part:
            expanded_parts.extend(glob.glob(part))
        else:
            expanded_parts.append(part)
    return [' '.join(expanded_parts)]

    # cmd2 = parstring.split()
    # newcmd = []
    # for i in cmd2:
    #     newcmd.append(i)
    #     if '*' in i:
    #         for j in glob.glob( cmd2[i] ):
    #             if not os.path.isdir(j):
    #                 newcmd.append(j)
    #     else:
    #         newcmd.append(cmd2[i])
    # return newcmd

# =========================================================
#   shell (True or False...check it) run of the commands. with some basic protection
# =========================================================
def run_or_die( cmd , debug = False):
    """
    runs shell command. Iterates over * from filesystem
    """
    res = 0
    if exclude(cmd): return
    res = 0
    #print()
    if debug: print("Exe...", cmd)
    cmd2 = cmd.split()
    for i in range(len(cmd2)):
        #print(i, cmd2[i])
        cmd2[i] = cmd2[i].strip('"')
    newcmd = []
    newcmd.append( cmd2[0] )
    for i in range(1,len(cmd2)):
        # print(">>>",cmd2[i] )
        if '*' in cmd2[i]:
            for j in glob.glob( cmd2[i] ):
                newcmd.append(j)
        else:
            newcmd.append(cmd2[i])
    #print(cmd2)
    if debug: print("Exe...",  newcmd)
    try:
        res = sp.check_call( newcmd )#, shell = True)
        if debug: print("ok",res)
    except:
        res =1
        print(f"X... {fg.red} error running /{bg.white}{cmd}{bg.default}/{fg.default}")
    #print()
    #if res != 0: die("")
# =========================================================

def termline(txt):
    #termsize3 = os.get_terminal_size().columns
    termsize3 = config.get_terminal_columns() # os.get_terminal_size().columns

    cont = f"#... ________ {txt} "
    cont = cont + "_"*(termsize3 - len(cont)-2)
    print(f"{fg.orange}{cont}{fg.default}")


# # ==============================================================================================
# # ==============================================================================================
# # ==============================================================================================
# # ==============================================================================================
# def load( spectrum = None):
#     """
#     special case, load
#     """
#     # Your code here
#     print("i... running command load INTERP", spectrum)
#     return f"loaded"

# def connect(dfname, from_=0, to=999999, display=False, savename=None, quest="meo"):
#     # Your code here
#     print("i... running command connect  INTERP")
#     return f"conected"

# def unzoom(dfname, from_=0, to=999999, display=False, savename=None, quest="meo"):
#     # Your code here
#     print("i... running command unzoom  INTERP")
#     return f"unzoomed"

# def zoom(dfname, from_=0, to=999999, display=False, savename=None, quest="meo"):
#     # Your code here
#     print("i... running command zoom  INTERP")
#     return f"zoomed"
# # ==============================================================================================
# # ==============================================================================================
# # ==============================================================================================
# # ==============================================================================================


def main( cmd ):
    listcmd = cmd.split()
    kw1 = listcmd[0] #.split()[0]
    #
    # ======== I need to interpolate * for filesystem
    # if kw1 in KNOWN_COMMANDS_SHELL_FS or kw1 in KNOWN_COMMANDS_LOCAL_FS:
    #     print("D... FS interpol")
    #     listcmd = interpolate_star( listcmd) # only files, not directories
    kw2 = " ".join( listcmd[1:])
    #cmd = f"{kw1} {kw2}"
    #
    termline(cmd)
    match kw1:
        case 'reset':
            #print("RESET:",cmd,"    ")
            os.system("reset")
            move_cursor(3,1)
            return 1
        # attempt to use the interpretter here**********************
        case 'c':
             print(f"Command recognized /{cmd}/ ... connecting table   {list(kw2)} ")
             return 2
        # case 'zoom':
        #     #print("ZOOM:",cmd,"    ")
        #     return 2
        # case 'unzoom':
        #     #print("UNZOOM:",cmd,"    ")
        #     return 2
        # case 'connect':
        #     #print("CONNECT:",cmd,"    ")
        #     return 2
        case _: # =========== DEFAULT == SHELL COMMANDS ==========================
            # ====== SHELL COMMANDS (itteration of * from FS?)

            #if kw1 in KNOWN_COMMANDS_SHELL_OTHER:
            if kw1 in KNOWN_COMMANDS_SHELL_FS or kw1 in KNOWN_COMMANDS_SHELL_OTHER:
                # replace some commands
                if kw1=="ll": cmd = "ls -l "+kw2
                run_or_die(cmd)
                #

            elif kw1 in KNOWN_COMMANDS_LOCAL_OTHER: # zoom, show
                ### full control of cmd_parser ------- object list ----------
                ### func = getattr( cmd_parser, kw1) # WHEN ELSEWHERE
                ### --------- get the function from globals --------------------
                #func =  globals()[kw1] # WHEN HERE
                ### --------- HA! import a module fn_yrname
                func =  cmd_parser.str_func_to_func( kw1 )
                #func = func.main
                res = cmd_parser.call_function_with_command( func , kw2)
                # for i in res: print("RES:",i) # print results
                #

            elif kw1 in KNOWN_COMMANDS_LOCAL_OBJ: # zoom, show
                func =  cmd_parser.str_func_to_func( kw1 )
                res = cmd_parser.call_function_with_command( func , kw2)
                #

            elif kw1 in KNOWN_COMMANDS_LOCAL_FS:  # load
                ### ----- I need to do glob myself and call repetitively -------
                ### I try to import a module =======
                ###
                ### func = getattr( cmd_parser, kw1) # WHEN ELSEWHERE
                ### --------- get the function from globals --------------------
                #func =  globals()[kw1]
                ### --------- HA! import a module fn_yrname
                func =  cmd_parser.str_func_to_func( kw1 )
                # func = func.main
                # kw2_bis = iterate_star( kw2 )
                #for i in kw2_bis:
                res = cmd_parser.call_function_with_command( func , kw2, use_files=True)
                #for i in res: print("RES:",i) # print results

            else:
                print(f"{fg.red}X... unknown command /{cmd}/    {fg.default}")
            print("."*70)
            return 0   # 0 is the default case if x is not found
    pass
    #print()

if __name__=="__main__":
    Fire(main)
