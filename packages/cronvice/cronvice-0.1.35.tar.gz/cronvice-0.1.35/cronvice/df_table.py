#!/usr/bin/env python3

# to override print <= can be a big problem with exceptions
# from __future__ import print_function # must be 1st
# import builtins

# import sys

from fire import Fire

# from cronvice.version import __version__
# from cronvice import unitname
from cronvice import config
from cronvice import libs_screen
from cronvice import libs_cron
# import list_screen_sessions
# import time
# import datetime as dt
from console import fg, bg
import time
# import os

import pandas as pd
import numpy as np
from terminaltables import SingleTable
import datetime as dt
from dateutil import parser
#import dateutil
# =============================================================
#
#--------------------------------------------------------------

def decode_datetime(date_string):
    return parser.parse(date_string, dayfirst=True)

def crtable():
    scrlist = libs_screen.list_screen_sessions()
    crolist = libs_cron.list_crons()
    #print(scrlist)
    #time.sleep(3)
    df = pd.DataFrame(  columns=['cron', 'screen',  'elapsed', 'comment', 'DT', 'path'])
    #print(df)
    ix = 0
    # list here all what is in cron
    for i in crolist:
        name = i #item[0].split(".")[1]
        comment = libs_cron.get_comment(name)
        libs_cron.fill_current_DTS() # refresh all DT - time consuming MUST COME BEFORE DT
        dtslice = libs_cron.get_DT(name)
        #config.debug_write(dtslice, "DF")
        if not comment is None:
            comment = comment.strip().replace("#", "")
            comment = comment.strip().replace("myservice_description:", "").strip(" ")
        else:
            comment = "..."
        df.loc[ ix, 'cron'] = name
        df.loc[ ix, 'screen'] = "----"
        #df.loc[ ix, 'time'] = "----"

        # if it was run
        interval = "----"

        ### mystery  ***** NOT REALLY * running is always from outside; here there is no idea
        # NEVERHAPPENS
        if name in config.PROC_OBJ.keys():
            #config.debug_write(f"Warning:  key {name} in obj", "DF")
            if 'dt' in config.PROC_OBJ[name]:
                interval = config.PROC_OBJ[name]['dt']
                #pass
        #     with open("/tmp/cronvice.log", "a") as f:
        #         f.write(f"i... in DF ... {name} at {config.INSIDE_PROC_OBJ[name]}\n")

        #     if type(config.INSIDE_LAST_RUN[name]) == dt.timedelta:
        #         interval = round(config.INSIDE_LAST_RUN[name].total_seconds(), 1)
        #         with open("/tmp/cronvice.log", "a") as f:
        #             f.write(f"i... in DF ... {name} timedelta {config.INSIDE_LAST_RUN[name]}\n")

        df.loc[ ix, 'elapsed'] = interval #
        df.loc[ ix, 'comment'] = comment
        df.loc[ ix, 'DT'] = dtslice
        df.loc[ ix, 'path'] = libs_cron.get_fullpath(name).split("/")[-2]
        #if name.find("flash") >= 0:
        #    config.debug_write(f"{dtslice}, {ix}, {df.loc[ ix, 'DT']}", "XX")
        ##df.loc[ 0, 'time'] = ctime
        ix += 1

    #print(df)
    #df.set_index( df['cron'], inplace=True)
    #print("-------------", list(df['cron']), name)
    #time.sleep(10)
    # ---------------------------- SCREENS  -------------------------
    if (scrlist is None) or (len(scrlist) < 1):
        return df
    for i in scrlist:
        item = i.strip().split("\t")
        if len(item) < 2:
            config.debug_write(f"Error: in screen ls: {i} {scrlist}", "DF")
            config.debug_write(f"Error: in screen", "DF")
            return df # HARDER !!!!!
            continue # BUG WITH SCREEN LS - myservice was failing a lot
        ctime = item[1].strip("()")
        name = item[0].split(".")[1] # THIS WILL BE WITH _CX
        if name.find( config.CONFIG['screentag'] ) > 0:
            #print(f"{line[0]:20s} -  {xtime}  -  {xlong}")
            name = name.split( config.CONFIG['screentag'] )[0]
        else:
            name = None
        #print(name, type(name))
        if name in list(df['cron']):
            index = df.index[df['cron'] == name][0] # get index of the row where col:cron==name
            df.loc[ index, 'screen'] = name
            #df.loc[ 0, 'screen'] = name
            #df.loc[ index, 'time'] = ctime
            #dateutil.parser.parserinfo(dayfirst=True)
            date_time = decode_datetime(ctime)
            #date_time = dt.datetime.strptime(ctime, "%d/%m/%y %H:%M:%S")
            time_difference = dt.datetime.now() - date_time
            xe = f"{time_difference.days}d {time_difference.seconds // 3600}h {(time_difference.seconds % 3600) // 60}m"
            df.loc[ index, 'elapsed'] = xe
            pass
        #ix += 1
    #time.sleep(10)
    return df

# =============================================================
#
#--------------------------------------------------------------

