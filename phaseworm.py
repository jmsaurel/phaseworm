"""
PhaseNet wrapper to EarthWorm.

usage: phaseworm [-h] [-c CONFIG_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --configfile CONFIG_FILE
                        use configuration file named CONFIG_FILE instead of
                        default config.cfg
"""

import sys
import os
import time
import argparse
import logging
from obspy.core import UTCDateTime
from obspy.clients import seedlink
from obspy.clients import earthworm
from obspy.clients import fdsn
from obspy.clients.filesystem import sds
import numpy as np
from get_data import get_data_from_client
import read_config
from phasenet import app
from phasenet.app import get_prediction, init_pred


# ___ DATA TYPES ______________________________________________________________
class Pick():
    """A class to store a PhaseNet pick."""

    def __init__(self, time, phase, proba, scnl, amp, ew):
        """Initialization."""
        self.time = time
        self.phase = phase
        self.probability = proba
        self.scnl = scnl
        self.amplitude = amp
        self.fm = '?'
        self.pickid = 0
        self.msgtype = ew.msgtype
        self.instid = ew.instid
        self.modid = ew.modid

    def set_h71_weight(self, law):
        """Convert pick probability into Hypo71 weight."""
        # Linear between and
        if law == 'a':
            wt = -4.29 * self.probability + 4.29
            if self.probability < 0.3:
                wt = 3
        # Linear between and
        elif law == 'b':
            wt = -2.857 * self.probability + 2.857
            if self.probability < 0.3:
                wt = 3
        # Linear between 0 and 1 mapped between 0 and 3
        elif law == 'linear':
            wt = 3 * (1 - self.probability)
        # Linear between 0.3 and 1 mapped between 0 and 3
        elif law == 'taped_linear':
            if self.probability < 0.3:
                wt = 3
            else:
                wt = 3 * (1 - self.probability)
        # Set weight
        self.weight = wt
        logging.debug("Proba = %.1f -> weight = %d"
                      % (self.probability, self.weight))

    def print(self):
        """Print the pick to standard output."""
        [s, c, n, l] = self.scnl.split('.')
        msg = str("%s %c %.1f %s.%s.%s.%s\n"
                  % (self.time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                     self.phase, self.probability, n, s, l, c))
        logging.info(msg)

    def TYPE_PICK_SCNL(self):
        """Write TYPE_PICK_SCNL message."""
        [s, c, n, l] = self.scnl.split('.')
        msg = str("%d %d %d %d %s.%s.%s.%s %c%1d %18s %d %d %d\n"
                  % (self.msgtype, self.modid, self.instid,
                     self.pickid, s, c, n, l, self.fm, self.weight,
                     self.time.strftime("%Y%m%d%H%M%S.%f")[:-3],
                     self.amplitude, self.amplitude, self.amplitude))
        return msg


class EarthWorm():
    """A class to store EarthWorm informations."""

    def __init__(self):
        """Initialization."""
        self.instid = 255
        self.modid = 0
        self.msgtype = 8
        self.outring = 1000

    def read_conf(self, opts):
        """Read EarthWorm configuration files."""
        # Search InstitutionID and MessageType in earthworm_global.d file
        file = os.path.join(opts.params, 'earthworm_global.d')
        try:
            f = open(file, 'r', encoding='latin-1')
            for line in f:
                if opts.MyInstitutionID in line:
                    self.instid = int(line.split()[2])
                elif 'TYPE_PICK_SCNL' in line:
                    self.msgtype = int(line.split()[2])
            f.close()
            logging.debug("Found %s = %d"
                          % (opts.MyInstitutionID, self.instid))
            logging.debug("Found TYPE_PICK_SCNL = %d" % self.msgtype)
        except OSError:
            logging.error('Unable to open file %s' % file)
        # Search ModuleID, OutRing in earthworm.d file
        file = os.path.join(opts.params, 'earthworm.d')
        try:
            f = open(file, 'r', encoding='latin-1')
            for line in f:
                if opts.MyModuleID in line:
                    self.modid = int(line.split()[2])
                elif opts.OutRing in line:
                    self.outring = int(line.split()[2])
            f.close()
            logging.debug("Found %s = %d"
                          % (opts.MyModuleID, self.modid))
            logging.debug("Found %s = %d"
                          % (opts.OutRing, self.outring))
        except OSError:
            logging.error('Unable to open file %s' % file)
