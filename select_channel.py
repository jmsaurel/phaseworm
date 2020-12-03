from obspy.core import UTCDateTime
from obspy.clients import seedlink
from obspy.clients import fdsn
import time
from obspy.core.stream import Stream

def select_channel(net,sta,ti,t0):

    #latency = 600
    
    #ti = UTCDateTime.now() - latency
    #print(ti)
    #t0 = ti - 30
    
    if UTCDateTime.now() - ti > 600 :
        try :
            client = fdsn.Client('http://195.83.188.34:8080')
        except :
            print('Cannot connect to FDSN webservice, switch to Seedlink')
            client = seedlink.Client('195.83.188.34', timeout=2)
    else :
        client = seedlink.Client('195.83.188.34', timeout=2)
    
    #try :
    #    slink = seedlink.Client('195.83.188.34', timeout=2)
    #except :
    #    print('Cannot connect to seedlink server')
    #    return Stream()#exit()

    #try :
    #    fdsnws = fdsn.Client('http://195.83.188.34:8080')
    #except :
    #    print('Cannot connect to FDSN webservice')
    #    exit()
    
    #net = 'ED'
    #sta = 'MCHI'
    #loc = '00'
    #chan = 'BH?'
    
    #net = ['QM', '1T', 'ED', '1T', 'AM']
    #sta = ['KNKL', 'PMZI', 'MCHI', 'MTSB', 'R0CC5']
    loc = '*'
    chan = '*'
    chan_priority_list = ['HH?', 'EH?', 'SH?', 'HN?', 'BH?']
    
    #for i,s in enumerate(sta) :
    #n = net[i]
    try :
#        st = slink.get_waveforms(net,sta,"*","*",t0-30,ti+30)
        st = client.get_waveforms(net,sta,"*","*",t0-30,ti+30)
    except :
        print('No data found from Seedlink')
        st=Stream()
        return st
    #print(st)
    for c in chan_priority_list :
        s = st.select(channel=c) 
        if s :
            print("%s channel found, process data" %(c))
            #print(s)
            return s
            #break
        else :
            print("%s channels not found, try next channel" %(c))
    return Stream()




