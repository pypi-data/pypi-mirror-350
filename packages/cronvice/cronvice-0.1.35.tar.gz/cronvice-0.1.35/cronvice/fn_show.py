#!/usr/bin/env python3
"""
 These modules should contain one function each...


"""

from fire import Fire
from console import fg,bg
from cronvice import config
from cronvice import objects

KNOWN_COMMANDS_LOCAL_TYPE = "OBJ"

def main(*args,**kwargs):
    #print(f"{fg.dimgray}D... main() @fn_lo: args/kwargs.../{args}/{kwargs}/{fg.default}")
    #print(f"D... main() @fn_show: args/kwargs.../{args}/{kwargs}/")
    if len(args)==0:
        print("D...  give me an object: allowed objects:",objects.get_objects_list_names() )
        return
    oname = args[0]
    if objects.object_exists(oname):
        print(f"{fg.green}i... showing {oname}{fg.default}")
        obj = objects.get_object( oname )
        print(f"    filename: {obj.src_filename}")
        print(f"    basename: {obj.src_basename}")
        print(f"    path    : {obj.src_path}")
        print(f"    type    : {obj.typ}")
        #if obj.started is not None:
        print(f"    started : {obj.started}")
        #if obj.elements is not None:
        print(f"    elements: {obj.elements:,d}")
        #if obj.comment is not None:
        print(f"    comment : {obj.comment}")
    else:
        print(f"i... {fg.red} NOT showing {oname}{fg.default}")


if __name__=="__main__":
    Fire(main)
