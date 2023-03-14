#-----------------------------------------------------------------------------
#                    Earthworm Common Variables
#
#  Define values for the Earthworm Common variables.
#  Values of the variables already set within the shell environment will be
#  overwritten by the declarations contained within this file.
#
#  Variables declared inside this file can be recalled within all .d file using
#  the following syntax:   ${VARIABLE_NAME}
#  The respective values will be expanded within the original .d file.
#  The variable expansion for this file is implemented only from the
#  environment shell, avoiding recursivity.
#
#  An example copy of earthworm_commonvars.d resides in the vX.XX/environment
#  directory of this Earthworm distribution.
#  A copy of earthworm_commonvars.d should be placed in your EW_PARAMS
#  directory.
#
#  Syntax:
#          SetEnvVariable VARIABLE_NAME VARIABLE_VALUE
#          SetEnvVariable VARIABLE_NAME "VARIABLE_VALUE"
#
#  VARIABLE_NAME can contain only characters [A-Za-Z0-9_] and it must start
#  with a nonnumeric character.
#  VARIABLE_VALUE can contain all characters execpt for '}',
#                 use quote when it contains spaces.
#  The maximum length for VARIABLE_NAME and VARIABLE_VALUE is 255 characters.
#
#  Best practice:
#     - Avoid to declare EW_HOME, EW_VERSION, EW_LOG, EW_PARAMS, ...
#
#  Examples:
#
#     1) SetEnvVariable MYDERIVEDVAR "${ENVVARFROMSHELL}/myfile"
#        # Value for ENVVARFROMSHELL will be substituted only if the variable
#        # has been set within the shell environment before launching
#        # the module startstop.
#
#     2) SetEnvVariable MYVAR1 xxxxxxx
#        SetEnvVariable MYVAR2 ${MYVAR1}
#        # MYVAR2 will not expanded with variable  from this file, but only
#        # from the shell environment if MYVAR1 has been set outside from here.
#
#-----------------------------------------------------------------------------

SetEnvVariable EW_INST_ID INST_UNKNOWN
SetEnvVariable STATIONFILE revosima.hinv
SetEnvVariable EWLOGFILE 2
SetEnvVariable PHASE_NET_OUT ../PICK_SCNL/
SetEnvVariable ROOT_NLL /opt/earthworm/run_prod/data/nll/