# ___ END : DATA TYPES ________________________________________________________


# ___ INIT FUNCTIONS __________________________________________________________
def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run PhaseNet picker")

    parser.add_argument("-c", "--configfile",
                        help="use configuration file named CONFIG_FILE")
    args = parser.parse_args()

    return args


def get_client(data_source):
    """Initialize data client from data_source string."""
    data_type = data_source.split('://', 1)[0]
    data_server = data_source.split('://', 1)[1]

    if data_type == 'waveserver':
        # ew_ws = '127.0.0.1:16000'
        ew_ws = data_server.split(':')
        if len(ew_ws) == 1:
            port = 16017
        else:
            port = int(ew_ws[1])
        client = earthworm.Client(ew_ws[0], port=port, timeout=2.0)
        logging.debug('Successfully initialized WaveServerV client %s'
                      % data_server)
        return client

    elif data_type == 'slink':
        # slink = '195.83.188.34:18000'
        slink = data_server.split(':')
        if len(slink) == 1:
            port = 18000
        else:
            port = int(slink[1])
        client = seedlink.Client(slink[0], port=port, timeout=2.0)
        logging.debug('Successfully initialized SeedLink client %s'
                      % data_server)
        return client

    elif data_type == 'sds':
        # SDS = '/data/SDS'
        SDS = data_server
        return client

    elif data_type == 'fdsnws':
        # fdsn_ws = 'http://195.83.188.34:8080'
        try:
            client = fdsn.Client(data_server)
        except Exception:
            logging.error('Error : failed to connect to %s FDSN webservice'
                          % data_server)
        else:
            logging.debug('Successfully initialized FDSNWS client %s'
                          % data_server)
            return client

    else:
        print('Error : unknown <%s> server type' % data_type)
# ___ END : INIT FUNCTIONS ____________________________________________________


# ___ PICK PREDICTION AND PROCESSING __________________________________________
def run_phasenet(ti, sess, model, client, conf, ew):
    """Send data snippet to PhaseNet for prediction."""
    npicks = 0

    client_type = conf.general.datasource.split('://', 1)[0]

    tw = conf.general.tw
    sps = conf.general.sps

    NetSta_list = list(conf.general.station_list.split(','))
    Net = [netsta.split('.')[0] for netsta in NetSta_list]
    Sta = [netsta.split('.')[1] for netsta in NetSta_list]

    chan_list = list(conf.general.chan_list.split(','))
    logging.debug('Using channel priority list %s' % chan_list)

    t0 = ti-tw

    for ista in range(len(Sta)):
        logging.info(Sta[ista])
        st = get_data_from_client(Net[ista], Sta[ista], t0, ti,
                                  chan_list, client, client_type)
        logging.debug(st)
        if len(st) == 0:
            logging.info('No data')
            continue
        st.merge(method=1, fill_value='interpolate')
        st.detrend(type='demean')
        # st.taper(0.005,type='hamming')
        try:
            st.interpolate(sampling_rate=sps)
        except Exception:
            logging.warning('Failed to interpolate data')
            continue
        st = st.slice(starttime=t0, endtime=ti)
        st = st.sort()
        data = []
        tr_statistics = []
        if len(st) == 3:
            for ch in ['E', 'N', 'Z']:
                tr = st.select(channel='*'+ch)[0]
                if tr.stats.sampling_rate*tw+1 != tr.stats.npts:
                    logging.error('Trace inconsistency : %d != %d'
                                  % (tr.stats.sampling_rate*tw+1, tr.stats.npts))
                    continue
                data.append(tr.data[:-1])
                tr_statistics.append(tr.stats)
            if len(data) != 3:
                logging.error('Found %d channels, not 3' % len(data))
                continue
        else:
            continue
            data.append(np.zeros(np.int(sps*tw)))
            data.append(np.zeros(np.int(sps*tw)))
            tr = st.select(channel='*'+'Z')[0]
            if tr.stats.sampling_rate*tw+1 != tr.stats.npts:
                logging.error('Trace inconsistency : %d != %d'
                              % (tr.stats.sampling_rate*tw+1, tr.stats.npts))
                continue
            data.append(tr.data[:-1])
            tr_statistics.append(tr.stats)
            tr_statistics.append(tr.stats)
            tr_statistics.append(tr.stats)
        data = np.array(data).T

        logging.info('Sending data to PhaseNet prediction')
        picks = get_prediction(data, sess, model)
        if picks:
            npicks += process_picks(picks, tr_statistics, ew, conf)

    return npicks


