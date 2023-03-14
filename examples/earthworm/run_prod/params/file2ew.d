# file2ew.d
#
# Picks up files from a specified directory, converts the contents 
# to an Earthworm message and places  it into a message ring. The type
# of message produced is configurable by the suffix of the filename.
#
# Option to save (to subdir ./save) or delete the file afterwards.
# If it has trouble converting a file, it saves it to subdir ./trouble. 
# Maintains its own local heartbeat and also monitors the peer's
# heartbeat via a file. Complains if the peer's expected heartbeat
# interval is exceeded; announces resumption of peer's heartbeat.

# Basic Module information
#-------------------------
MyModuleId        MOD_FILE2EW      # module id 
RingName          PICK_RING	       # shared memory ring for output
HeartBeatInterval 30               # seconds between heartbeats to statmgr

LogFile           ${EWLOGFILE}     # 0 log to stderr/stdout only; 
                                   # 1 log to stderr/stdout and disk;
                                   # 2 log to disk module log only.

Debug             0                # 1=> debug output. 0=> no debug output

# Data file manipulation
#-----------------------
GetFromDir      ${PHASE_NET_OUT}   # look for files in this directory
CheckPeriod     0.5                # sleep this many seconds between looks
OpenTries       2                  # How many times we'll try to open a file 
OpenWait        100                # Milliseconds to wait between open tries
SaveDataFiles   1                  # 0 = remove files after processing
                                   # non-zero = move files to save subdir
                                   #            after processing  
LogOutgoingMsg  0                  # If non-zero, write contents of each 
                                   #   outgoing msg to the daily log.

  

# Peer (remote partner) heartbeat manipulation
#---------------------------------------------
PeerHeartBeatFile  localhost  HEARTBT.TXT  0 
                                   # PeerHeartBeatFile takes 3 arguments:
                                   # 1st: Name of remote system that is 
                                   #   sending the heartbeat files.
                                   # 2nd: Name of the heartbeat file. 
                                   # 3rd: maximum #seconds between heartbeat 
                                   #   files. If no new PeerHeartBeatFile arrives
                                   #   in this many seconds, an error message will
                                   #   be sent.  An "unerror message" will be
                                   #   sent after next heartbeat file arrives
                                   #   If 0, expect no heartbeat files.
                                   # Some remote systems may have multiple 
                                   # heartbeat files; list each one in a
                                   # seperate PeerHeartBeatFile command
                                   # (up to 5 allowed).

#PageOnLostPeer technician          # Optional command: Name of group to page 
                  	           #   if PeerHeartBeatFile is late. This allows
                                   #   pages to be sent to groups other than 
                                   #   those listed in statmgr.d. Up to 5 
                                   #   PageOnLostPeer commands can be used.
                                   # Must run telafeeder on same system to 
                                   #   actually get the pages sent.

LogHeartBeatFile 0                 # If non-zero, write contents of each
                                   #   heartbeat file to the daily log.


# Commands specific to file2ew
#-----------------------------

MaxSuffixType 5                    # Optional command.  Set the maximum number
                                   #   of file suffix/message type pairs to
                                   #   configure here (default=5)

# The filename suffix will determine the Earthworm message type
# (and optionally the Earthworm installation id) that file2ew will 
# use when placing the contents of the file into the Earthworm ring.
# If the installation is ommitted, file2ew will use the local
# installation id.

#           suffix   EW MsgType           EW Installation (optional)
#           ------   ----------------     --------------------------
SuffixType  .pick     TYPE_PICK_SCNL      

