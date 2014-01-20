################################
#File: chlib.py
#Made by: cellsheet/charizard
#Description: My take on a flexable chatango library.
#Contact: charizard.chatango.com
#Release date: 7/31/2013
#Version: 1.5
################################

################################
#Python Imports
################################

import socket
import select
import time
import re
import urllib.request
import random
import threading

################################
#Get server number
################################

def getServer(group):
  s_num = None
  specials = {"de-livechat": 5, "ver-anime": 8, "watch-dragonball": 8, "narutowire": 10, "dbzepisodeorg": 10,
              "animelinkz": 20, "kiiiikiii": 21, "soccerjumbo": 21, "vipstand": 21, "cricket365live": 21,
              "pokemonepisodeorg": 22, "watchanimeonn": 22, "leeplarp": 27, "animeultimacom": 34,
              "rgsmotrisport": 51, "cricvid-hitcric-": 51, "tvtvanimefreak": 54, "stream2watch3": 56,
              "mitvcanal": 56, "sport24lt": 56, "ttvsports": 56, "eafangames": 56, "myfoxdfw": 67, "peliculas-flv": 69,
              "narutochatt": 70}

  if group in specials.keys(): s_num = specials[group]
  else:
    weights = [['5', 75], ['6', 75], ['7', 75], ['8', 75], ['16', 75], ['17', 75], ['18', 75], ['9', 95], ['11', 95], ['12', 95], ['13', 95], ['14', 95], ['15', 95], ['19', 110], ['23', 110], ['24', 110], ['25', 110], ['26', 110], ['28', 104], ['29', 104], ['30', 104], ['31', 104], ['32', 104], ['33', 104], ['35', 101], ['36', 101], ['37', 101], ['38', 101], ['39', 101], ['40', 101], ['41', 101], ['42', 101], ['43', 101], ['44', 101], ['45', 101], ['46', 101], ['47', 101], ['48', 101], ['49', 101], ['50', 101], ['52', 110], ['53', 110], ['55', 110], ['57', 110], ['58', 110], ['59', 110], ['60', 110], ['61', 110], ['62', 110], ['63', 110], ['64', 110], ['65', 110], ['66', 110], ['68', 95], ['71', 116], ['72', 116], ['73', 116], ['74', 116], ['75', 116], ['76', 116], ['77', 116], ['78', 116], ['79', 116], ['80', 116], ['81', 116], ['82', 116], ['83', 116], ['84', 116]]
    group = group.replace('-', 'q').replace('_', 'q')
    tmp8 = max(int(group[6:][:3], 36), 1000) if len(group) > 6 else 1000
    tmp9 = (int(group[:5], 36) % tmp8) / tmp8
    tmp6 = sum(x[1] for x in weights)
    tmp4 = 0
    for i in range(0, len(weights)):
      tmp4 += weights[i][1] / tmp6
      if (tmp9 <= tmp4):
        s_num = weights[i][0]
        break
  return s_num

################################
#Generate Auth/Anon ID
################################

class Generate:

  def aid(self, n, uid):
    try:
      if (int(n) == 0) or (len(n) < 4): n = "3452"
    except ValueError: n = "3452"
    if n != "3452": n = str(int(n))[-4:]
    v1, v5 = 0, ""
    for i in range(0, len(n)): v5 += str(int(n[i:][:1])+int(str(uid)[4:][:4][i:][:1]))[len(str(int(n[i:][:1])+int(str(uid)[4:][:4][i:][:1]))) - 1:]
    return v5

  def auth(self):
    auth = urllib.request.urlopen("http://chatango.com/login",
                                  urllib.parse.urlencode({
                                  "user_id": self.user,
                                  "password": self.password,
                                  "storecookie": "on",
                                  "checkerrors": "yes" }).encode()
                                  ).getheader("Set-Cookie")
    try: return re.search("auth.chatango.com=(.*?);", auth).group(1)
    except: return None

################################
#Represents chat groups
################################