def process_picks(picks, traces_stats, ew, conf):
    """Process PhaseNet predictions."""
    npicks = 0
    logging.info("Processing <%s> picks" % (traces_stats[0].station))
    for pks in picks:
        # P picks are on colunms 0 and 1 (k=0)
        # S picks are on columns 2 and 3 (k=2)
        for k in 0, 2:
            # Iterate over picks
            for i, idx in enumerate(pks[k]):
                # Get pick probability
                proba = pks[k+1][i]
                # Iterate over traces statistics to find vertical channel
                if k == 0:
                    for stats in traces_stats:
                        if (stats.channel.find('Z') > 0
                                or stats.channel.find('3') > 0):
                            tr_stats = stats
                            break
                    scnl = tr_stats.station + '.' +\
                        tr_stats.channel + '.' +\
                        tr_stats.network + '.' +\
                        tr_stats.location
                    # Calculate pick time from trace starttime, sps and index
                    time = tr_stats.starttime + tr_stats.delta * idx
                    # Create P-pick with 100 amplitude
                    pick = Pick(time, 'P', proba, scnl, 100, ew)
                    logging.debug('P pick : %s' % pick.print())
                elif k == 2:
                    for stats in traces_stats:
                        if (stats.channel.find('N') > 0
                                or stats.channel.find('2') > 0
                                or stats.channel.find('E') > 0
                                or stats.channel.find('1') > 0):
                            tr_stats = stats
                            break
                    scnl = tr_stats.station + '.' +\
                        tr_stats.channel + '.' +\
                        tr_stats.network + '.' +\
                        tr_stats.location
                    # Calculate pick time from trace starttime, sps and index
                    time = tr_stats.starttime + tr_stats.delta * idx
                    # Create S-pick with 400 amplitude
                    pick = Pick(time, 'S', proba, scnl, 400, ew)
                    logging.debug('S pick : %s' % pick.print())
                # Read pick number from keeper file
                if os.path.exists(conf.earthworm.nb_pick_keeper):
                    with open(conf.earthworm.nb_pick_keeper, 'r') as f:
                        ew.pickid = int(f.readline())
                        f.close()
                else:
                    with open(conf.earthworm.nb_pick_keeper, 'w') as f:
                        ew.pickid = 0
                        f.write(str(ew.pickid))
                        f.close()
                # Set pick ID
                pick.pickid = ew.pickid
                # Convert PhaseNet probability to Hypo weight
                pick.set_h71_weight(conf.general.prob_to_wt_law)
                # Write TYPE_PICK_SCNL message
                if conf.general.write_picks:
                    logging.info('Writing pick to file')
                    write_pick(pick.TYPE_PICK_SCNL(), conf, pick.pickid)
                # Update pickid
                if ew.pickid == 999999:
                    ew.pickid = 0
                else:
                    ew.pickid += 1
                # Update pick number in keeper file
                with open(conf.earthworm.nb_pick_keeper, 'w') as f:
                    f.write('%06d' % ew.pickid)
                    f.close()
                npicks += 1
    logging.info('Successfully processed %d picks' % npicks)
    return npicks


