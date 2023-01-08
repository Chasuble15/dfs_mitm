from fritm import hook, start_proxy_server
from bridge import InjectorBridgeHandler
import sys
import os
import time
from utils import delay
import json

DOFUS_PATH = "Dofus.lnk"

def launch_dofus():
    """to interrupt : dofus.terminate()"""
    platform = sys.platform
    if platform == "win32":
        path = DOFUS_PATH
    else:
        assert False, (
            "Your platform (%s) doesn't support automated launch yet" % sys.platform
        )
    return os.startfile(path)

bridge = None

def my_callback(coJeu, coSer):
    global bridge
    bridge = InjectorBridgeHandler(coJeu, coSer)
    bridge.loop()


def main():
    PORT = 5555
    FILTER = "port == 5555 || port == 443"
    TARGET = "Dofus.exe"
    
    launch_dofus()
    time.sleep(1)
    hook(TARGET, PORT, FILTER)
    httpd = start_proxy_server(my_callback, PORT)          

    command_console()
          
 
def command_console():
    while True:
        cmd = input("Command: ")
        
        if cmd == "scrape":
            with open("price_checklist.txt", "r") as f:
                for line in f:
                    print("Scraping ...")
                    gid = int(line)
                    bridge.check_resource(gid, True)
                    delay(0.5, 2)
                    bridge.check_resource(gid, False)
                    delay(0.5, 2)
            print("Scraping terminé:")
            print(json.dumps(bridge.prices , sort_keys=True, indent=4))      
            bridge.prices.clear()  
        if cmd == "hdv":
            bridge.open_hdv()        
            
                        
if __name__ == '__main__':
    main()     
                   