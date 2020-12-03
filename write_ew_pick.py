from obspy.core import UTCDateTime
import os

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

    else:
        print('Unkwnow probability to law mapping')
        wt = 0

    return(wt)


def __format_pick_scnl(wt,t0,s,n,c,l,pamp, dest, ew_vars):
#    global next_pick_number
    inst_id = ew_vars[0]
    mod_id = ew_vars[1]
    msg_type = ew_vars[2]
    next_pick_number = ew_vars[3]
    fm='?'
    # Write TYPE_PICK_SCNL message
    with open(os.path.join(dest, str('%06d.pick' %next_pick_number)), 'w') as f:
        print("%d %d %d %d %s.%s.%s.%s %c%1d %18s %ld %ld %ld"
            %(msg_type,mod_id,inst_id,
                next_pick_number,s,n,c,l,fm,wt,
                t0.strftime("%Y%m%d%H%M%S.%f")[:-3],pamp,pamp,pamp), file=f)
        f.close()
    print("%s.%s.%s.%s %s"
            %(s,n,c,l,t0.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]))
    if next_pick_number == 999999 :
        next_pick_number = 0
    else :
        next_pick_number += 1
    ew_vars[3] = next_pick_number
    return(ew_vars)



# Converts picks list into single TYPE_PICK_SCNL messages
# traces_stats : list of tr.stats for each channel
# picks : list of PhaseNet detections (idx_p, prob_p, idx_s, prob_s)
# dest : directory to write TYPE_PICK_SCNL messages
def write_ew_pick(traces_stats,picks,dest, ew_vars):
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
                ew_vars = __format_pick_scnl(wt, time, tr_stats.station, tr_stats.network,
                    tr_stats.channel, tr_stats.location, pamp, dest, ew_vars)
    return(ew_vars)