def write_pick(msg, conf, pkid):
    """Write pick message."""
    dest = conf.earthworm.pick_dir
    tmpfile = os.path.join(dest, 'tmp', str('%06d.pick' % pkid))
    with open(tmpfile, 'w') as f:
        f.write(msg)
        f.close()
    pick_msg = os.path.join(dest, str('%06d.pick' % pkid))
    os.link(tmpfile, pick_msg)

# ___ END : PICK PREDICTION AND PROCESSING ____________________________________


# ___ MAIN LOOP _______________________________________________________________
def run_loop():
    """Parse arguments, read config and loop infinitely."""
    args = parse_args()

    # Read configuration file
    if args.configfile:
        conf = read_config.Config(args.configfile)
    else:
        conf = read_config.Config()
    log_level = getattr(logging, conf.general.log, None)
    logging.basicConfig(level=log_level)
    logging.debug("Configuration file <%s> read" % args.configfile)
    if not os.path.isabs(conf.phasenet.checkpoint):
        appdir = os.path.dirname(os.path.abspath(__file__))
        conf.phasenet.checkpoint = os.path.join(appdir,
                                                conf.phasenet.checkpoint)
    # Neural network model configuration
    phasenet_config = app.Config()
    phasenet_config.sampling_rate = conf.general.sps
    phasenet_config.dt = 1.0 / conf.general.sps
    n = int(conf.general.sps * conf.general.tw)
    phasenet_config.X_shape = (n, 1, phasenet_config.n_channel)
    phasenet_config.Y_shape = (n, 1, phasenet_config.n_class)
    phasenet_config.min_event_gap = 3 * conf.general.sps
    # Init neural network model
    sess, model = init_pred(phasenet_config, conf.phasenet)
    logging.debug("Tensor flow model <%s> initialized"
                  % conf.phasenet.checkpoint)
    # Init data client
    cl = get_client(conf.general.datasource)
    if not cl:
        logging.critical("No client returned, abort")
        exit()
    # Init EarthWorm values
    ew = EarthWorm()
    ew.read_conf(conf.earthworm)
    logging.debug("EarthWorm configuration initialized")
    # Run infinite loop from RealTime
    if conf.general.mode == 'NORMAL':
        while 1:
            logging.debug('Processing %s ' % UTCDateTime.now())
            t0 = time.time()
            ti = UTCDateTime.now() - conf.general.latency
            n = run_phasenet(ti, sess, model, cl, conf, ew)
            t1 = time.time() - t0
            logging.debug('Processing time %.1fs' % t1)
            logging.debug('%d picks processed' % n)
            if t1 > conf.general.tw/2.0:
                logging.warning('Process time %.1fs longer than tw %.1fs'
                                % t1, conf.general.tw)
            else:
                time.sleep(conf.general.tw/2.0 - t1)
    # Run loop starting from old starttime
    elif conf.general.mode == 'REPLAY':
        ti = UTCDateTime(conf.general.starttime)
        while 1:
            t0 = time.time()
            n = run_phasenet(ti, sess, model, cl, conf, ew)
            t1 = time.time() - t0
            ti += conf.general.tw/2.0
            logging.debug(ti)
            if ti > UTCDateTime.now():
                logging.info('Reached real-time, stop replay')
                break
    # Exit program
    exit()


def main():
    """Run the main loop and handle ctrl-C events."""
    try:
        run_loop()
    except KeyboardInterrupt:
        sys.stderr.write('\nAborting.\n')
        sys.exit()
# ___ END : MAIN LOOP _________________________________________________________


if __name__ == "__main__":
    main()