def create_dummy_df():
    """
    create dummy dataframe from scratch.... test purposes
    """
    columns = ["a", "b", "c", "_fg", "_bg"]
    # columns1=[x for x in columns if x[0]!="_"]
    df = pd.DataFrame(np.random.randint(0, 9, size=(11, len(columns))),
                      columns=columns)
    df["_fg"] = fg.lightgray  # fg.default
    df["_bg"] = bg.default

    # --------------------------- default pattern ------------
    for i, row in df.iterrows():
        if i % 3 == 0:
            df.loc[i, ["_bg"]] = bg.darkslategray  # bg.dimgray#bg.darkslategray
        else:
            df.loc[i, ["_bg"]] = bg.default  # bg.black

        #if i % 5 == 0:
        #    df.loc[i, ["_fg"]] = fg.lightgreen  # lightyellow

    return df


def inc_dummy_df(df):
    """
    increase df cells by unit for the demo dummy table
    """
    for i, row in df.iterrows():
        df.iloc[i, :-2] = df.iloc[i, :-2] + 1  # loc doesnt work, iloc is ok
    return df



def enhance_df(df):
    """
    With a read dataframe, you need to enhance with _bg and _fg to be displayable
    """
    #columns = ["a", "b", "c", "_fg", "_bg"]
    # columns1=[x for x in columns if x[0]!="_"]
    #df = pd.DataFrame(np.random.randint(0, 9, size=(11, len(columns))),
    #                  columns=columns)
    df["_fg"] = fg.lightgray  # fg.default
    df["_bg"] = bg.default

    # --------------------------- default pattern ------------
    for i, row in df.iterrows():
        if i % 3 == 0:
            df.loc[i, ["_bg"]] = bg.darkslategray  # bg.dimgray#bg.darkslategray
        else:
            df.loc[i, ["_bg"]] = bg.default  # bg.black
        #
        #if i % 5 == 0:
        #    df.loc[i, ["_fg"]] = fg.lightgreen  # lightyellow
    return df




# ======================================================
def show_table(df, selection="3", return_subdf=False):
    """
    enhance the df and display fancy. Also return df when selection
    """

    row_n = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    #---------------

    if return_subdf:
        # Convert selection to a list of integers (0-based index)
        # selected_indices = [ord(char) - 1 for char in str(selection) ]
        selected_indices = [row_n.index(char) for char in selection]
        selected_indices = [i for i in selected_indices if i < len(df)] # avoid crasjh
        return  df.iloc[selected_indices]

    dfenha = df.copy()
    dfenha = enhance_df(dfenha)
    #-
    dfpure = df.copy()
    # dfpure.drop(columns=["_fg", "_bg"], inplace=True) # oooo

    rows = dfpure.values.tolist() #-------------------->>>>>
    rows = [[str(el) for el in row] for row in rows] #->>>>>
    # columns = df.columns.tolist()
    #
    columns2 = [x for x in list(dfenha.columns) if x[0] != "_"]
    #
    tab_header = [["n"] + columns2]  #----------
    #
    # tab_header = [  f"{fg.white}{x}{fg.default}" for x in tab_header] # NOTW
    # data = [['a','b'], ['ca','cb']]
    #========================= start to construct the table ============
    tab_src = tab_header.copy()

    # nn=0  #I use index
    padding = "  "  # nicer bars
    for index, row in dfenha.iterrows():
        # i take row from pure
        row = list(dfpure.loc[index, :])
        fgcol = fg.white
        fgcol = dfenha.loc[index, ["_fg"]].iloc[0]
        bgcol = dfenha.loc[index, ["_bg"]].iloc[0]
        if selection is not None and row_n[index] in list(selection):
            # print(index, selection)
            bgcol = bg.yellow4  # df.loc[index,['_fg']][0]

        # print(bgcol)
        # print(index, row ) # list of pure df cols for row
        row = [row_n[index]] + row

        for j in range(len(row)):  # change color for all columns
            row[j] = (
                fgcol
                + bgcol
                + padding
                + str(row[j])
                + padding
                + bg.default
                + fg.default
            )



        tab_src.append(row)  # prepend to list /THE TABLE TO DISPLAY/
        # nn+=1

    # ==================== HERE IS THE OBJECT=========
    table = SingleTable(tab_src)
    table.padding_left = 0
    table.padding_right = 0
    # blessings terminal() t.clear()

    # --------- if too wide - i think
    if not table.ok:
        table.padding_left = 0
    if not table.ok:
        table.padding_right = 0
    while not table.ok:
        # if bad size
        # remove columns here
        j = 0
        for k in tab_src:
            tab_src[j] = k[:-1]
            j+=1
        table = SingleTable(tab_src)
        table.padding_left = 0
        table.padding_right = 0

    print(table.table)





def main():
    """
    Show table
    """
    df = create_dummy_df()
    df = inc_dummy_df(df)
    move_cursor(15, 4)
    show_table(df)


if __name__ == "__main__":
    Fire(main)