class Group:

  def __init__(self, manager, group, user, password, uid):

    self.manager = manager
    self.name = group
    self.user = user.lower()
    self.password = password
    self.time = None
    self.chSocket = None
    self.wbuf = b""
    self.snum = getServer(group)
    self.loginFail = False
    self.uid = uid
    self.mods = list()
    self.owner = None
    self.blist = list()
    self.bw = list()
    self.users = list()
    self.ping = False
    self.pArray = {}
    self.unum = None
    self.limit = 0
    self.limited = 0
    self.fSize = "11"
    self.fFace = "0"
    self.fColor = "000"
    self.nColor = "CCC"
    self.connect()

  def fileno(self): return self.chSocket.fileno()
  def connect(self):
    self.chSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.chSocket.setblocking(True)
    self.chSocket.connect(("s"+str(self.snum)+".chatango.com", 443))
    threading.Timer(90, self.manager.pingTimer, (self,)).start()
    self.wbuf += bytes("bauth:"+self.name+":"+self.uid+":"+self.user+":"+self.password+"\x00", "latin-1")

  def disconnect(self):
    self.chSocket.close()
    if self in self.manager.cArray: self.manager.cArray.remove(self)

  def getBanList(self):
    self.blist = list()
    self.sendCmd("blocklist", "block", "", "next", "500")

  def sendCmd(self, *args): self.wbuf += bytes(':'.join(args)+"\r\n\x00", "latin-1")
  def getLastPost(self, match, data = "user"):
    try: post = [x for x in list(self.pArray.values()) if getattr(x, data) == match][-1]
    except IndexError: post = None
    return post

  def sendPost(self, post, html = True):
    if not html: post = post.replace("<", "&lt;").replace(">", "&gt;")
    if len(post) < 2700 and self.limited == 0: self.sendCmd("bmsg", "t12r", "<n"+self.nColor+"/><f x"+self.fSize+self.fColor+"=\""+self.fFace+"\">"+post)

  def login(self, user, password = None):
    if user and password:
      self.sendCmd("blogin", user, password) #user
      self.user = user
    elif user:
      self.user = "#" + user
      self.sendCmd("blogin", user) #temporary user
    else: self.sendCmd("blogin")

  def logout(self): self.sendCmd("blogout")

  def enableBg(self): self.sendCmd("getpremium", "1")
  def disableBg(self): self.sendCmd("msgbg", "0")

  def enableVr(self): self.sendCmd("msgmedia", "1")
  def disableVr(self): self.sendCmd("msgmedia", "0")

  def setNameColor(self, nColor): self.nColor = nColor
  def setFontColor(self, fColor): self.fColor = fColor
  def setFontSize(self, fSize):
    if int(fSize) < 23: self.fSize = fSize
  def setFontFace(self, fFace): self.fFace = fFace

  def getAuth(self, user):
    if user == self.owner: return "2"
    if user in self.mods: return "1"
    else: return "0"

  def getBan(self, user):
    banned = [x for x in self.blist if x.user == user]
    if banned: return banned[0]
    else: return None

  def dlPost(self, post): self.sendCmd("delmsg", post.pid)

  def dlUser(self, user):
    post = self.getLastPost(user)
    unid = None
    if post: unid = post.unid
    if unid: self.sendCmd("delallmsg", unid, "")

  def bUser(self, user):
    unid = None
    ip = None
    try:
      unid = self.getLastPost(user).unid
      ip = self.getLastPost(user).ip
    except: pass
    if unid and ip:
      if (user.startswith("#")) or (user.startswith("!")): self.sendCmd("block", unid, ip, "")
      else: self.sendCmd("block", unid, ip, user)
    self.getBanList()

  def flUser(self, user):
    pid = self.getLastPost(user).pid
    self.sendCmd("g_flag", pid)

  def ubUser(self, user):
    banned = [x for x in self.blist if x.user == user]
    if banned:
      self.sendCmd("removeblock", banned[0].unid, banned[0].ip, banned[0].user)
      self.getBanList()

  def setMod(self, mod): self.sendCmd("addmod", mod)
  def eraseMod(self, mod): self.sendCmd("removemod", mod)
  def clearGroup(self):
    if self.user == self.owner: self.sendCmd("clearall")
    else: #;D
      for history in list(self.pArray.values()): self.sendCmd("delmsg", history.pid)
  
################################
#Connections Manager
#Handles: New Connections and Connection data
################################

