import os

# Read earthworm params file
# Set global variables for InstitutionID, ModuleID and MessageType
def read_earthworm_conf(EW_params_dir, MyInstId, MyModId):
#    global inst_id
#    global mod_id
#    global msg_type

    # Search InstitutionID and MessageType in earthworm_global.d file
    file = os.path.join(EW_params_dir, 'earthworm_global.d')
    try :
        f = open(file, 'r', encoding='latin-1')
        for line in f:
            if MyInstId in line:
                inst_id = int(line.split()[2])
            elif 'TYPE_PICK_SCNL' in line:
                msg_type = int(line.split()[2])
        f.close()
    except :
        print('ERROR : unable to open file %s' %file)

    # Search ModuleID in earthworm.d file
    file = os.path.join(EW_params_dir, 'earthworm.d')
    try :
        f = open(file, 'r', encoding='latin-1')
        for line in f:
            if MyModId in line:
                mod_id = int(line.split()[2])
                break
        f.close()
    except :
        print('ERROR : unable to open file %s' %file)

    # If InstitutionID not found, set to INST_UNKNOWN = 255
    try :
        inst_id
    except :
        print('WARNING : %s Institution not found, set to INST_UNKNOWN' %MyInstId)
        inst_id = 255

    # If ModuleID not found, set to MOD_WILDCARD = 0
    try :
        mod_id
    except :
        print('WARNING : %s Module not found, set to MOD_WILDCARD' %MyModId)
        mod_id = 0

    # If MessageType not found, exit with error
    try :
        msg_type
    except :
        print('ERROR : TYPE_PICK_SCNL message type not found, exit')
        exit(0)

    next_pick_number = 0
    ew_vars = [inst_id, mod_id, msg_type, next_pick_number]
    return(ew_vars)
