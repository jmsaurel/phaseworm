from obspy.core import UTCDateTime
from obspy.clients import seedlink
from obspy.clients import earthworm
from obspy.clients import fdsn
from obspy.clients.filesystem import sds
from obspy.core.stream import Stream


# Get data from an SDS local archive
# sdsclient : SDS Client
# net : network code (string)
# sta : station code (string)
# chan_priority_list : list of channels by decreasing priority order
# t0 : start time of data request
# ti : end time of data request
# Return an obspy Stream()
def _get_data_sds(sdsclient, net, sta, chan_priority_list, t0, ti):
    try :
        st = sdsclient.get_waveforms(net,sta,"*","*",t0,ti)
    except :
        s = Stream()
    else :
        for c in chan_priority_list:
            s = st.select(channel=c) 
            if s :
                break
    finally :
        return s

# Get data from an EarthWorm WaveServerV
# ewclient : WaveServerV Client
# net : network code (string)
# sta : station code (string)
# chan_priority_list : list of channels by decreasing priority order
# t0 : start time of data request
# ti : end time of data request
# Return an obspy Stream()
def _get_data_ew(ewclient, net, sta, chan_priority_list, t0, ti):
    for c in chan_priority_list:
        try :
            available_data = ewclient.get_availability(net,sta,"*",c)
        except :
            st = Stream()
        else :
            if available_data:
                loc = str(available_data[0][2])
                st = ewclient.get_waveforms(net,sta,loc,c,t0,ti)
                break
            else :
                st = Stream()
    return st


# Get data from a Seedlink server
# slclient : Seedlink Client
# net : network code (string)
# sta : station code (string)
# chan_priority_list : list of channels by decreasing priority order
# t0 : start time of data request
# ti : end time of data request
# Return an obspy Stream()
def _get_data_slink(slclient, net, sta, chan_priority_list, t0, ti):
    for c in chan_priority_list:
        try :
            available_chans = slclient.get_info(net,sta,"*",c, level='channel')
        except :
            st = Stream()
        else :
            if available_chans:
                loc = str(available_chans[0][2])
                st = slclient.get_waveforms(net,sta,loc,c,t0,ti)
                break
            else :
                st = Stream()
    return st

# Get data from and FDSN webservice
# wsclient : FDSN webservice Client
# net : network code (string)
# sta : station code (string)
# chan_priority_list : list of channels by decreasing priority order
# t0 : start time of data request
# ti : end time of data request
# Return an obspy Stream()
def _get_data_fdsn(wsclient, net, sta, chan_priority_list, t0, ti):
    try :
        st = wsclient.get_waveforms(net,sta,"*","*",t0,ti)
    except :
        s = Stream()
    else :
        for c in chan_priority_list:
            s = st.select(channel=c) 
            if s :
                break
    finally :
        return s


# Get data from best source
# net : network code (string)
# sta : station code (string)
# t0  : start time of data request
# ti  : end time of data request
# chan_priority_list : list of channels by decreasing priority
# Return on obspy Stream object
def get_data(net,sta,t0,ti,chan_priority_list,data_source):
    data_type = data_source.split('://',1)[0]
    data_server = data_source.split('://',1)[1]

    if data_type == 'waveserver' :
        # ew_ws = '127.0.0.1:16000'
        ew_ws = data_server.split(':')
        client = earthworm.Client(ew_ws[0], port=int(ew_ws[1]), timeout=2.0)
        try :
            client.get_availability()
        except :
            #print('Error : failed to connect to %s WaveServerV' %ew_ws)
            st = Stream()
        else :
            st = _get_data_ew(client,net,sta,chan_priority_list,t0,ti)
        finally :
            return st

    elif data_type == 'slink' :
        # slink = '195.83.188.34:18000'
        slink = data_server.split(':')
        client = seedlink.Client(slink[0], port=int(slink[1]), timeout=2.0)
        try :
            client.get_info()
        except :
            #print('Error : failed to connect to %s Seedlink server' %slink)
            return Stream()
        else :
            st = _get_data_slink(client,net,sta,chan_priority_list,t0,ti)
        finally :
            return st
    
    elif data_type == 'sds' :
        # SDS = '/data/SDS'
        SDS = data_server
        try :
            client = sds.Client(sds_root=SDS)
        except :
            #print('Error : failed to find %s directory' %SDS)
            st = Stream()
        else :
            st = _get_data_slink(client,net,sta,chan_priority_list,t0,ti)
        finally :
            return st

    elif data_type == 'fdsnws' :
        # fdsn_ws = 'http://195.83.188.34:8080'
        try :
            client = fdsn.Client(data_server)
        except :
            #print('Error : failed to connect to %s FDSN webservice' %fdsn_ws)
            st = Stream()
        else :
            st = _get_data_fdsn(client,net,sta,chan_priority_list,t0,ti)
        finally :
            return st

    else :
        #print('Error : unknown <%s> server type' %data_type)
        return Stream()

