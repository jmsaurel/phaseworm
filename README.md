# pick_PhNet

This python script wraps-up PhaseNet (ref) for use as a picker within an EarthWorm installation

## Installation
Create conda environment
git clone

## Configuration
Two configuration examples are shipped : config_replay.cfg and config_rt.cfg.
PhaseWorm can be used in two different modes : replay or real-time.

### Replay mode
The file config_replay.cfg contains a configuration for replay use.

pick_PhNet reads data from FDSN webservice, starting from xxx until xxx.

### Real-time mode
The file config_rt.cfg contains a configuration for near real-time use.

pickPhNet reads data from an EarthWorm WaveServerV (recommended) or SeedLink.

pickPhNet write picks in the PICK_SCNL directory

