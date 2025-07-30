#!/usr/bin/env python3


from cronvice.version import __version__
from fire import Fire
from cronvice import config
import os

import mmap
import time
import sys


MMAPFILE = os.path.expanduser("~/.config/cronvice/mmapfile")
MMAPRESP = os.path.expanduser("~/.config/cronvice/mmapresponse")
MMAPSIZE = 1000
NULLCHAR = chr(127)
# -------------------------------------------------------------------------

def mmcreate(filename=MMAPFILE):
    # - to have different filenames on the same PC
    #PORT=config.CONFIG['netport']
    #filename = f"{filename}{PORT}"

    DIR = os.path.dirname( os.path.expanduser(filename ))
    if not os.path.exists(DIR):
        os.mkdir(DIR)

    with open( os.path.expanduser(filename), "w") as f:
        f.write(NULLCHAR*MMAPSIZE)


def mmwrite(text, filename = MMAPFILE):
    """
    write text to filename
    """
    #PORT=config.CONFIG['netport']
    #filename = f"{filename}{PORT}"

    if not os.path.exists(filename):
        print(f"W...  creating {filename}")
        mmcreate(filename)
    else:
        file_size = os.path.getsize( filename )
        if file_size!=MMAPSIZE:
            print(f"X... File Size IS== {file_size}, should be {MMAPSIZE} ")
            sys.exit(0)

    with open(filename, mode="r+", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE, offset=0) as mmap_obj:
            # print(" WRITING: ",text)
            put = str(text).encode("utf8")
            mmap_obj.write( put)
            mmap_obj.write( str(NULLCHAR*(MMAPSIZE-len(put)) ).encode("utf8") )  # 2ms
            mmap_obj.flush()





# -------------------------------------------------------------------------

def mmread(filename = MMAPFILE):
    """
TO DEBUG ONLY
    """

    #PORT=config.CONFIG['netport']
    #filename = f"{filename}{PORT}"

    print("... MMREAD FROM",filename)
    #print(filename)
    #print(filename)
    #print(filename)
    #print(filename)
#    with open(filename, mode="r", encoding="utf8") as file_obj:
#        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
#            text = mmap_obj.read()
#            print("READTEXT =",text)

    with open(filename, mode="r+", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE, offset=0) as mmap_obj:
            text = mmap_obj.read().decode("utf8").strip().strip(NULLCHAR)
            print(text)
            print(text)
            print(text)
            print(text)
            return text



def mmread_n_clear(  filename = MMAPFILE ):
    """
    read and clear  filename
    """

    #PORT=config.CONFIG['netport']
    #filename = f"{filename}{PORT}"

    # print("D... MMRC")
    if os.path.exists(filename):
        file_size = os.path.getsize( filename )
        if int(file_size) != int(MMAPSIZE):
            print(f"! File Size == {file_size}, should be {MMAPSIZE}")
            print(f"! File Size == {file_size}, should be {MMAPSIZE}")
            print(f"! File Size == {file_size}, should be {MMAPSIZE}")
            print(f"! File Size == {file_size}, should be {MMAPSIZE}")
            print(f"! File Size == {file_size}, should be {MMAPSIZE}")
            os.remove( filename )
            #sys.exit(0)
            mmcreate( filename )

    if not os.path.exists(filename):
        print( f"xxxxxx ... {filename} not found... creating","1")
        mmcreate( filename)
        #return  "xxxxxx","1"


    with open(filename, mode="r+", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE, offset=0) as mmap_obj:
            text = mmap_obj.read().decode("utf8").strip()
            # print("READTEXT: ",text)


            # execute(text.decode("utf8"))
            if text[0] == NULLCHAR:
                response = ""#"xxxxxx","1"
                #return response
            elif NULLCHAR in text:  # take everything before "*"
                response = text.split(NULLCHAR)[0]
                response = response+"\n" # BREAKING FLASHCAM SYSTEM
                # if len(response.split())>1:
                #     spl01 = response.split()[0].strip()
                #     spl02 = " ".join(response.split()[1:])
                #     spl02 = spl02.strip()
                #     response = f"{spl01}",f"{spl02}"
                #     print("i... mmapread'nclear returning ", response)
                # else:
                #     response = "xxxxxx","1"
            else:
                response = "xxxxxx","1"

                # print("i... mmapread'nclear returning ", response)
                # print("i... mmapread'nclear returning ", response)

            text = NULLCHAR*999
            # print("CLEARING: ",text)

            mmap_obj[:MMAPSIZE] = str(NULLCHAR*MMAPSIZE).encode("utf8")
            mmap_obj[:len(text)] = str(text).encode("utf8")
            mmap_obj.flush()
            return response
    return ""
# -------------------------------------------------------------------------

if __name__ == "__main__":
    Fire( mmwrite )
    #print("... sleeping 2")
    #time.sleep(2)
