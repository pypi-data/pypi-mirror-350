# cronvice

*maintain your programs running under SCREEN using AT job scheduler*

## Example

``` python
 # example
cronvice --help
```

## Installation

``` {.bash org-language="sh"}
# you need the scheduler
# sudo  apt install at # NOT HERE
sudo apt install crontab
# you nee the code (anti PEP 668 way)
pip3 install cronvice
```

All scripts must be in \~/.myservice/anyname/tag

-   where \~/.myservice is the S-PATH, path to scripts structure
-   anyname - can be number of different subfolders
-   tag must be a executable script with a uniqe name in all
    \~/.myservice
-   \~/.config/cronvice/cfg.json - contains the S-PATH (\"services\")
-   without a parameter, interactive tui is run, quit it with .q

## Usage

Harmless calls

``` example
cris l
cris t syncthing
cris p syncthing
cris c syncthing
```

Enter to screen enviroment when running

``` example
cris e syncthing
```

-   r(un)
-   a(dd)
-   d(elete)
-   e(nter)
-   c(omment show)
-   t(ime show)
-   p(ath show)
-   l(ist cron)
-   x (block service call with impossible timestamp)

## Important services

### PI

-   inet/ap~switch~
-   inet/piaddr.py
-   warning/lowdisk
-   hwdevs/tele012~ntc~ (technic)
-   image/flashcam8000
-   image/flashcam5000

## BUGS

-   crashes when no crontab defined
-   DATE MUST BE \`Sat 12 Apr 17:09:55 CEST 2025\`
    -   NOT \`Sat Apr 12 15:09:39 UTC 2025\`
    -   use install.me script to repair

## Appendix

*these are comments for using uv and uvx.... this is new stuff*

### New workflow with environments

Workflow

-   ./distcheck.sh (no pip3 inside)

    -   if `twine`{.verbatim} not present,
        `uv tool install --force twine`
    -   same with `uv tool install --force bump2version`

-   `uv tool install --upgrade cronvice` and if hidden errors:

    -   `uv tool install --upgrade cronvice==0.1.31` force to reveal

-   NEVERTHELESS, environment is needed

    -   `make ~/.venv`
    -   `cd ~/.venv`
    -   `uv venv myservicenv` and it is in this user folder.
    -   ANY USE NEEDS `source ~/.venv/myservicenv/bin/activate`
    -   All stuff needs to be installed via uv: like
        `uv pip install fire`
    -   When all is installed, `source ...activate` is run before python
        call
        -   which works for `tele01` that calls `te01.py`
        -   that has normal shebang

-   PROBLEM for `influx_chrony`

    -   no idea now...

-   NO PROBLEM `telegrf`, only telegraf needs to get installed

    **Using local venv is even better**

    `uv venv` creates local .venv in the project, see more and more
    about lock

### Hybrid shebang

*two cases with different environemnts are hard*

``` bash
#!/bin/bash
#myservice_description: disk and ntp to INFLUX

"""" 2>/dev/null
# BASH CODE STARTS HERE

echo "Hello world from Bash!"
sleep 1
if [ -e "$HOME/.venv/myservicenv/bin/activate" ]; then
 source  $HOME/.venv/myservicenv/bin/activate
 echo i... myservicenev is activated
else
 echo i... not activated
fi
sleep 2
# BASH CODE ENDS HERE
/usr/bin/env python3 $0
exit
"""


#Python code goes here
"""
...
PEP668  UV UVX.... I dont know how to use environment....
"""
import fire
import subprocess as sp
import socket

if __name__=="__main__":
    fire.Fire( main )
```
