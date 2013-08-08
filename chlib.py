################################
#File: chlib.py
#Made by: cellsheet/charizard
#Description: My take on a flexable chatango library.
#Contact: charizard.chatango.com
#Release date: 7/31/2013
#Version: 1.0
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
  specials = {"mywowpinoy": 5, "bateriafina-8": 8, "narutowire": 10, "as-chatroom": 10, "chia-anime": 12, "flowhot-chat-online": 12,
              "dbzepisodeorg": 12, "kiiiikiii": 18, "portalsports": 18, "watch-dragonball": 19, "animelinkz": 20, "soccerjumbo": 21,
              "soccerjumbo2": 21, "vipstand": 21, "cricket365live": 21, "phnoytalk": 21, "pokemonepisodeorg": 22, "watchanimeonn": 26,
              "leeplarp": 27, "ver-anime": 34, "animechat20": 34, "proudlypinoychat": 51, "rgsmotrisport": 51, "cricvid-hitcric-": 51,
              "narutochatt": 52, "iluvpinas": 53, "tvanimefreak": 54, "animeproxer": 55, "finalshatman": 55, "stream2watch3": 56,
              "mitvcanal": 56, "sport24lt": 56, "ttvsports": 56, "eplsiite": 56, "eafangames": 56, "bobproctor": 56, "bguk": 67,
              "futboldirectochat": 67, "myfoxdfw": 67, "magicc666": 67}

  if group in specials.keys(): s_num = specials[group]

  else:

    weights = [['5', 61], ['6', 61], ['7', 61], ['8', 61], ['16', 61], ['17', 61], ['9', 90], ['11', 90], ['13', 90], ['14', 90],
               ['15', 90], ['23', 110], ['24', 110], ['25', 110], ['28', 104], ['29', 104], ['30', 104], ['31', 104], ['32', 104],
               ['33', 104], ['35', 101], ['36', 101], ['37', 101], ['38', 101], ['39', 101], ['40', 101], ['41', 101], ['42', 101],
               ['43', 101], ['44', 101], ['45', 101], ['46', 101], ['47', 101], ['48', 101], ['49', 101], ['50', 101], ['57', 110],
               ['58', 110], ['59', 110], ['60', 110], ['61', 110], ['62', 110], ['63', 110], ['64', 110], ['65', 110], ['66', 110]]

    group = 'q'.join(map(str, group.split('_')))
    group = 'q'.join(map(str, group.split('-')))
    gsub36 = int(group[:min(5, len(group))], 36)
    if len(group) >= 6:
      tmp = group[6:][:min(3, len(group) - 5)]
      tmp2 = int(tmp, 36)
    else:
      tmp2 = 1000
    tmp3 = (gsub36 % tmp2) / tmp2
    tmp5 = 0
    tmp6 = 0
    while (tmp6 < len(weights)):
      tmp5+= weights[tmp6][1]
      tmp6+=1
    tmp7 = 0
    tmp8 = [0]*67
    tmp6 = 0
    while (tmp6 < len(weights)):
      tmp7+= weights[tmp6][1] / tmp5
      tmp8[int(weights[tmp6][0])] = tmp7
      tmp6+=1
    tmp6 = 0
    while (tmp6 < len(weights)):
      if (tmp3 <= tmp8[int(weights[tmp6][0])]):
        s_num = weights[tmp6][0]
        break
      tmp6+=1

  return s_num


################################
#Generate Auth/Anon ID
################################

class Generate:

  def aid(self, n, uid):
    n = n.split(".")[0]
    try:
      if (int(n) == 0) or (len(n) < 4): n = "3452"
    except ValueError: n = "3452"
    uid = uid[4:][:4]
    v1 = 0
    v5 = ""
    while v1 < len(n):
      v4 = n[v1:][:1]
      v3 = uid[v1:][:1]
      v2 = str(int(v4)+int(v3))
      v5 += v2[len(v2) - 1:]
      v1 += 1
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
#Represents group banned users
################################

class BannedUser:

  def __init__(self, unid, ip, user, uid, mod):
    self.unid = unid
    self.ip = ip
    if user: self.user = user
    else: self.user = None
    self.uid = uid
    self.mod = mod


################################
#Represents group posts
################################

