#
# This is eqcoda's parameter file
#
 MyModuleId  MOD_EQASSEMBLE  # module id to label logfile  with.
                         # Note: eqcoda is part of a mega-module which is
                         # ultimately started by the program eqproc.  All
                         # child processes of this mega-module need to use the
                         # same module id (thus use eqproc's module id).

 LogFile       ${EWLOGFILE}         # 0=log to stderr/stdout only
                         # 1=log to disk and stderr/stdout
                         # 2=log to disk only
 
 LogArcMsg     1         # Optional command; default LogArcMsg=0
                         # 0=do not log output TYPE_HYP2000ARC msg
                         # non-zero=write ARC msg to log file

 LabelAsBinder 0         # 0=label phases as generic P and S;
                         # non-zero = label phases as binder did

 LabelVersion  0         # Optional command; default LabelVersion=1
                         # 0 = write a blank in the version field of the 
                         #   summary line of the TYPE_HYP2000ARC msg 
                         # non-zero = use the version number passed from
                         #   eqproc,eqprelim on the summary line.

# PipeTo sends eqcoda's output to one of these three modules:
#   log_everything  debug tool which writes all of eqcoda's
#                   output to the screen and to a file in the
#                   EW_PARAMS directory named "log_everything".
#   eqverify        performs some tests to determine if the event
#                   is noise or a real earthquake.
#   hyp2000_mgr     locates event and calculates coda duration mag.
#-------------------------------------------------------------------
#PipeTo "log_everything"
#PipeTo "eqverify eqverify.d"
# PipeTo "hyp2000_mgr hyp2000_mgr.d ncal2000.hyp"
PipeTo "nll_mgr nll_mgr.d"

# StaFile loads per-channel parameters (added in v5.1).
# Use same station list as pick_ew.  eqcoda uses only the
# SCNL, CodaTerm and ClipCount fields and ignores the rest.
#--------------------------------------------------------------
# StaFile ${PICK_EWFILE}

# Obsolete commands (in v5.1 and higher)
#--------------------------------------------------------------
# Define the coda termination level (counts) and clipping
# levels for all channels.  Default values are appropriate for
# Earthworm 12-bit data.
# coda_term     49.14   # same as CodaTerm in pick_ew stationfile
# coda_clip       820
# p_clip1         984
# p_clip2        1148
 
