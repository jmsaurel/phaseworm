from obspy.core import UTCDateTime
from obspy.clients import seedlink
from obspy.clients import fdsn
import time
from obspy.realtime import RtTrace
from obspy.clients.seedlink.easyseedlink import EasySeedLinkClient

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

net = 'QM'
sta = 'KNKL'
loc = '00'
chan = 'HH?'

rt_trace = RtTrace(max_length=120)

class MyClient(EasySeedLinkClient):
    def on_data(self, trace):
        rt_trace.append(trace, gap_overlap_check=True)

slinkRT = MyClient('195.83.188.34:18000')
slinkRT.select_stream(n,s,''.join((l,c)))


deb = time.time()
try :
    st_sl = slink.get_waveforms(net,sta,loc,chan,t0,ti)
    print(st_sl)
except :
    print('No data found from Seedlink')
end = time.time()
print('Seedlink request done in %.2f' %(end - deb))

deb = time.time()
try :
    st_ws = fdsnws.get_waveforms(net,sta,loc,chan,t0,ti)
    print(st_ws)
except :
    print('No data found from FDSN webservice')
end = time.time()
print('FDSNWS request done in %.2f' %(end - deb))



