# xxxx - PhaseNet picker prediction to EarthWorm
# Copyright (C) 2020-
# Lise Retailleau (retailleau@ipgp.fr)
# Jean-Marie Saurel (saurel@ipgp.fr)
# Licensed under GNU GPLv3 (see LICENSE.txt)

"""Configuration reading."""

import configparser
import read_config as rc
import os


class earthworm(object):
    """Private class to store EarthWorm configuration."""

    def __init__(self, config):
        """
        Initialize the EarthWorm configuration values.

        # Directory where to find EarthWorm .d configuration files
        #   default to /opt/earthworm/run_prod/params
        params_dir = /opt/earthworm/run_prod/params

        # EarthWorm Institution ID (must be defined in earthworm_global.d)
        #   default to INST_UNKNOWN
        MyInstitutionID = INST_REVOSIMA

        # EarthWorm Module ID assigned to this app
        # (must be defined in earthworm.d)
        #   default to MOD_WILDCARD
        MyModuleID = MOD_PHASENET

        # EarthWorm ring to write messages (must be defined in earthworm.d)
        #   default to PICK_RING
        OutRing = PICK_RING

        # File to keep track of the pick number
        # (must be unique to each PhaseNet instance)
        #   default to /tmp/PhaseNet_next_pick_number
        nb_pick_keeper = /tmp/next_pick_number
        """
        section = 'EarthWorm'

        opt = 'params'
        path = config.get(section, opt) if config.has_option(
            section, opt) else '/opt/earthworm/run_prod/params'
        self.params = os.path.normpath(path)

        opt = 'MyInstitutionID'
        self.MyInstitutionID = config.get(section, opt) if config.has_option(
            section, opt) else 'INST_UNKNOWN'

        opt = 'MyModuleID'
        self.MyModuleID = config.get(section, opt) if config.has_option(
            section, opt) else '/opt/earthworm/run_prod/params'

        opt = 'OutRing'
        self.OutRing = config.get(section, opt) if config.has_option(
            section, opt) else 'PICK_RING'

        opt = 'nb_pick_keeper'
        path = config.get(section, opt) if config.has_option(
            section, opt) else '/tmp/PhaseNet_next_pick_number'
        self.nb_pick_keeper = os.path.normpath(path)

        opt = 'pick_dir'
        path = config.get(section, opt) if config.has_option(
            section, opt) else '/opt/earthworm/run_prod/PICK_SCNL'
        self.pick_dir = os.path.normpath(path)


class phasenet(object):
    """Private class to store PhaseNet configuration."""

    def __init__(self, config):
        """
        Initialize the PhaseNet configuration values.

        # PhaseNet neural network directory
        # Absolute path or path relative to phaseworm root directory
        #   default to phasenet/model/190703-214543
        checkpoint = phasenet/model/190703-214543
        """
        section = 'PhaseNet'

        opt = 'checkpoint'
        path = config.get(section, opt) if config.has_option(
            section, opt) else 'phasenet/model/190703-214543'
        self.checkpoint = os.path.normpath(path)