class Post:

  def __init__(self, group, time, user, tmp, uid, unid, x, ip, post):
    self.time = time
    self.group = group
    if user: self.user = user.lower()
    elif tmp: self.user = "#" + tmp
    else: self.user = "!Anon"
    self.tmp = tmp
    self.uid = uid
    self.unid = unid
    self.pid = None
    self.pnum = None
    try:
      if int(x): self.pnum = x #if b cmd
    except ValueError: self.pid = x #if i cmd
    self.ip = ip
    self.fSize = None
    self.fColor = None
    self.fFace = None
    self.nColor = None
    self.n = None
    self.post = self.cleanPost(post)


  def addId(self, pid): self.pid = pid

  def cleanPost(self, post):
    self.n = re.search("<n(.*?)/>", post)
    if self.n and self.user == "!Anon": self.user += Generate.aid(self, self.n.group(1), self.uid)
    elif self.n: self.nColor = self.n.group(1)
    post = re.sub("<n(.*?)/>", "", post)
    try:
      fTag = re.search("<f x(.*?)>", post).group(1)
      self.fSize = fTag[:2]
      self.fFace = re.search("(.*?)=\"(.*?)\"", fTag).group(2)
      self.fColor = re.search(self.fSize+"(.*?)=\""+self.fFace+"\"", fTag).group(1)
    except:
      self.fSize = "11"
      self.fColor = "000"
      self.fFace = "0"
    if not self.fColor: self.fColor == "000"
    post = re.sub("<(.*?)>", "", post).replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", "\"").replace("&apos;", "'").replace("&amp;", "&")
    return post


################################
#Represents chat groups
################################

class Group:

  def __init__(self, group, user, password, uid):
    
    self.name = group
    self.user = user
    self.password = password
    self.time = None
    self.chSocket = None
    self.snum = getServer(group)
    self.writebuf = b""
    self.loginFail = False
    self.uid = uid
    self.mods = list()
    self.owner = None
    self.blist = list()
    self.bw = list()
    self.users = list()
    self.ping = False
    self.pArray = list()
    self.pHint = None
    self.post = None
    self.unum = None
    self.mhist = None
    self.fSize = "11"
    self.fFace = "0"
    self.fColor = "000"
    self.nColor = "000"


  def connect(self):
    self.chSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.chSocket.connect(("s"+self.snum+".chatango.com", 443))
    self.chSocket.setblocking(False)
    self.writebuf += bytes("bauth:"+self.name+":"+self.uid+":"+self.user+":"+self.password+"\x00", "utf-8")


  def getBanList(self):
    self.blist = list()
    self.sendCmd("blocklist", "block", "", "next", "500")

  def sendCmd(self, *args):
    self.writebuf += bytes(':'.join(args)+"\r\n\x00", "utf-8")

  def sendPost(self, post, html = False):
    if not html: post = post.replace("<", "&lt;").replace(">", "&gt;")
    if len(post) < 2700: self.sendCmd("bmsg", "t12r", "<n"+self.nColor+"/><f x"+self.fSize+self.fColor+"=\""+self.fFace+"\">"+post)
    else: print("Error - Post is too big.")

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

  def getPost(self, var, pData):
    try: post = [x for x in self.pArray if getattr(x, var) == pData][0]
    except IndexError: post = None
    return post

  def getBan(self, user):
    banned = [x for x in self.blist if x.user == user]
    if banned: return banned[0]
    else: return None

  def dlPost(self, post): self.sendCmd("delmsg", post.pid)

  def dlUser(self, user):
    unid = self.getPost("user", user).unid
    self.sendCmd("delallmsg", unid, "")

  def bUser(self, user):
    unid = self.getPost("user", user).unid
    ip = self.getPost("user", user).ip
    if unid and ip:
      if (user.startswith("#")) or (user.startswith("!")): self.sendCmd("block", unid, ip, "")
      else: self.sendCmd("block", unid, ip, user)

  def flUser(self, user):
    pid = self.getPost("user", user).pid
    self.sendCmd("g_flag", pid)

  def ubUser(self, user):
    banned = [x for x in self.blist if x.user == user][0]
    self.sendCmd("removeblock", banned.unid, banned.ip, banned.user)
    self.getBanList()

  def setMod(self, mod): self.sendCmd("addmod", mod)

  def eraseMod(self, mod): self.sendCmd("removemod", mod)

  def clearGroup(self):
    if self.user == self.owner:
      self.sendCmd("clearall")
    else: #;D
      if self.mhist:
        for history in self.pArray:
          self.sendCmd("delmsg", history.pid)

  def loadHist(self):
    self.sendCmd("get_more", "35")

  
################################
#Connections Manager
#Handles: New Connections and Connection data
################################


