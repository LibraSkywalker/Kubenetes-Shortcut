import subprocess
import sys
from functools import partial

def _shell(proc, cmd) :
    proc.stdin.write((cmd + '\n') .encode())
    proc.stdin.flush()
    return proc.stdout.readline().decode().rstrip()

proc = subprocess.Popen(['/bin/bash'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
shell = partial(_shell, proc)

cmd_list = ["kls", "kcd", "kcat", "klog", "kexit"]
cmd_alias = {
    "kls" : "get",
    "kcat" : "describe",
    "klog" : "log"
}
namespace = '~'
print("Welcome to use kubernetes shell.")
while True :
    cmd = input('%s:%s$ ' % (shell("echo $USER"), namespace))
    if (cmd.split()[0] in cmd_list) :
        cmd = cmd.split()
        if cmd[0] == "kexit" :
            print("Kubernetes shell exit.")
            sys.exit(0)
        elif cmd[0] == "kcd" :
            if cmd[1] == "default" :
                namespace = "~"
            elif cmd[1] == ".." :
                namespace = "/"
            else :
                namespace = cmd[1]
        else :
            cmd = ["kubectl", cmd_alias[cmd[0]]] + cmd[1:]
            if namespace == "/" :
                cmd.append('-A')
            elif namespace != "~" :
                cmd.extend(["-n",namespace])
            cmd = " ".join(cmd)
            print(shell(cmd))
        
    else :
        print(shell(cmd))
