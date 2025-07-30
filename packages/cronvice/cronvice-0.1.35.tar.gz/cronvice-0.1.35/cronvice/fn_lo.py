#!/usr/bin/env python3
"""
 These modules should contain one function each...
ls for the objects...

"""

from fire import Fire
from console import fg,bg
from cronvice import config
from cronvice import objects

KNOWN_COMMANDS_LOCAL_TYPE = "OTHER"

def main(*args,**kwargs):
    #print(f"{fg.dimgray}D... main() @fn_lo: args/kwargs.../{args}/{kwargs}/{fg.default}")
    #print( objects.get_objects_list() )
    objects.list_objects()
    #print("D... lo ends here")

if __name__=="__main__":
    Fire(main)
