import subprocess
import sys
import select
from functools import partial
import logging
import time

def _fetch(file) :
    ret, buf = "", ""
    while buf != "EOF" :
        if buf :
            ret += buf + "\n"
        buf = file.readline().decode().rstrip()
        
    return ret.rstrip()

def _shell(proc, logger, cmd, log = True) :
    proc.stdin.write((cmd + '\n') .encode())
    proc.stdin.write("echo EOF\n".encode())
    proc.stdin.write(">&2 echo EOF\n".encode())
    proc.stdin.flush()

    out = _fetch(proc.stdout)
    err = _fetch(proc.stderr)

    if out and log:
        print(out)
    if err and log:
        print(err)

    return out


proc = subprocess.Popen(['/bin/bash'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
logger = logging.getLogger('bash_log')
logger.setLevel(logging.ERROR)
shell = partial(_shell, proc, logger)

cmd_list = ["kls", "kcd", "kcat", "klog", "kexit"]
cmd_alias = {
    "kls" : "get",
    "kcat" : "describe",
    "klog" : "log"
}
namespace = '~'
print("Welcome to use kubernetes shell.")
while True :
    cmd = input('%s:%s[%s]$ ' % (shell("echo $USER", log = False),shell("dirs +0", log = False), namespace))
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
            shell(cmd)
        
    else :
        shell(cmd)
