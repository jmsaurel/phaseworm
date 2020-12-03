from obspy.core import UTCDateTime
import os, stat
import shutil
import tempfile

# Read earthworm params file
# Set global variables for InstitutionID, ModuleID and MessageType
# EW_params_dir : directory where to find active .d conf files
# MyInstID : institution ID to find in earthworm_global.d
# MyModID : module ID to find in earthworm.d
# Return ew_vars, list with institution ID, module ID and message type values
#  and pick number keeper file
def read_earthworm_conf(EW_params_dir, MyInstID, MyModID):

    # Search InstitutionID and MessageType in earthworm_global.d file
    file = os.path.join(EW_params_dir, 'earthworm_global.d')
    try :
        f = open(file, 'r', encoding='latin-1')
        for line in f:
            if MyInstID in line:
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
            if MyModID in line:
                mod_id = int(line.split()[2])
                break
        f.close()
    except :
        print('ERROR : unable to open file %s' %file)

    # If InstitutionID not found, set to INST_UNKNOWN = 255
    try :
        inst_id
    except :
        print('WARNING : %s Institution not found, set to INST_UNKNOWN' %MyInstID)
        inst_id = 255

    # If ModuleID not found, set to MOD_WILDCARD = 0
    try :
        mod_id
    except :
        print('WARNING : %s Module not found, set to MOD_WILDCARD' %MyModID)
        mod_id = 0

    # If MessageType not found, exit with error
    try :
        msg_type
    except :
        print('ERROR : TYPE_PICK_SCNL message type not found, exit')
        exit(0)

    ew_vars = [inst_id, mod_id, msg_type, '']
    return ew_vars


# Converts PhaseNet probabilities to Hypo weigths
def __proba_to_wt(proba,law):

    if law == 'a':
        wt = -4.29 * proba + 4.29
        if proba < 0.3:
            wt = 3

    elif law == 'b':
        wt = -2.857 * proba + 2.857
        if proba < 0.3:
            wt = 3

    elif law == 'linear':
        wt = 3 * (1 - proba)

    elif law == 'taped_linear':
        if proba < 0.3:
            wt = 3
        else:
            wt = 3 * (1 - proba)

    elif law == 'all_equal':
        if proba < 0.3:
            wt = 3
        else:
            wt = 0

    else:
        print('Unkwnow probability to law mapping')
        wt = 0

    return(wt)


# Format and write TYPE_PICK_SCNL message
# wt : pick weigth (0-4)
# t0 : pick time (UTCDateTime)
# s  : station code (string)
# n  : network code (string)
# c  : channel code (string)
# l  : location code (string)
# pamp : pick amplitude (int)
# dest : directory to write message in
# ew_vars : list of EarthWorm variables
# Returns 1 if message successfully written
def __format_pick_scnl(wt,t0,s,n,c,l,pamp, dest, ew_vars):
    inst_id = ew_vars[0]
    mod_id = ew_vars[1]
    msg_type = ew_vars[2]
    pick_num_keeper_file = ew_vars[3]
    fm='?'

    # Read pick number from keeper file
    if os.path.exists(pick_num_keeper_file) :
        with open(pick_num_keeper_file,'r') as f:
            next_pick_number = int(f.readline())
            f.close()
    else :
        with open(pick_num_keeper_file,'w') as f:
            next_pick_number = 0
            f.write(str(next_pick_number))
            f.close()

    result = 0

    # Write TYPE_PICK_SCNL message
    msg = str("%d %d %d %d %s.%s.%s.%s %c%1d %18s %d %d %d"
            %(msg_type,mod_id,inst_id,
            next_pick_number,s,c,n,l,fm,wt,
            t0.strftime("%Y%m%d%H%M%S.%f")[:-3],pamp,pamp,pamp))
    fd, tmpfile = tempfile.mkstemp()
    # os.write(fd,msg)
    # os.fsync(fd)
    os.close(fd)
    with open(tmpfile, 'w') as f:
        # f.write("%d %d %d %d %s.%s.%s.%s %c%1d %18s %d %d %d"
        #     %(msg_type,mod_id,inst_id,
        #         next_pick_number,s,c,n,l,fm,wt,
        #         t0.strftime("%Y%m%d%H%M%S.%f")[:-3],pamp,pamp,pamp))
        f.write(msg)
        f.close()
#    os.chmod(tmpfile,stat.S_IROTH)
    pick_msg = os.path.join(dest, str('%06d.pick' %next_pick_number))
    shutil.copyfile(tmpfile,pick_msg)
    os.remove(tmpfile)
    result = 1
    if next_pick_number == 999999 :
        next_pick_number = 0
    else :
        next_pick_number += 1

    # Update pick number in keeper file
    with open(pick_num_keeper_file,'w') as f:
        f.write('%06d' %next_pick_number)
        f.close()

    return result



# Converts picks list into single TYPE_PICK_SCNL messages
# traces_stats : list of tr.stats for each channel
# picks : list of PhaseNet detections (idx_p, prob_p, idx_s, prob_s)
# dest : directory to write TYPE_PICK_SCNL messages
# ew_vars : list of variables read from EarthWorm conf files
# Returns number of picks successfully written
def write_ew_pick(traces_stats, picks, dest, ew_vars):
    npicks = 0
    for pks in picks:
        # P picks are on colunms 0 and 1 (k=0)
        # S picks are on columns 2 and 3 (k=2)
        for k in 0,2:
            # Iterate over picks
            for i, idx in enumerate(pks[k]):
                prob = pks[k+1][i]
                # Iterate over traces statistics to find vertical channel
                if k == 0:
                    for stats in traces_stats:
                        if (stats.channel.find('Z')>0
                                or stats.channel.find('3')>0):
                            tr_stats = stats
                            break
                    # Fixed fake P-pick amplitude
                    pamp = 100
                elif k == 2:
                    for stats in traces_stats:
                        if (stats.channel.find('N')>0
                                or stats.channel.find('2')>0
                                or stats.channel.find('E')>0
                                or stats.channel.find('1')>0):
                            tr_stats = stats
                            break
                    # Fixed fake S-pick amplitude
                    pamp = 400
                # Calculate pick time from trace starttime, sampling rate and index
                time = tr_stats.starttime + tr_stats.delta * idx
                # Convert PhaseNet probability to Hypo weight
                wt = __proba_to_wt(prob,'a')
                # Write TYPE_PICK_SCNL message
                npicks += __format_pick_scnl(wt, time, tr_stats.station, tr_stats.network,
                    tr_stats.channel, tr_stats.location, pamp, dest, ew_vars)
    return npicks