class conManager:

  def __init__(self, user, password, pm):
    self.user = user.lower()
    self.password = password
    self.pm = pm
    self.name = "pm"
    self.connected = False
    self.pmConnected = False
    self.cArray = list()
    self.groups = list()
    self.fl = list()
    self.bl = list()
    self.chSocket = None
    self.wbuf = b""
    self.pmAuth = None
    self.ping = None
    self.ip = None
    self.fSize = "11"
    self.fFace = "0"
    self.fColor = "000"
    self.nColor = "000"
    self.uid = str(int(random.randrange(1000000000000000, 10000000000000000)))
    self.cmdPrefix = None
    if self.pm: self.pmConnect()

  def fileno(self): return self.chSocket.fileno()

  def pmConnect(self):
    self.chSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.chSocket.setblocking(True)
    self.chSocket.connect(("c1.chatango.com", 5222))
    self.pmAuth = Generate.auth(self)
    threading.Timer(90, self.pingTimer, (self,)).start()
    self.wbuf += bytes("tlogin:"+self.pmAuth+":2:"+self.uid+"\x00", "latin-1")

  def sendCmd(self, *args): self.wbuf += bytes(':'.join(args)+"\r\n\x00", "latin-1")

  def addGroup(self, group):
    if not self.getGroup(group) in self.cArray:
      group = Group(self, group, self.user, self.password, self.uid)
      self.cArray.append(group)
      self.groups.append(group.name)
    self.connected = True

  def removeGroup(self, group):
    group = self.getGroup(group)
    if group in self.cArray:
      self.cArray.remove(group)
      self.groups.remove(group.name)
      group.chSocket.close()
      self.recvRemove(group)
    if not self.cArray:
      self.ping = False
      self.connected = False

  def getGroup(self, group):
    group = [g for g in self.cArray if g.name == group]
    if group: return group[0]

  def getUser(self, user):
    groups = list()
    for group in self.cArray:
      if hasattr(group, "users"):
        if user.lower() in group.users: groups.append(group.name)
    if groups: return groups
    else: return None

  def cleanPM(self, pm): return re.sub("<i s=\"sm://(.*?)\" w=\"(.*?)\" h=\"(.*?)\"/> ", "", re.sub(" <i s=\"sm://(.*?)\" w=\"(.*?)\" h=\"(.*?)\"/>", "", re.sub("<mws c='(.*?)' s='(.*?)'/>", "", re.sub("<g x(.*?)\">", "", re.sub("<n(.*?)/>", "", re.sub("</(.*?)>", "", pm.replace("<m v=\"1\">", "").replace("<g xs0=\"0\">", "")))))))
  def sendPM(self, user, pm): self.sendCmd("msg", user, "<n"+self.nColor+"/><m v=\"1\"><g xs0=\"0\"><g x"+self.fSize+"s"+self.fColor+"=\""+self.fFace+"\">"+pm+"</g></g></m>")

  def manage(self, group, cmd, bites):

    args = [group]
    
    if cmd == "denied":
      group.chSocket.close()
      self.cArray.remove(self.getGroup(group.name))
      if not self.cArray: self.connected = False

    elif cmd == "ok":
      if bites[3] != 'M': self.removeGroup(group.name)
      else:
        group.owner = bites[1]
        group.time = bites[5]
        self.ip = bites[6]
        group.mods = bites[7].split(';')
        group.mods.sort()

    elif cmd == "inited":
      group.sendCmd("blocklist", "block", "", "next", "500")
      group.sendCmd("g_participants", "start")
      group.sendCmd("getbannedwords")
      group.sendCmd("getratelimit")

    elif cmd == "premium":
      if int(bites[2]) > time.time(): group.sendCmd("msgbg", "1")

    elif cmd == "getratelimit":
      group.limit = int(bites[1])
      group.limited = int(bites[2])

    elif cmd == "g_participants":
      pl = ":".join(bites[1:]).split(";")
      for p in pl:
        p = p.split(":")[:-1]
        if p[-2] != "None" and p[-1] == "None": group.users.append(p[-2].lower())
      group.users.sort()

    elif cmd == "blocklist":
      if bites[1]:
        blklist = (":".join(bites[1:])).split(";")
        for banned in blklist:
          bData = banned.split(":")
          group.blist.append(type("BannedUser", (object,), {"unid": bData[0], "ip": bData[1], "user": bData[2], "uid": bData[3], "mod": bData[4]}))
        lastUid = group.blist[-1].uid
        group.sendCmd("blocklist", "block", lastUid, "next", "500")

    elif cmd == "bw": group.bw = bites[2].split("%2C")
    elif cmd == 'participant':
      user = None
      if (bites[1] == '0') and (bites[4] != "None") and (bites[4].lower() in group.users):
        group.users.remove(bites[4].lower())
      if (bites[1] == '1') and (bites[-4] != "None"):
        group.users.append(bites[4].lower())
        group.users.sort()
      args = [bites[1], group, user, bites[3]]

    elif cmd == "ratelimited": group.limit = int(bites[1])
    elif cmd == "ratelimitset": group.limit = int(bites[1])
    elif cmd == "getratelimit":
      group.limit = int(bites[1])
      group.limited = int(bites[2])

    elif cmd == 'b':
      try:
        fTag = re.search("<f x(.*?)>", bites[10]).group(1)
        fSize = fTag[:2]
        fFace = re.search("(.*?)=\"(.*?)\"", fTag).group(2)
        fColor = re.search(fSize+"(.*?)=\""+fFace+"\"", fTag).group(1)
      except:
        fSize = "11"
        fColor = "000"
        fFace = "0"
      group.pArray[int(bites[6])] = type("Post", (object,), {"group": group, "time": bites[1], "user": bites[2].lower() if bites[2] != '' else "#" + bites[3] if bites[3] != '' else "!anon" + Generate.aid(self, re.search("<n(.*?)/>", bites[10]).group(1), bites[4]) if re.search("<n(.*?)/>", bites[10]) != None else None , "tmp": bites[3] if bites[3] != '' else None, "uid": bites[4], "unid": bites[5], "pnum": bites[6], "ip": bites[7], "post": re.sub("<(.*?)>", "", ":".join(bites[10:])).replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", "\"").replace("&apos;", "'").replace("&amp;", "&"), "nColor": re.search("<n(.*?)/>", bites[10]).group(1) if re.search("<n(.*?)/>", bites[10]) else "000", "fSize": fSize, "fFace": fFace, "fColor": fColor})

    elif cmd == 'u':
      try:
        post = group.pArray[int(bites[1])]
        setattr(post, "pid", bites[2])
        if post.post: #not blank post
          self.recvPost(post.user, group, group.getAuth(post.user), post)
          if post.post[0] == self.cmdPrefix: self.recvCommand(post.user, group, group.getAuth(post.user), post, post.post.split()[0][1:].lower(), " ".join(post.post.split()[1:]))
      except KeyError: pass

    elif cmd == "n": group.unum = bites[1]
    elif cmd == "mods":
      mlist = bites[1:]
      mod = ""
      if len(mlist) < len(group.mods):
        mod = [m for m in group.mods if m not in mlist][0]
        group.mods.remove(mod)
        args = [True, group, mod]
      if len(mlist) > len(group.mods):
        mod = [m for m in mlist if m not in group.mods][0]
        group.mods.append(mod)
        args = [False, group, mod]

    elif cmd == "deleteall":
      for pid in bites[1:]:
        deleted = group.getLastPost(pid, "pid")
        if deleted:
          args = [group, deleted]
          del group.pArray[int(deleted.pnum)]
        else: args = [group, None]

    elif cmd == "delete":
      deleted = group.getLastPost(bites[1], "pid")
      if deleted:
        args = [group, deleted]
        del group.pArray[int(deleted.pnum)]
      else: args = [group, None]

    elif cmd == "blocked":
      if bites[3]: args = [group, bites[3], bites[4]]
      else:
        post = group.getLastPost(bites[1], "unid")
        if post: args = [group, post.user, bites[4]]
      group.getBanList()

    elif cmd == "unblocked":
      if group.name == "pm": self.bl.remove(bites[1])
      else:
        if bites[3]:
          group.getBanList()
          args = [group, bites[3], bites[4]]
        else: args = [group, "Non-member", bites[4]]

    elif cmd == "logoutok": group.user  = "!anon" + Generate.aid(self, self.nColor, group.uid)
    elif cmd == "clearall":
      if bites[1] == "ok": group.pArray = {}

    elif cmd == "tb":
      mins, secs = divmod(int(bites[1]), 60)
      args = [group, mins, secs]

    elif cmd == "OK": self.sendCmd("wl")
    elif cmd == "wl":
      for i in range(1, len(bites), 4): self.fl.append(bites[i])
      self.fl.sort()

    elif cmd == "msg": args = [bites[1], self.cleanPM(":".join(bites[6:]))]
    elif cmd == "msgoff": args = [bites[1], self.cleanPM(":".join(bites[6:]))]

    if hasattr(self, "recv"+cmd) and None not in args: getattr(self, "recv"+cmd)(*args)

  def decode(self, group, buffer):
    buffer = buffer.split(b"\x00")
    for raw in buffer:
      if raw: self.manage(group, raw.decode("latin-1")[:-2].split(":")[0], raw.decode("latin-1")[:-2].split(":"))

  def pingTimer(self, group):
    group.ping = True
    while group.ping:
      group.sendCmd("\r\n\x00")
      time.sleep(90)
    group.ping = False

  def main(self):
    self.run()
    while self.connected or self.pmConnected:
      rSocks, wSocks, eSocks = select.select(self.cArray, [x for x in self.cArray if x.wbuf], self.cArray)
      for wSock in wSocks:
        try: wSock.chSocket.send(wSock.wbuf)
        except BrokenPipeError: wSock.disconnect()
        wSock.wbuf = b""
      for rSock in rSocks:
        rbuf = b""
        while not rbuf.endswith(b'\x00'):
          try: rbuf += rSock.chSocket.recv(1024) #need the WHOLE buffer ;D
          except OSError: rSock.disconnect()
        if len(rbuf) > 0: self.decode(rSock, rbuf)
      time.sleep(0.1)
    [x.chSocket.close() for x in self.cArray]