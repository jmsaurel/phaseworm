# pkfilter configuration file

# Basic Earthworm setup:
#------------------------
 MyModuleId   MOD_PKFILTER    # module id for this instance of pkfilter 
 InRing       PICK_RING       # shared memory ring for input
 OutRing      PICK_RING # shared memory ring for output
 HeartbeatInt 30              # seconds between heartbeats
 LogFile      ${EWLOGFILE}               # 0 log to stderr/stdout only 
                              # 1 log to stderr/stdout and to disk file
                              # 2 log to disk file only
 Debug        1

# List the message logos to grab from InRing, WILDCARDs permitted.
# Multiple "GetLogo" commands are allowed, with no hardcoded limit.
#         Installation    Module      Message Types
#-----------------------------------------------------------------
 GetLogo  ${EW_INST_ID}  MOD_FILE2EW # TYPE_PICK_SCNL & TYPE_CODA_SCNL
                                      # TYPE_PICK2K & TYPE_CODA2K

# Pick Filtering Parameters
#--------------------------
 PickHistory          10      # Keep track of this many picks which have
                             # made it thru the filter for each station.

 PickTolerance        0.05    # If pick times are within this many seconds of
                             # each other, they are "duplicates."

 OlderPickAllowed     1      # 0=reject any non-duplicate pick whose 
                             #   timestamp is earlier than the youngest 
                             #   passed pick for this station.
                             # 1=accept a non-duplicate pick whose timestamp
                             #   is earlier than the youngest passed pick,
                             #   but place a limit on how old it can be.
                             #   Must also use the "OlderPickLimit" command.
                             # 2=accept any non-duplicate pick whose 
                             #   timestamp is earlier than the youngest   
                             #   passed pick.

 OlderPickLimit       60     # Required only if OlderPickAllowed = 1
                             # Accept an pick whose timestamp is between
                             # PickTolerance and OlderPickLimit sec     
                             # earlier than the youngest passed pick
                             # from this station.

 DuplicateOnQuality   1      # If non-zero, transfer a duplicate when its
                             #  quality is better than the original.

 QualDiffAllowed      1      # Required quality difference for later pick to
                             # be allowed to pass as a duplicate.
                             #  0 means any pick greater than current pick
                             #  1 means a pick of 1 replaces a pick of 3 
                             #  2 means a pick of 0 replaces a pick of 3 
                             #  3 is invalid because it is equivalent to 
                             #    turning off the duplicate on quality test 

# List of Allowed Components
#---------------------------
# If you want ALL component codes to be eligible to pass thru 
# pkfilter, comment out all "AllowComponent" commands.
# If you want to limit which component codes pass thru pkfilter,
# use one "AllowComponent" command for each allowed component code.
# AllowComponent   VDZ

# Coda Filtering Parameters
#--------------------------
 CodaFilter       2          # Possible coda filtering values:
                             #  0 = allow no codas thru filter
                             #  1 = allow only codas which match passed
                             #      picks to pass thru filter 
                             #  2 = allow all codas thru

# Optional commands:
#-------------------
 MaxMessageSize   128        # length (bytes) of largest msg to be processed
                             # from InRing.  Default=MAX_BYTES_PER_EQ

 UseOriginalLogo  0          # 0  apply pkfilter's logo to any messages that
                             #    pass the filter test (normal Earthworm behavior)
                             # non-zero means apply the original logo to any
                             #    messages that pass the filter test.  This
                             #    also requires that InRing and OutRing be 
                             #    different to avoid "missed message" or
                             #    "sequence gap" storms in pick-reading modules.