class conManager:

  def __init__(self, user, password, pm):
    self.user = user
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
    self.pmAuth = None
    self.ping = None
    self.ip = None
    self.fSize = "11"
    self.fFace = "0"
    self.fColor = "000"
    self.nColor = "000"
    self.recvbuf = b""
    self.pmWritebuf = b""
    self.uid = str(int(random.randrange(1000000000000000, 10000000000000000)))
    self.cmdPrefix = None
    if self.pm: self.pmConnect()
    

  def pmConnect(self):
    self.chSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.chSocket.connect(("c1.chatango.com", 5222))
    self.chSocket.setblocking(False)
    self.pmAuth = Generate.auth(self)
    self.pmWritebuf += (("tlogin:"+self.pmAuth+":2:"+self.uid+"\x00").encode())


  def pmDisconnect(self):
    self.pmConnected = False
    self.cArray.remove(self)


  def sendCmd(self, *args): self.pmWritebuf += bytes(':'.join(args)+"\r\n\x00", "utf-8")


  def addGroup(self, group):
    group = Group(group, self.user, self.password, self.uid)
    group.connect()
    if not self.getGroup(group):
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
        if user in group.users: groups.append(group.name)
    if groups: return groups
    else: return None


  def cleanPM(self, pm):
    pm = pm.replace("<m v=\"1\">", "").replace("<g xs0=\"0\">", "")
    pm = re.sub("</(.*?)>", "", pm)
    pm = re.sub("<n(.*?)/>", "", pm)
    pm = re.sub("<g x(.*?)\">", "", pm)
    pm = re.sub("<mws c='(.*?)' s='(.*?)'/>", "", pm)
    pm = re.sub(" <i s=\"sm://(.*?)\" w=\"(.*?)\" h=\"(.*?)\"/>", "", pm)
    pm = re.sub("<i s=\"sm://(.*?)\" w=\"(.*?)\" h=\"(.*?)\"/> ", "", pm)
    return pm


  def sendPM(self, user, pm):
    self.sendCmd("msg", user, "<n"+self.nColor+"/><m v=\"1\"><g xs0=\"0\"><g x"+self.fSize+"s"+self.fColor+"=\""+self.fFace+"\">"+pm+"</g></g></m>")


  def manage(self, group, cmd, bites):


    ################################
    #Group Events
    ################################

    
    if cmd == "ok":
      if bites[3] != 'M':
        self.removeGroup(group.name)
        #self.recvFailedLogin(group)
      else:
        group.owner = bites[1]
        group.time = bites[5]
        self.ip = bites[6]
        group.mods = bites[7].split(';')
        group.mods.sort()


    if cmd == "denied":
      #self.recvFailedConnect(group)
      pass


    if cmd == "inited":
      group.pArray.reverse()
      group.sendCmd("blocklist", "block", "", "next", "500")
      group.sendCmd("g_participants", "start")
      group.sendCmd("getbannedwords")
      self.recvInit(group)


    if cmd == "premium":
      if int(bites[2]) > time.time(): group.sendCmd("msgbg", "1")


    if cmd == "g_participants":
      pl = ":".join(bites[1:]).split(";")
      for p in pl:
        p = p.split(":")[:-1]
        if p[-2] != "None" and p[-1] == "None": group.users.append(p[-2])
      group.users.sort()


    if cmd == "blocklist":
      if bites[1]:
        blklist = (":".join(bites[1:])).split(";")
        for banned in blklist:
          bData = banned.split(":")
          group.blist.append(BannedUser(bData[0], bData[1], bData[2], bData[3], bData[4]))
        lastUid = group.blist[-1].uid
        group.sendCmd("blocklist", "block", lastUid, "next", "500")


    if cmd == "bw": group.bw = bites[2].split("%2C")


    if cmd == 'participant':
      user = None
      if bites[1] == '0' and bites[4] != "None" and bites[4] in group.users:
        group.users.remove(bites[4])
        #self.recvUserLeave(group, user)
      if bites[1] == '1' and bites[-4] != "None":
        group.users.append(bites[4])
        group.users.sort()
        #self.recvUserJoin(group, user)


    if cmd == 'i': group.pArray.append(Post(group, bites[1], bites[2], bites[3], bites[4], bites[5], bites[6], bites[7], ":".join(bites[10:])))

    if cmd == 'b': group.pHint = Post(group, bites[1], bites[2], bites[3], bites[4], bites[5], bites[6], bites[7], ":".join(bites[10:]))

    if cmd == 'u' and bites[2] != "psbulg==":
      if bites[1] == group.pHint.pnum:
        group.pHint.addId(bites[2])
        post = group.pHint
        group.pArray.append(post)
        if post.post: #not blank post
          if post.post[0] == self.cmdPrefix:
            self.recvCommand(post.user, group, group.getAuth(post.user), post, post.post.split()[0][1:].lower(), " ".join(post.post.split()[1:]))
            self.recvPost(post.user, group, group.getAuth(post.user), post) #wont fragment per-post code to gather data
          else: self.recvPost(post.user, group, group.getAuth(post.user), post)


    if cmd == "n": group.unum = bites[1]


    if cmd == "mods":
      mlist = bites[1:]
      if len(mlist) < len(group.mods):
        rmod = [m for m in group.mods if m not in mlist][0]
        group.mods.remove(rmod)
        #self.recvModErase(group, rmod)
      if len(mlist) > len(group.mods):
        amod = [m for m in mlist if m not in group.mods][0]
        group.mods.append(amod)
        #self.recvModAdd(group, amod)


    if cmd == "deleteall":
      for pid in bites[1:]:
        deleted = group.getPost("pid", pid)
        if deleted:
          group.pArray.remove(deleted)
          #self.recvPostDelete(group, deleted)


    if cmd == "delete":
      deleted = group.getPost("pid", bites[1])
      if deleted:
        group.pArray.remove(deleted)
        #self.recvPostDelete(group, deleted)
        

    if cmd == "blocked":
      if bites[3]:
        #self.recvBan(group, bites[3], bites[4])
        pass
      else:
        #self.recvBan(group, group.getPost("unid", bites[1]).user, bites[4])
        pass
      group.getBanList()


    if cmd == "unblocked":
      if group.name == "pm": self.bl.remove(bites[1])
      else:
        if bites[3]:
          group.getBanList()
          #self.recvUnban(group, bites[3], bites[4])
        else:
          #self.recvUnban(group, "Non-member", bites[4])
          pass


    if cmd == "logoutok":
      group.user  = "!Anon" + Generate.aid(self, self.nColor, group.uid)
      #self.recvLogout(group)

    if cmd == "pwdok":
      #self.recvLogin(group)
      pass

    if cmd == "clearall":
      if bites[1] == "ok": group.pArray = list()
      #self.recvGroupClear(group)

    if cmd == "nomore":
      group.mhist = True
      #self.recvHistLoad(group)

    if cmd == "show_fw":
      #self.recvFlWarning(group)
      pass

    if cmd == "show_tb":
      #self.recvGroupBan(group)
      pass

    if cmd == "tb":
      mins, secs = divmod(int(bites[1]), 60)
      #self.recvGroupBanUpdate(mins, secs)

    if cmd == "chatango": #VERY RARE
      #self.recvAnnouncement(bites[1:])
      pass


    ################################
    #PM Events
    ################################


    if cmd == "OK":
      self.sendCmd("wl")
      self.sendCmd("getblock")
      #self.recvPMInit(group)


    if cmd == "DENIED":
      #self.recvFailedPMLogin(group)
      pass


    if cmd == "wl":
      for i in range(1, len(bites), 4): self.fl.append(bites[i])
      self.fl.sort()


    if cmd == "block_list":
      for bBite in bites[1:]:
        if bBite not in self.bl: self.bl.append(bBite)


    if cmd == "msg":
      self.recvPM(bites[1], self.cleanPM(":".join(bites[6:])))


    if cmd == "msgoff":
      #self.recvOfflinePM(bites[1], self.cleanPM(":".join(bites[6:])))
      pass


    if cmd == "wladd":
      #self.recvAddUser(bites[1], bites[2], bites[3])
      pass

    if cmd == "wldelete":
      #self.recvDeletUser(bites[1])
      pass

    if cmd == "wlonline":
      #self.recvOnlineUser(bites[1], bites[2])
      pass

    if cmd == "wloffline":
      #self.recvOfflineUser(bites[1], bites[2])
      pass

    if cmd == "kickingoff":
      #self.recvPMKick()
      pass



  def decode(self, group, buffer):
    buffer = buffer.split(b"\x00")
    for raw in buffer:
      if raw:
        bites = raw.decode("latin-1")[:-2].split(":")
        cmd = bites[0]
        self.manage(group, cmd, bites)


  def pingTimer(self, group):
    while group.ping:
      group.sendCmd("\r\n\x00")
      time.sleep(90)


  def main(self):
    self.run()
    if self.chSocket:
      self.cArray.append(self)
      self.pmConnected = True
    while self.connected or self.pmConnected:
      gSocks = [x.chSocket for x in self.cArray]
      rSockets, wSockets, error = select.select(gSocks, gSocks, [], 0.2)
      for wSocket in wSockets:
        group = [x for x in self.cArray if x.chSocket == wSocket][0]
        if not group.ping:
          t = threading.Timer(90, self.pingTimer, (group,))
          t.start()
          group.ping = True
        if wSocket.getpeername()[1] == 5222:
          if self.pmWritebuf:
            wSocket.send(self.pmWritebuf)
            self.pmWritebuf = b""
        elif group.writebuf:
          group.chSocket.send(group.writebuf)
          group.writebuf = b""
      for rSocket in rSockets:
        group = [x for x in self.cArray if x.chSocket == rSocket][0]
        while not self.recvbuf.endswith(b"\x00"):
          self.recvbuf += group.chSocket.recv(1024) #need the WHOLE buffer ;D
        if len(self.recvbuf) > 0:
          self.decode(group, self.recvbuf)
          self.recvbuf = b""
      time.sleep(0.01)
    [x.chSocket.close() for x in self.cArray]
