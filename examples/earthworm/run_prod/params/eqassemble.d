# This is Eqassemble's Parameter File

# Basic Earthworm setup:
#-----------------------
 MyModuleId   MOD_EQASSEMBLE    # Module id for this instance of eqassemble
 RingName     PICK_RING     # Ring to get input from
 HeartbeatInt 30            # seconds between heartbeats to statmgr
 LogFile      ${EWLOGFILE}  # 0 = turn off disk log file; 
                            # 1 = turn on disk log
                            # 2 = write disk log but not to stderr/stdout

# optional flag to see link messages
#Debug

# List the message logos to grab from transport ring
#               Installation       Module          Message Types
#-----------------------------------------------------------------
 GetPicksFrom   ${EW_INST_ID}    MOD_PKFILTER    # pick2k & coda2k
 GetAssocFrom   ${EW_INST_ID}       MOD_BINDER      # quake2k & link2k
  
# Send output to the following command (uncomment one):
#------------------------------------------------------
PipeTo "eqbuf eqbuf.d"     # buffer events for downstream modules
#PipeTo "eqcoda eqcoda.d"   # do coda weighting & extrapolation
#PipeTo "log_everything"    # end chain here for debugging

# Load station list
#------------------
 maxsite     3500
 site_file   ${STATIONFILE}

# Load crustal model
# Refer to file containing "lay" commands, or list them here
#-----------------------------------------------------------
@ALav_model.vel        # contents of ncal_model.d follow:

# Set pick/quake FIFO lengths (must be >= binder's fifo lengths)
#---------------------------------------------------------------
 pick_fifo_length  1000  # optional: default = 1000
 quake_fifo_length  100  # optional: default = 100

# Control how/when events are reported
#-------------------------------------
 ReportS      1     # 0 = do not send S-phases to next process
                    # non-zero = do send S-phases to next process
 HypCheckInterval  1.0	# interval (sec) at which to check all hypocenters   
                    #   to see if it's time to report an event

 UseS # an OPTIONAL flag to indicate S phases should be used in rules below,
#        otherwise just P phases are used in counts 

# Rules for reporting events
#---------------------------
# At least one of these rules must be given; there are no defaults
# Syntax:
#	PrelimRule numPhases
#		Event2K message released with version 0 when event has
#		<numPhases> P phases associated.
#	RapidRule numPhases seconds SinceOrigin
#     or
#	RapidRule numPhases seconds SinceDetection
#		Event2K message released with version 1 <seconds> since
#		origin or detection time provided <numPhases> P phases 
#		associated.
#	FinalRule numPhases seconds secQualifier [WaitForCodas]
#		Event2K message released with version 2 when a timer has
#		expired after <seconds>, has <numPhases> P phases associated,
#		and optionally after codas have arrived. 
# 		seqQualifier specifies when the timer starts. Allowed values:
#		SinceStable: time starts at most recent binder solution,
#		   allowing binder solution to become stable
#		SinceOrigin: timer starts at origin time
#		SinceDetection: timer starts at receipt of first binder
#		   for this event.
#
# Codas are reported only with the FinalRule and only if the
# WaitForCodas flag is included in the FinalRule command
#
#PrelimRule    10
#RapidRule     5 10 SinceDetection
FinalRule     4 5 SinceStable
#FinalRule     4 20 SinceDetection

# If we are going to wait for codas, and some picks are imported from
# other Earthworm Installations, eqassemble can optionally wait for codas
# from those other installations with one or more of:
# CodaFromInst InstId
# You do not need to list your own Inst ID.
# CodaFromInst is ignored if the FinalRule does not wait for codas.
CodaFromInst ${EW_INST_ID

# DataSrc: single character to indicate the source of phase data
DataSrc    W

# MaxPhasesPerEq: restrict the number of phases to be reported for
# the RapidRule and FinalRule to this value. Cannot be set greater than
# the Earthworm limit of 250, which is also the default for this parameter.
MaxPhasesPerEq 249

# Control debugging info to log
#------------------------------
 WaifTolerance   4.0  # tolerance (sec) for noting waif picks for
		      #   in log file. (optional: default = 4.0)

