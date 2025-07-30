#!/usr/bin/env python3
"""
 These modules should contain one function each...

MODIFIY THE original cronvice adding these functions only + editing CONFIG

... they need some common connect point to have common objects:
 1. config ?
  -  yes, but is there possible to do without?
     - ? for the sake of cronvice initial paradigm? or is that ok?

"""

from fire import Fire
from console import fg,bg
from cronvice import config
from cronvice import objects
import os
# I NEED TO UPDATE  -   config.object_list

KNOWN_COMMANDS_LOCAL_TYPE = "FS"

def main(*args,**kwargs):
    #print(f"{fg.dimgray}D... main() @fn_load: args/kwargs.../{args}/{kwargs}/{fg.default}")
    if len(args)==0:
        print(f"X... {fg.red}give me a file as a parameter...{fg.default}")
        return None
    # ===== loading ------*
    fname = args[0]
    print(f"i... {fg.green}loading {fname}{fg.default}")
    if not os.path.exists(fname):
        print("X... {fg.red}doesnt exist...{fg.default}")
        return

    ext = os.path.splitext(fname)[-1]
    #d1 = objects.O_dataframe("dodo")
    #h1 = objects.O_histogram("hoho")
    #print( objects.get_objects_list() )
    # ==============================================
    if ext == ".asc":
        objects.O_dataframe.from_file(fname)
    elif ext == ".txt":
        objects.O_histogram.from_file(fname)
    else:
        print(f"{fg.red}X...  unknown extension /{ext}/ ... not loading {fg.default} ")
    #objects.get_objects_list().append( args[0] )
    objects.list_objects()


if __name__=="__main__":
    Fire(main)
