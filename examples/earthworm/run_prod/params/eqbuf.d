#
#                 Eqbuf's Configuration File
#
#
MyModuleId  MOD_EQASSEMBLE     # Module id used to label the logfile.  Eqbuf is a
                           # descendent of the eqproc program.  All descendents
                           # of eqproc need to use eqproc's module id.
#
RingSize   10              # Buffer will hold RingSize items of size MAX_BYTES_PER_EQ
LogFile     ${EWLOGFILE}              # 0=no log; 1=log errors
                           # 2=write to module log but not to stderr/stdout
#PipeTo  "eqverify_assemble eqverify_assemble.d"  # The child program to be spawned by eqbuf
#PipeTo  "eqverify eqverify.d"  # The child program to be spawned by eqbuf
PipeTo  "eqcoda eqcoda.d"  # The child program to be spawned by eqbuf

