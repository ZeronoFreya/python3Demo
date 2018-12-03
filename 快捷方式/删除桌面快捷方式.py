from os import path
import winshell
import sys
 
def delete_shortcut_from_startup():
    target = sys.argv[0]
    target = target[:target.rfind("/")] + '/demo.txt'
    s = path.basename(target)
    fname = path.splitext(s)[0]
    delfile = path.join(winshell.startup(), fname + '.lnk')
    winshell.delete_file(delfile)

delete_shortcut_from_startup()
