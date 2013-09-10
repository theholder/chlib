import chlib


class Bot(chlib.conManager):

    def run(self):
      groups = ["example", "example2"] #list your group names instead
      for group in groups: self.addGroup(group)
      self.cmdPrefix = "!" #optional, just won't call any commands.

    def recvFail(self, group):
      print("Failed to connect to "+group.name)

    def recvInit(self, group):
      print("Connected to "+group.name)


    def recvPMInit(self, group):
      print("Connected to "+group.name)


    def recvRemove(self, group):
      print("Disconnected from "+group.name)


    def recvCommand(self, user, group, auth, post, cmd, args):

      if cmd == "a":
        group.sendPost("AAAAAAAAAAAAAA")


    def recvPost(self, user, group, auth, post):
      print(user+":"+post.post)


    def recvPM(self, user, pm):
      print("PM:"+user+": "+pm)
      self.sendPM(user, pm) # echo


    def recvPMKick(self):
      self.pmConnect()


if __name__ == "__main__": #no easy starting this time ;D
    bot = Bot(user = "username", password = "password", pm = True)
    bot.main()
