#import requests
import obspy
import numpy as np
#import matplotlib.pyplot as plt
from obspy.core import UTCDateTime
from obspy.clients.fdsn import Client
from obspy.clients import seedlink
import time
from app import predict,init_pred

from get_data import get_data
from earthworm import read_earthworm_conf, write_ew_pick

def main():
    #init model
    sess,model=init_pred()
    
    latency=30
    v=1
    while v==1:
        t0=UTCDateTime(2020,11,29,21,59,45)#time.time()
        ti=t0+30#UTCDateTime.now()-latency
        run_phasenet_2(ti,sess,model)
        t1=time.time()-t0
        print(UTCDateTime.now(),t1)
        v=0
        time.sleep(15-t1)

def run_phasenet_2(ti,sess,model):
    
    dired='./data/'
    
    
    # Directory where to write pick messages
    dir_pick_msg='/opt/phasenet/PICK_SCNL'
    
    # Some EarthWorm configuration values
    dir_ew_params='/opt/earthworm/run_prod/params'
    MyInstitutionID='INST_REVOSIMA'
    MyModuleID='MOD_PHASENET'
    nb_pick_keeper = '/tmp/next_pick_number'
    
    # Read some variables from earthworm config files
    ew_vars = read_earthworm_conf(dir_ew_params, MyInstitutionID, MyModuleID)
    ew_vars[3] = nb_pick_keeper
    
    filesta=open('listTerre.txt')
    liststa=filesta.readlines()
    Net=[liststa[i].rstrip().split(' ')[0] for i in range(len(liststa))]
    Sta=[liststa[i].rstrip().split(' ')[1] for i in range(len(liststa))]
    
    fs=100.0
    tw=30
    latency = 5
    
    #ti=UTCDateTime.now()-latency
    #ti=UTCDateTime.now()-latency
    #ti=UTCDateTime('2020-11-10 09:20:30')
    #ti=UTCDateTime.now()-latency
    t0=ti-tw
    #print(t0)
    
    fdsn = 'fdsnws://http://195.83.188.34:8080'
    seedlink = 'slink://195.83.188.34:18000'
    waveserver = 'waveserver://127.0.0.1:16000'
    #data_source = 'sds:///data/SDS'
    chan_list = ['HH?', 'EH?', 'SH?', 'HN?', 'BH?']
    
    for ista in range(len(Sta)):
        print(Sta[ista])
        if UTCDateTime.now() - ti > 600 :
            st = get_data(Net[ista],Sta[ista],t0,ti,chan_list,fdsn)
        else :
            st = get_data(Net[ista],Sta[ista],t0,ti,chan_list,waveserver)
    #        st = get_data(Net[ista],Sta[ista],t0,ti,chan_list,seedlink)
    
    
        #print(st)
        if len(st)==0:
            continue
        st.merge(method=1,fill_value='interpolate')
        #st.detrend(type='demean')
        #st.taper(0.005,type='hamming')
        print(st)
        try:
            st.interpolate(sampling_rate=fs)
        except:
            continue
        st=st.slice(starttime=t0,endtime=ti)
        st=st.sort()
        print(st)
        data=[]
        tr_statistics=[]
        if len(st)==3:
            for ch in ['E','N','Z']:
                tr=st.select(channel='*'+ch)[0]
                #print(tr.stats)
                #data.append(st.select(channel='*'+ch)[0].data)
                if tr.stats.sampling_rate*tw+1 != tr.stats.npts:
                    continue
                data.append(tr.data[:-1])
                tr_statistics.append(tr.stats)
            #print(np.shape(data))
            #moi
            if len(data)!=3:
                continue
        else:
            continue
            data.append(np.zeros(np.int(fs*tw)))
            data.append(np.zeros(np.int(fs*tw)))
            tr=st.select(channel='*'+'Z')[0]
            #print(tr)
            if tr.stats.sampling_rate*tw+1 != tr.stats.npts:
                continue
            data.append(tr.data[:-1])
            tr_statistics.append(tr.stats)
            tr_statistics.append(tr.stats)
            tr_statistics.append(tr.stats)
        data=np.array(data)
    
        #resp=1
        picks=predict(data,sess,model)
        print(st[0].stats.station,picks)
        continue
        npicks = write_ew_pick(tr_statistics,picks,dir_pick_msg, ew_vars)
        print('%d picks written' %npicks)
        #moi
    return


if __name__ == "__main__":
    main()


print('nodata')
moi
### Start running the model first:
### FLASK_ENV=development FLASK_APP=app.py flask run

def read_data(mseed):
    data = []
    mseed = mseed.sort()
    for c in ["E", "N", "Z"]:
        data.append(mseed.select(channel="*"+c)[0].data)
    return np.array(data).T

## prepare some test data
mseed = obspy.read()
data = []
for i in range(10): 
    data.append(read_data(mseed))
data = {"data": np.array(data).tolist()}

## run prediction
resp = requests.post("http://localhost:5000/predict", json=data)
picks = resp.json()["picks"]

## Convert predictions to TYPE_PICK_SCNL messages
# station_tr_stats : list of tr.stats
# picks : result of prediction
# dir_pick_msg : directory where to push pick messages
write_ew_pick(tr_statistics,picks,dir_pick_msg)


## plot figure
plt.figure()
plt.plot(np.array(data["data"])[0,:,1])
ylim = plt.ylim()
plt.plot([picks[0][0][0], picks[0][0][0]], ylim, label="P-phase")
plt.text(picks[0][0][0], ylim[1]*0.9, f"{picks[0][1][0]:.2f}")
plt.plot([picks[0][2][0], picks[0][2][0]], ylim, label="S-phase")
plt.text(picks[0][2][0], ylim[1]*0.9, f"{picks[0][1][0]:.2f}")
plt.legend()
plt.savefig("test.png")
