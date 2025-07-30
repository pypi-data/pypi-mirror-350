#!/usr/bin/env python3

# from {proj}.version import __version__
import time
import datetime as dt
import os
from fire import Fire
import pytermgui # import  report_cursor, save_cursor, restore_cursor
from cronvice import config
# import threading  # for key input

from console import fg, bg, fx
import socket
import hashlib
# theight= terminal.height
# twidth= terminal.width

global_mode = " "

    #==================================================================
    #
    #------------------------------------------------------------------

def get_hostname():
    return socket.gethostname()

    #==================================================================
    #
    #------------------------------------------------------------------

def get_deterministic_index():
    termcodes = {}
    termcodes["slateblue"] = 62
    termcodes["brown"] = 124
    termcodes["purple"] = 5
    termcodes["darkcyan"] = 30
    termcodes["cadetblue"] = 73
    termcodes["darkslateblue"] = 60
    termcodes["darkgreen"] = 22
    termcodes["sienna"] = 130
    termcodes["indianred"] = 167
    termcodes["seagreen"] = 29
    hostname = socket.gethostname()
    hash_value = hashlib.sha256(hostname.encode()).hexdigest()[0:8]
    #print(hash_value)
    index = int(hash_value, 16) % len(termcodes)  # Get deterministic index
    #print("index", index)
    return index # int(hash_value, 16) % 10

    #==================================================================
    #
    #------------------------------------------------------------------

def get_deterministic_color_term():
    """
    This is consistent with bash script in tjkirchmod2 !!!!
    #https://www.w3.org/TR/css-color-3/#svg-color

    """
    termcodes = {}
    termcodes["slateblue"] = 62
    termcodes["brown"] = 124
    termcodes["purple"] = 5
    termcodes["darkcyan"] = 30
    termcodes["cadetblue"] = 73
    termcodes["darkslateblue"] = 60
    termcodes["darkgreen"] = 22
    termcodes["sienna"] = 130
    termcodes["indianred"] = 167
    termcodes["seagreen"] = 29

    hostname = socket.gethostname()
    hash_value = hashlib.sha256(hostname.encode()).hexdigest()[0:8]
    print(hash_value)
    index = int(hash_value, 16) % len(termcodes)  # Get deterministic index
    print("index", index)
    color_name = list(termcodes.keys())[index]  # Map index to a color name
    return termcodes[color_name]  # Return the xterm-256 color index


    #==================================================================
    #
    #------------------------------------------------------------------

