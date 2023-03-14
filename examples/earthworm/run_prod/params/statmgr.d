#
#                    Status Manager Configuration File
#                             (statmgr.d)
#
#   This file controls the notifications of earthworm error conditions.
#   The status manager can send pager messages to a pageit system, and
#   it can also send email messages to a list of recipients.
#   Earthquake notifications are not handled by the status manager.
#   In this file, comment lines are preceded by #.
#
MyModuleId  MOD_STATMGR

#   <RingName> specifies the name of the transport ring to check for
#   heartbeat and error messages.  Ring names are listed in file
#   earthworm.h.  Example ->  RingName HYPO_RING
#
RingName    PICK_RING

#   If CheckAllRings is set to 1 then ALL rings startstop currently
#   knows about will be checked for status messages. The above
#   single RingName, however, still needs to be a valid ring name.
#   If you use CheckAllRings, you don't want to use any
#   copystatus modules. Note statmgr may not be able to keep up
#   on a system with a very busy ring, and you may need to
#   set CheckAllRings to 0 and go back to the old way of using copystatus
#   Note this defaults to OFF if not set in the config file.
CheckAllRings	1

# Debug is an optional flag (if not provided, defaults to 0 or off)
# for now there are 2 levels above off: 1 and 2
#Debug 1

#   <GetStatusFrom> lists the installations & modules whose heartbeats
#   and error messages statmgr should grab from transport ring:
#
#              Installation     Module           Message Types
GetStatusFrom  ${EW_INST_ID}   MOD_WILDCARD   # heartbeats & errors

#   <LogFile> sets the switch for writing a log file to disk.
#             Set to 1 to write a file to disk.
#             Set to 0 for no log file.
#             Set to 2 for module log file but no logging to stderr/stdout
#
LogFile   ${EWLOGFILE}

#   <heartBeatPageit> is the time in seconds between heartbeats
#   sent to the pageit system.  The pageit system will report an error
#   if heartbeats are not received from the status manager at regular
#   intervals.
#
heartbeatPageit  120

#   <pagegroup> is the pager group name.
#   The paging program maps this name to a list of pager recipients.
#   Between 1 and 10 pagegroup lines can be used (one is required).
#
pagegroup   earthworm-ops

#   Between 1 and 10 names of computers to use as a mail server.
#	   They will be tried in the order listed
#   This system must be alive for mail to be sent out.
#   This parameter is used by Windows NT only.
#
#   Syntax
#     MailServer  <serverName1>
#     MailServer  <serverName2>
#             ...
#     MailServer  <serverNameN>
#
MailServer  mailserver.your.org

#   Between 0 and 10 email recipients may be specified below.
#   These lines are optional.
#
#   Syntax
#     mail  <emailAddress1>
#     mail  <emailAddress2>
#             ...
#     mail  <emailAddressN>
#
#mail  earthworm-ops@your.org

# Mail program to use, e.g /usr/ucb/Mail (not required)
# If given, it must be a full pathname to a mail program
#
#MailProgram /usr/ucb/Mail


# Specify the "From" line for the email messages. (not required)
# If commented out, the email "From" field will be filled out
# with environment variables:  %USERNAME%@%COMPUTERNAME%.
# This parameter is used by Windows NT only.
#
#From username@thishost

#
# Subject line for the email messages. (not required)
#
Subject "This is an earthworm status message"

#
# Message Prefix - useful for paging systems, etc.
#    this parameter is optional
#
MsgPrefix "(("

#
# Message Suffix - useful for paging systems, etc.
#    this parameter is optional
#
MsgSuffix "))"

# new optional to squash annoying messages one might not care about
#DontReportUnknownModule 1


#   Now list the descriptor files which control error reporting
#   for earthworm modules.  One descriptor file is needed
#   for each earthworm module.  If a module is not listed here,
#   no errors will be reported for the module.  The file name of a
#   module may be commented out, if it is temporarily not to be used.
#   To comment out a line, insert # at the beginning of the line.
#
Descriptor  statmgr.desc
Descriptor  startstop.desc
Descriptor  binder_ew.desc
Descriptor  file2ew.desc
Descriptor  pkfilter.desc
Descriptor  eqassemble.desc

