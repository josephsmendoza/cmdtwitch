try:
    import sys

    class Tee(object):
        def __init__(self, name, mode):
            self.file = open(name, mode)
            self.stdout = sys.stdout
            self.stderr = sys.stderr
            sys.stdout = self
            sys.stderr = self

        def __del__(self):
            sys.stdout = self.stdout
            sys.stderr = self.stderr
            self.file.close()

        def write(self, data):
            self.stdout.write(data)
            self.stdout.flush()
            self.file.write(data)
            self.file.flush()

    Tee("cmdtwitch.log", "w")

except Exception:
    import traceback
    input(traceback.format_exc())

while(True):
    try:
        import jsonpickle
        import requests
        break
    except ModuleNotFoundError as e:
        import os
        os.system("pip install "+e.name)

from dataclasses import dataclass, field
import jsonpickle
import json
import socket
import multiprocessing
import requests
import os

@dataclass
class Config:
    password: str = "https://twitchapps.com/tmi/"
    username: str = "nobody"
    channel: str = "nowhere"
    ssl: bool = True
    host: str = "irc.chat.twitch.tv"
    port: int = 6697
    commands: dict[str, str] = field(default_factory=dict)

@dataclass
class Chatters:
    chatters: dict[str, list[str]] = field(default_factory=dict)
    _links: list[str] = field(default_factory=list)
    chatter_count: int = 0

def print(msg):
    sys.stdout.write(msg+"\n")

try:
    config = Config(**json.loads(open("cmdtwitch.json", "r").read()))
    open("cmdtwitch.json", "w").write(
        jsonpickle.encode(config, unpicklable=False, indent=4))
except FileNotFoundError:
    config = Config()
    open("cmdtwitch.json", "x").write(
        jsonpickle.encode(config, unpicklable=False, indent=4))
    input("close this program and edit cmdtwitch.json to continue")
    exit()

sock = socket.socket()
if(config.ssl):
    import ssl
    sock = ssl.wrap_socket(sock)

sock.connect((config.host, config.port))

def send(msg):
    if(msg.startswith("pass")):
        print("< pass redacted")
    else:
        print("< "+msg)
    sock.send((msg+"\r\n").encode())

def sendMessage(msg):
    send("privmsg #"+config.channel+" :"+msg)

mods=[]

send("CAP REQ :twitch.tv/commands")
sendMessage("/mods")
sendMessage("cmdtwitch online")
findstr = "#"+config.channel+" :"
modstr = "The moderators of this channel are: "
while(True):
    raw = sock.recv(1024).decode()
    if not raw:
        input("connection closed")
        exit()
    for msg in raw.split("\r\n"):
        if not msg:
            continue
        print("> "+msg)
        if(msg.startswith("PING")):
            send("PONG"+msg[4:])
            continue
        modindex=msg.find(modstr)
        if(modindex != -1):
            mods=msg[modindex+len(modstr):].split(", ")
            print("! mods list updated: "+" ".join(mods))
            continue
        user = msg[1:msg.find("!")]
        if user not in mods:
            continue
        msg = msg.lower()
        index = msg.find(findstr)+len(findstr)
        msg = msg[index:].split(" ")
        if msg[0] not in config.commands.keys():
            continue
        cmd=config.commands[msg[0]].replace("$args"," ".join(msg[1:]))
        print("! "+user+":"+(" ".join(msg))+":"+cmd)
        try:
            os.system(cmd)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
