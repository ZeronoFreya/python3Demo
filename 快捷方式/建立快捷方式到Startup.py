from os import path
import winshell
import sys
print(winshell.startup())
def create_shortcut_to_startup(): 
    target = sys.argv[0]
    target = target[:target.rfind("/")]+'/demo.txt'
    title = '我的快捷方式'
    s = path.basename(target) 
    fname = path.splitext(s)[0] 
    winshell.CreateShortcut( 
    Path = path.join(winshell.startup(),  
    fname + '.lnk'), 
    Target = target, 
    Icon=(target, 0), 
    Description=title) 


create_shortcut_to_startup()
