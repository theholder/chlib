chlib
=====

A chatango library with a flexible manager.


Requirements: This library requires at this time to have python 3 or greater installed.

Method enabling: no longer needed, each method can be added or removed in the bot without any changes to the library.

Methods and parameters:

groups:

The group method's are now based on the command chatango send's. recvOldMethodName(args) = recvNewMethodName(args)

recvFailedLogin(group) = recvDenied(group)
recvInit(group) = recvInited(group)
recvUserLeave(group, user) = recvParticipant(bit, group, user) NOTE: bit = 0
recvUserJoin(group, user) = recvParticipant(bit, group, user) NOTE: bit = 1
recvCommand(user, group, auth, post, command, command arguments) NOTE: unchanged
recvPost(user, group, auth, post) NOTE: unchanged
recvModErase(group, user) = recvMods(left, group, mod) NOTE: left = true
recvModAdd(group, user) = recvMods(left, group, mod) NOTE: left = false
recvPostDelete(group, post) = recvDelete(group, post)
recvBan(group, user, mod) = recvBlocked(group, user, mod)
recvUnban(group, user, mod) = recvUnblocked(group, user mod)
recvLogout(group) = recvLogoutok(group)
recvLogin(group) = recvPwdok(group)
recvGroupClear(group) = recvClearall(group)
recvFlWarning(group) = recvShow_fw(group)
recvGroupBan(group) = recvShow_tb(group)
recvGroupBanUpdate(minutes, seconds) = recvTb(group, mins, secs)

PM's:

recvPMInit(group) = recvOK(group)
recvOfflinePM(user, pm) = recvMsgoff(group, user, pm)
recvPm(user, pm) = recvMsg(group, user, pm)
recvPMKick() = recvKickingoff(group)
