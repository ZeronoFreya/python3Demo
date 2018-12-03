from os import path 
import winshell 
import sys

def create_shortcut_to_desktop(): 
    target = sys.argv[0]
    target = target[:target.rfind("/")]+'/demo.txt'
    title = 'Demo'
    s = path.basename(target) 
    fname = path.splitext(s)[0] 
    winshell.CreateShortcut( 
    Path = path.join(winshell.desktop(), fname + '.lnk'), 
    Target = target, 
    Icon=(target, 0), 
    Description=title)  


create_shortcut_to_desktop()
