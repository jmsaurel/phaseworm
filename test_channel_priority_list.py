from obspy.core import UTCDateTime
from obspy.clients import seedlink
from obspy.clients import fdsn
import time

latency = 600

ti = UTCDateTime.now() - latency
print(ti)
t0 = ti - 30

try :
    slink = seedlink.Client('195.83.188.34', timeout=2)
except :
    print('Cannot connect to seedlink server')
    exit()

try :
    fdsnws = fdsn.Client('http://195.83.188.34:8080')
except :
    print('Cannot connect to FDSN webservice')
    exit()

#net = 'ED'
#sta = 'MCHI'
#loc = '00'
#chan = 'BH?'

net = ['QM', '1T', 'ED', '1T', 'AM']
sta = ['KNKL', 'PMZI', 'MCHI', 'MTSB', 'R0CC5']
loc = '*'
chan = '*'
chan_priority_list = ['HH?', 'EH?', 'SH?', 'HN?', 'BH?']

for n,s in zip(net,sta) :
    #n = net[i]
    try :
        st = slink.get_waveforms(n,s,"*","*",t0,ti)
    except :
        print('No data found from Seedlink')
    print(st)
    for c in chan_priority_list :
        s = st.select(channel=c) 
        if s :
            print("%s channel found, process data" %(c))
            print(s)
            break
        else :
            print("%s channels not found, try next channel" %(c))
