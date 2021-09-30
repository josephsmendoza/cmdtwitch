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
            self.file.write(data)
            self.file.flush()

    Tee("log.txt", "w")

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
        config = Config(**json.loads(open("config.json", "r").read()))
        open("config.json", "w").write(
            jsonpickle.encode(config, unpicklable=False, indent=4))
    except FileNotFoundError:
        config = Config()
        open("config.json", "x").write(
            jsonpickle.encode(config, unpicklable=False, indent=4))
        input("close this program and edit config.json to continue")
        exit()

    sock = socket.socket()
    if(config.ssl):
        import ssl
        sock = ssl.wrap_socket(sock)

    sock.connect((config.host, config.port))

    def send(msg):
        msg += '\n'
        if(msg.startswith("pass")):
            print("< pass redacted\n")
        else:
            print("< "+msg)
        sock.send(msg.encode())

    def sendMessage(msg):
        send("privmsg #"+config.channel+" :"+msg)

    def isMod(user):
        if user == config.channel:
            return True
        chatters = Chatters(
            **json.loads(requests.get("http://tmi.twitch.tv/group/user/" + config.channel + "/chatters").text))
        return user in chatters.chatters["moderators"]

    send("pass "+config.password)
    send("nick "+config.username)
    send("join #"+config.channel)
    sendMessage("cmdtwitch online")

    while(True):
        msg = sock.recv(1024).decode()
        if not msg:
            input("connection closed")
            exit()
        if(msg.startswith("PING")):
            send("PONG"+msg[4:-1])
            continue
        user = msg[1:msg.find("!")]
        if not isMod(user):
            continue
        msg = msg.lower()
        findstr = "#"+config.channel+" :"
        index = msg.find(findstr)+len(findstr)
        msg = msg[index:-2]
        if msg not in config.commands.keys():
            continue
        cmd=config.commands[msg]
        print("! "+user+":"+msg+":"+cmd)
        try:
            os.system(cmd)
        except Exception as e:
            import traceback
            print(traceback.format_exc()+"\n")

except Exception:
    import traceback
    input(traceback.format_exc())