class general(object):
    """Private class to store all general configuration variables."""

    def __init__(self, config):
        """
        Initialize the general configuration values.

        # Configuration of the data source to use
        # Can be an FDSN dataselect webservice,
        # a SeedLink server
        # or an EarthWorm WaveServerV
        #   default to IRIS
        # FDSN : can be one ObsPy server (see obspy.clients.fdsn for full list)
        #   e.g., datasource = IRIS
        #   or specify a server, datasource = fdsnws://server:port
        #   e.g., datasource = fdsnws://http://service.iris.edu
        # SeedLink server : 18000 default port if not provided
        #   datasource = seedlink://server:port
        #   e.g., datasource = seedlink://rtserve.iris.washington.edu:18000
        # EarthWorm WaveServerV :  16017 default port if not provided
        #   datasource = waveserver://server:port
        #   e.g., datasource = waveserver://mazama.ess.washington.edu:16024
        datasource = IRIS
        #fdsn = 'fdsnws://http://195.83.188.34:8080'
        #seedlink = 'slink://195.83.188.34:18000'
        #waveserver = 'waveserver://127.0.0.1:16000'

        # Comma separated channel list to use by descending priority
        #   third orientation character should be wildcard '?'
        #   default to HH?,BH?,HN?
        chan_list = HH?,EH?,SH?,HN?,BH?

        # Comma separated Network.Station list to use
        station_list = 1T.MTSB,QM.KNKL,1T.PMZI,AM.R1EE2,AM.R0CC5,ED.MCHI

        # All data are interpolated to sps samples per seconds for PhaseNet
        #   default to 100
        sps = 100

        # Log : INFO, DEBUG
        #   default to INFO
        log = INFO

        # Running mode :
        #   NORMAL : predict and send picks to EarthWorm in almost real-time
        #   REPLAY : predict on an old time span and prints out picks
        #            (no output written)
        #   default to NORMAL
        mode = NORMAL

        # NORMAL and DUMMY mode, wait latency seconds after real-time
        # before requesting data
        #   default to 10s
        latency = 10

        # REPLAY mode, parameter is only used in replay mode
        #   data start time to analyze
        #   start time in ISO format YYYY-mm-ddTHH:MM:SS
        starttime =

        # NORMAL and REPLAY mode, time window length in seconds
        # to process at a time
        #   default to 30
        tw = 30

        # Write EW picks : set to True to write TYPE_PICK_SCNL messages
        #   default to True
        write_picks = True

        # PhaseNet probability to weight conversion law
        #   a           : linear between 0.3 and 1 mapped wt between 3 and 0
        #   b           :
        #   linear      : linear between 0 and 1 mapped wt between 3 and 0
        #   taped_linear: linear between 0 and 1 mapped wt between 3 and 0
        #                 probablility below 0.3, weight of 3
        #   default to a
        prob_to_wt_law = a

        """
        section = 'General'

        opt = 'datasource'
        self.datasource = config.get(section, opt) if config.has_option(
            section, opt) else 'IRIS'

        opt = 'chan_list'
        self.chan_list = config.get(section, opt) if config.has_option(
            section, opt) else 'HH?,BH?,HN?'

        opt = 'station_list'
        self.station_list = config.get(section, opt) if config.has_option(
            section, opt) else ''

        opt = 'sps'
        self.sps = config.getint(section, opt) if config.has_option(
            section, opt) else 100

        opt = 'log'
        self.log = config.get(section, opt).upper() if config.has_option(
            section, opt) else 'INFO'

        opt = 'mode'
        self.mode = config.get(section, opt) if config.has_option(
            section, opt) else 'NORMAL'

        opt = 'latency'
        self.latency = config.getfloat(section, opt) if config.has_option(
            section, opt) else 30.0

        opt = 'tw'
        self.tw = config.getfloat(section, opt) if config.has_option(
            section, opt) else 30.0

        opt = 'starttime'
        self.starttime = config.get(section, opt) if config.has_option(
            section, opt) else ''

        opt = 'write_picks'
        self.write_picks = config.getboolean(
            section, opt) if config.has_option(section, opt) else True

        opt = 'prob_to_wt_law'
        self.prob_to_wt_law = config.get(section, opt) if config.has_option(
            section, opt) else 'a'


class Config(object):
    """Private class to store all the configuration."""

    def __init__(self, configfile='config.cfg'):
        """
        Initialize the configurations values read from the configuration file.

        The file is divided in 3 main sections, each one prefixed
        with a [] header :
            * EarthWorm for output related configuration
            * PhaseNet for the prediction related configuration
            * Setting for general configuration of the picker

        Each section is parsed and read by its class (see above)
        """
        self.configfile = configfile

        # Load parameters from config file
        config = configparser.ConfigParser()
        config.read(self.configfile)

        # Read EarthWorm section parameters
        self.earthworm = rc.earthworm(config)

        # Read PhaseNet section parameters
        self.phasenet = rc.phasenet(config)

        # Read Setting section parameters
        self.general = rc.general(config)