class TopBar:
    """
    allows to define top bar(s) and keep printing them
    """

    host_colors =  [ bg.slateblue,   bg.brown, bg.purple,   bg.darkcyan, bg.cadetblue, bg.darkslateblue, bg.darkgreen,  bg.sienna,  bg.indianred, bg.seagreen]
    # not used, just in findcolor
    cocodes = {}
    cocodes["slateblue"] = "#6A5ACD"
    cocodes["brown"] = "#A52A2A"
    cocodes["purple"] = "#800080"
    cocodes["darkcyan"] = "#008B8B"
    cocodes["cadetblue"] = "#5F9EA0"
    cocodes["darkslateblue"] = "#483D8B"
    cocodes["darkgreen"] = "#006400"
    cocodes["sienna"] = "#A0522D"
    cocodes["indianred"] = "#CD5C5C"
    cocodes["seagreen"] = "#2E8B57"


    #==================================================================
    #
    #------------------------------------------------------------------

    def __init__(self, pos=1, bgcolor="auto"):
        self.pos = pos # bar number 1 (most top) or more
        self.elements = {}
        self.twidth = 80 # terminal width online
        #self.positions = {}
        self.t2 = None
        if bgcolor is None:
            self.BCOL = bg.blue
        elif bgcolor == "auto":
            i = get_deterministic_index()
            self.BCOL = self.host_colors[i]
        else:
            self.BCOL = bgcolor

    #==================================================================
    #
    #------------------------------------------------------------------

    @classmethod
    def get_colors(cls):
        return cls.host_colors

        # self.t = threading.currentThread()

        # try:
        #     pass
        #     # print("report_cursor to appear")
        #     # print( "i... topbar: pos/cursor",pos  )
        #     report_cursor()
        #     # print("report done")
        # except:
        #     print("X... problem with report_cursor")
        # # print("i... topbar bar started")

    #==================================================================
    #
    #------------------------------------------------------------------

    def add_bar(self, two=2, bgcolor=bg.blue):
        """
        create second bar
        """
        if two == 2:
            self.t2 = TopBar(two, bgcolor=bgcolor)
        else:
            print("X... nobody wanted more than two......  NOT OK")
        return self.t2

    #==================================================================
    #
    #------------------------------------------------------------------

    def add_element(self, name, x, length, text, style):
        """
        insert into the bar, x is x coordinate, no tuple anymore; tup<0 is from right
        """
        xp = 1
        if isinstance(x,int):
            xp = x
        else:
            print("X... only  int in the TOPBAR  for position")
            sys.exit(1)
        if type(text) != str:
            print("X... display string only")
            sys.exit(1)
        #self.positions[x] = s # coordinate has text
        self.elements[name] = [ x, length, text, style] # x coordinate  ; text  text
        #print(self.elements.keys() )

    def update_element(self, name, text, style=None):
        if name in self.elements:
            x = self.elements[name][0]
            length = self.elements[name][1]
            style1 = self.elements[name][3]
            if style is not None:
                style1 = style
            self.elements[name] = [ x, length, text, style1] # x coordinate  ; text  text


    #==================================================================
    #
    #------------------------------------------------------------------
    def prepare_element(self, eledict):
        """
        prepare elements list and size, always 3x default @end
        """
        x0 = eledict[0]
        length = eledict[1]
        text = eledict[2]
        style = eledict[3]
        #
        if len(text) > length:
            text = text[:length]
        elif len(text) < length:
            if x0 < 0:
                text = text.rjust(length)
            else:
                text = text.ljust(length)
        text = f"{self.BCOL}{style}{text}{bg.default}{fx.default}{fg.default}"
        if x0 < 0:
            x0 = self.twidth - abs(x0) + 1
            #if x0 + length > self.twidth:
            #    text = text[: self.twidth - x0 - length]
        if x0 < 0:
            x0 = 1
        return x0, text


    #==================================================================
    #
    #------------------------------------------------------------------

    def place(self):
        """
        Place the TOPBAR on screen
        """
        # curs = (-1, -1)
        #twidth = os.get_terminal_size().columns
        self.twidth = config.get_terminal_columns() # os.get_terminal_size().columns
        #print(twidth)

        if self.pos == 1:
            pytermgui.save_cursor()

        # do background first -------------------------------
        pytermgui.print_to( (1, self.pos), f"{self.BCOL}" + " " * self.twidth + bg.default) # paint default BG
        pytermgui.print_to( (1, self.pos + 1), " " * self.twidth)

        # --------------------------------------------------------------------------------
        #
        for k in self.elements.keys():
            x0, text = self.prepare_element( self.elements[k]  )
            pytermgui.print_to(   ( x0, self.pos), text )

        if self.t2 is not None:
            self.t2.place()

        if self.pos == 1:
            pytermgui.restore_cursor()
            print("", end="\r")  # this make GOOD thing in printing



# #################################################################################3
#
#
#
# ------------------------------------------------------------------------------------
def main():
    """
    print an example top bar
    """

    # BOTH
    # bg.cadetblue  bg.steelblue bg.darkgreen, bg.olive
    # bg.steelblue, is too close
    print("\n\n showing some  bar colors ..... \n\n")
    for c in [ bg.navy, bg.steelblue]:
        print(fg.white, c, "        SEE an example of a top bar  -  ",fg.black, "kill with  Ctrl-c     ", bg. default)


    print()
    print(fg.white, "with  WHITE-and-BLACK LETTERS I have now :  ***10***  useful colors !") # bg.olive,

    for c in TopBar.get_colors():
        print(fg.white, c, "        SEE an example of a top bar  -  ",fg.black, "kill with  Ctrl-c     ", bg. default, fg.default)

    # print(fg.white, "with  BLACK LETTERS")
    # for c in [  bg.orange, bg.khaki, bg.burlywood, bg.aquamarine, bg.sandybrown, bg.tomato, bg.salmon, bg.lightcoral,]:
    #     print(fg.black, c, "        SEE an example of a top bar  -  ",fg.white, "kill with  Ctrl-c     ", bg. default)

    #time.sleep(3)
    print("-------------------------------------------")
    print(" #       add_element( NAME, x (positive or negative),  length,   TEXT, tyle  ) ")
    print(" #       update_element( NAME,  TEXT  ) ")
    print()
    t = TopBar(1)
    t.add_element("time", 11,10 + 12, str(dt.datetime.now())[:-4], fg.white + fx.bold)
    t.add_element("host", -10,10, get_hostname(), bg.orange + fx.bold + fg.blue)
    #
    print("\n\n  see the bar running for 33 seconds \n\n")
    for i in range(100):
        #
        # DO whatever stuff and PLACE PRINTTO SLEEP
        #
        t.place()
        t.update_element("time", str(dt.datetime.now())[:-4] )
        #t.update_element("host", get_hostname() )
        time.sleep(0.3)



if __name__ == "__main__":
    Fire(main)
    #Fire({"termcolor":get_deterministic_color_term,       "m":  main})
    #Fire(get_deterministic_color_term)
