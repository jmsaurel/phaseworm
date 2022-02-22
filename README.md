# PhaseWorm

This python script wraps-up [PhaseNet](https://github.com/wayneweiqiang/PhaseNet)
for use as a picker within an [Earthworm](http://www.earthwormcentral.org/)
installation. For manual validation of the results, we recommend to use [SeisComP](http://www.seiscomp.de) or [SeisComP3](http://www.seiscomp.de/seiscomp3) software to build a catalog of the events with magnitudes.

<!-- Saurel, J.-M., Retailleau, L., Zhu, W., Issartel, S., Satriano, C., and Beroza, G. C.: Implementation of a new real time seismicity detector for the Mayotte crisis, EGU General Assembly 2021, online, 19–30 Apr 2021, EGU21-10646, [10.5194/egusphere-egu21-10646](https://doi.org/10.5194/egusphere-egu21-10646), 2021. -->

Retailleau, L., Saurel, J.-M., Zhu, W., Satriano, C., Beroza, G. C, Issartel, S., Boissier, P., OVPF Team and OVSM Team (2022). A wrapper to use a machine-learning-based algorithm for earthquake monitoring, Seismological Research Letter, **XX**, 1-9, [10.1785/0220210279](https://doi.org/10.1785/0220210279).

![flow-chart](/doc/flow-chart.png)
_
PhaseWorm can access data from 4 differents data sources, using [ObsPy](https://www.obspy.org) clients:

* SeedLink
* FDSN webservice
* Earthworm WaveServerV
* SDS disk file archive

Picks can be written as Earthworm **TYPE\_PICK\_SCNL** messages files or simply
written to the standard output.

PhaseWorm can run in an infinite loop in an almost real-time manner
and can also process (replay) old data.

**PhaseNet** identifies P and S arrivals and **PhaseWorm** binds them to,
respectively, vertical and horizontal channels.

---
## Installation and configuration

The _PhaseWorm_ code has been developed with **Python 3.8**,
**ObsPy 1.2.2** and **Earthworm v7.10**.
The _PhaseNet_ included version uses **TensorFlow 2**.

*Note that TensorFlow 2 is currently not compatible with Python 3.9.*


### PhaseWorm

Download PhaseWorm by cloning the repository into your local installation
directory.

	git clone https://github.com/jmsaurel/phaseworm.git


#### Preparing your environment

A python environment with proper libraries and modules is necessary to run
PhaseWorm and the underlying PhaseNet.

##### Using Anaconda (recommended)
```
conda create --name phaseworm python=3.8
conda activate phaseworm
conda install tensorflow=2.3
conda install matplotlib scipy numpy
conda install obspy -c conda-forge
```
##### Using virtualenv
```
pip install virtualenv
virtualenv .phaseworm
source .phaseworm/bin/activate
```

#### Installing PhaseWorm

You can install _PhaseWorm_ using `pip` from the main directory:

	pip install .

Or, in "developer mode":

	pip install -e .



### Earthworm
_PhaseWorm_ is designed to output **TYPE\_PICK\_SCNL** Earthworm messages files
that will be read by the _file2ew_ module and injected into a RingBuffer.

Because _PhaseNet_ is designed to use overlapping time sequences,
it is recommended to use a _pkfilter_ module to remove duplicated picks.

#### file2ew

PhaseWorm pick file should be looked for regularly by the _file2ew_ module to be
injected in the correct RingBuffer.
We recommend a scan every 0.5 second and no logging extensive logging.
Pick files are written by PhaseWorm with the file extension **.pick**.

Because pick files are written, and then a hard symlink made to the _file2ew_
 deposit directory, it's recommended to not activate the _SaveDataFiles_
 option.

The _SuffixType_ option should be configure with the InsitutionID used in the
 Earthworm setup.

```
CheckPeriod     0.5                # sleep this many seconds between looks
OpenTries       2                  # How many times we'll try to open a file
OpenWait        100                # Milliseconds to wait between open tries
SaveDataFiles   0                  # 0 = remove files after processing
LogOutgoingMsg  0
SuffixType  .pick     TYPE_PICK_SCNL       INST_xxx
```

#### pkfilter

PhaseNet picks predictions are equally accurate when working on overlapping
data windows. We recommend a value of **0.05** seconds for _PickTolerance_.

When working with 30s timewindows, a pick could be detected only on the next
overlapping time window. We then allow **60s** _OlderPickLimit_ to be checked.

```
PickTolerance  0.05
OlderPickLimit 60
```

#### binder_ew

_Binder_ew_ module should be setup as usual, according to the local area
settings. However, to take full advantage of the **P** and **S** phase
identifications from _PhaseNet_, two parameters should be activated:
* no_S_on_Z (only _PhaseNet_ **P** readings are sent on vertical channels)
* no_P_on_Horiz (only _PhaseNet_ **S** readings are sent on horizontal channels)

Since **S** phases are sent to horizontal channel, binder_ew shouldn't be
allowed to initiate the stack on horizontal channels.

Currently, PhaseNet doesn't output any amplitude pick measurements. It's
then recommended not to use the **S** to **P** amplitude ratio setting.

```
# stack_horizontals
# s_to_p_amp_ratio 2.0
no_S_on_Z
no_P_on_Horiz
```

#### eqassemble

Because _PhaseNet_ picks **S** readings, it's important to activate them in _eqassemble_ module.

```
ReportS 1
```

---
## Usage
By default, PhaseWorm will use the configuration from the **config.cfg** file.

	phaseworm

Alternative configuration file can be passed on the command line.

	phaseworm --config-file /my/path/to/my_config.cfg

The configuration file is divided into 3 different sections.

### Earthworm section
This section defines variables linked to the Earthworm setup that will be used
to process the pick messages (`module_id`, `inst_id`, `message_id`).
This section also defines the directory in which **TYPE\_PICK\_SCNL** messages
will be written to.

### PhaseNet section
This section defines PhaseNet related variables.
Currently there is only one available variable: the neural network training
file to use.
The recommended default is to use the file shipped with PhaseNet and
included in this bundle.

If you have trained PhaseNet on your own data, you might want to use
your training file.

### General section
The general section contains various variables to set-up _PhaseWorm_:
* data source
* time window lenght to process
* network.stations to look for
* channels priority list to look for each station
* **replay** or **real-time** mode
* whether to activate or not the **TYPE\_PICK\_SCNL** message writing.

---
## Examples
Two configuration examples are shipped: `config_replay.cfg` and `config_rt.cfg`.

### Replay mode
The file `config_replay.cfg` contains a configuration for replay use.

PhaseWorm reads data from FDSN webservice, starting from xxx until xxx.

### Real-time mode
The file `config_rt.cfg` contains a configuration for near real-time use.

PhaseWorm reads data from an Earthworm WaveServerV (recommended) or SeedLink.

PhaseWorm write picks in the **TYPE\_PICK\_SCNL** directory.

---
## Acknowledgements
_PhaseNet_ code was simplified on purpose by Weiqiang Zhu.

Data preprocessing was designed and implemented by Lise Retailleau.

Overall wrapping was done by Jean-Marie Saurel.

Claudio Satriano provided extensive code review.

Testing was performed on Mayotte seismo-volcano crisis for the
Réseau de surveillance volcanologique et sismologique de Mayotte: [REVOSIMA](
http://www.ipgp.fr/revosima).
