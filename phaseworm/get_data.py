"""Module to provide data from various clients."""
# from obspy.core import UTCDateTime
# from obspy.clients import seedlink
# from obspy.clients import earthworm
# from obspy.clients import fdsn
# from obspy.clients.filesystem import sds
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
    try:
        st_all = sdsclient.get_waveforms(net, sta, "*", "*", t0, ti)
    except Exception:
        st_all = Stream()
    for c in chan_priority_list:
        st = st_all.select(channel=c)
        if st:
            break
    return st


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
        try:
            available_data = ewclient.get_availability(net, sta, "*", c)
        except Exception:
            st = Stream()
            available_data = []
        if available_data:
            loc = str(available_data[0][2])
            st = ewclient.get_waveforms(net, sta, loc, c, t0, ti)
            break
        else:
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
        try:
            available_chans = slclient.get_info(
                                net, sta, "*", c, level='channel')
        except Exception:
            st = Stream()
            available_chans = []
        if available_chans:
            loc = str(available_chans[0][2])
            st = slclient.get_waveforms(net, sta, loc, c, t0, ti)
            break
        else:
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
    try:
        st_all = wsclient.get_waveforms(net, sta, "*", "*", t0, ti)
    except Exception:
        st_all = Stream()
    for c in chan_priority_list:
        st = st_all.select(channel=c)
        if st:
            break
    return st


# Get data from best source
# net : network code (string)
# sta : station code (string)
# t0  : start time of data request
# ti  : end time of data request
# chan_priority_list : list of channels by decreasing priority
# Return on obspy Stream object
def get_data_from_client(net, sta, t0, ti, chan_priority_list, cl, data_type):
    """Get snippet of data for net.sta station from cl Client."""
    if data_type == 'waveserver':
        st = _get_data_ew(cl, net, sta, chan_priority_list, t0, ti)
        return st

    elif data_type == 'slink':
        st = _get_data_slink(cl, net, sta, chan_priority_list, t0, ti)
        return st

    elif data_type == 'sds':
        st = _get_data_slink(cl, net, sta, chan_priority_list, t0, ti)
        return st

    elif data_type == 'fdsnws':
        st = _get_data_fdsn(cl, net, sta, chan_priority_list, t0, ti)
        return st

    else:
        # print('Error : unknown <%s> server type' %data_type)
        return Stream()
