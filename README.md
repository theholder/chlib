chlib
=====

A chatango library with a flexible manager.


Requirements: This library requires at this time to have python 3 or greater installed.


Specifics:

Chatango will give announcements via in-chat popups, though it isn't guarentee'd it will display correctly
through recvAnnouncement due to lack of announcements, just guarentee'd that you will see the text it gives.


Method enabling:

There are some methods that are disabled by default but can be enabled if needed.
If there is a method that you want to enable, find it by looking for the lines that start with "#self.recv"
followed by the method name. Delete the hashtag and add the method with self followed by its arguments in the bot.
If there is "pass" directly underneath the method name, this can be commented out or removed.


Methods and parameters:

groups:

recvFailedLogin(group)
recvFailedConnect(group)
recvInit(group)
recvUserLeave(group, user)
recvUserJoin(group, user)
recvCommand(user, group, auth/level, post, command, command arguments)
recvPost(user, group, auth/level, post)
recvModErase(group, user)
recvModAdd(group, user)
recvPostDelete(group, post)
recvBan(group, user, mod)
recvUnban(group, user, mod)
recvLogout(group)
recvLogin(group)
recvGroupClear(group)
recvFlWarning(group)
recvGroupBan(group)
recvGroupBanUpdate(minutes, seconds)
recvAnnouncement(announcement text)

PM's:

recvPMInit(group)
recvFailedPMLogin(group)
recvOfflinePM(user, pm)
recvAddUser(user, status, time)
recvDeleteUser(time)
recvOnlineUser(user, time)
recvOfflineUser(user, time)
recvPMKick()
