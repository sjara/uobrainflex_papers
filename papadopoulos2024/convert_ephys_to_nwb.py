"""
This script converts ephys data from Papadopoulos et al (2024) to NWB format.

Usage:
python convert_ephys_to_nwb.py ./nwb_metadata.py /tmp/  # Convert all sessions
python convert_ephys_to_nwb.py ./nwb_metadata.py /tmp/ LA3_session3  # Convert single session

where ./nwb_metadata.py is a file that defines the metadata for all recorded sessions,
/tmp/ is the path to the directory where the NWB files will be saved,
and LA3_session3 is the name of a single session to convert (optional).
"""

import os
import sys
import pynwb
from datetime import datetime
import pytz
import numpy as np
import h5py
import importlib

# -- Select what to process (useful for debugging) --
ADD_TRIAL_INFO = 1  # Add trial information to NWB file
ADD_SPIKES = 1      # Add spike times to NWB file
ADD_BEHAVIOR = 1    # Add pupil, running, and whisking data to NWB file
SAVE_NWB = 1        # Save NWB file

# -- Parse command line arguments --
if len(sys.argv) > 3:
    sessions = [sys.argv[3]]
else:
    sessions = None    
if len(sys.argv) > 2:
    metadata_filename = sys.argv[1]
    output_path = sys.argv[2]
else:
    raise ValueError('Please provide a metadata file.')

# -- Read metadata file --
def read_metadata(metadata_filename):
    spec = importlib.util.spec_from_file_location('metadata_module', metadata_filename)
    metamodule = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(metamodule)
    return metamodule

metamodule = read_metadata(metadata_filename)
metadata = metamodule.metadata
if sessions is None:
    sessions = metadata.keys()

# -- Currently hardcoded in the metadata file. Better if read from the HDF5 data files. --
STIM_DURATION = metamodule.stim_duration

# -- For each session, read data from HDF5 file and create an NWB file --
for session in sessions:
    print(f'Converting session {session}')

    h5file_fullpath = os.path.join(metadata[session]['path_to_data'],
                                   metadata[session]['filename'])
    
    # -- Add sesion information --
    start_time = datetime.fromisoformat(metadata[session]['session_start_time'])
    nwbfile = pynwb.NWBFile(
        experiment_description = metadata[session]['experiment_description'],
        keywords = metadata[session]['keywords'],
        session_description = metadata[session]['session_description'],
        identifier = metadata[session]['identifier'],
        session_start_time = start_time,
        experimenter = metadata[session]['experimenter'],
        lab = metadata[session]['lab'],
        institution = metadata[session]['institution'],
        session_id = metadata[session]['session_id'],
        related_publications = metadata[session]['related_publications']
    )

    # -- Add subject information --
    nwbfile.subject = pynwb.file.Subject(
        subject_id = metadata[session]['subject_id'],
        age = metadata[session]['subject_age'],
        description = metadata[session]['subject_description'],
        species = metadata[session]['subject_species'],
        sex = metadata[session]['subject_sex']
    )

    # -- Add trial information --
    if ADD_TRIAL_INFO:
        with h5py.File(h5file_fullpath, 'r') as datafile:
            print('Storing trial information...')
            trial_start_time = datafile['stim_data']['stim_on_time'][()]
            stim_frequency = datafile['stim_data']['stim_Hz'][()]

            nwbfile.add_trial_column(name='stim_frequency',
                                     description='Stimulus frequency (Hz)')
            # NOTE: Looping through >5000 trials takes a long time,
            #       but pynwb doesn't seem to have a faster way.
            for indt, start_time in enumerate(trial_start_time):
                nwbfile.add_trial(start_time = start_time,
                                  stop_time = start_time+STIM_DURATION,
                                  stim_frequency = stim_frequency[indt])

    # -- Add spike-times information --
    if ADD_SPIKES:
        with h5py.File(h5file_fullpath, 'r') as datafile:
            print('Storing spike times information...')
            spike_times_all = datafile['cell_spikeTimes'][()]
            for indu, spike_times in enumerate(spike_times_all):
                nwbfile.add_unit(spike_times=spike_times)


    # -- Add pupil, running, and whisking data --
    if ADD_BEHAVIOR:
        print('Storing behavior (pupil/running/whisking) information...')
        behavior_module = nwbfile.create_processing_module(
            name = 'behavior', 
            description = 'Processed behavioral data'
        )

        with h5py.File(h5file_fullpath, 'r') as datafile:
            timestamps = datafile['behavioral_data']['time'][()]
            pupil = datafile['behavioral_data']['pupil_trace'][()]
            running = datafile['behavioral_data']['run_trace'][()]
            whisking = datafile['behavioral_data']['whisk_trace'][()]
            
        pupil_diameter = pynwb.base.TimeSeries(
            name = 'pupil_diameter',
            description = metamodule.pupil_description,
            timestamps = timestamps,
            data = pupil,
            unit = metamodule.pupil_units
        )
        pupil_tracking = pynwb.behavior.PupilTracking()
        pupil_tracking.add_timeseries(pupil_diameter)
        behavior_module.add(pupil_tracking)
        
        running_speed = pynwb.base.TimeSeries(
            name = 'running_speed',
            description = metamodule.running_description,
            timestamps = timestamps,
            data = running,
            unit = metamodule.running_units
        )
        behavior_module.add(running_speed)
        
        whisking_trace = pynwb.base.TimeSeries(
            name='whisking_trace',
            description=metamodule.whisking_description,
            timestamps = timestamps,
            data = whisking,
            unit = metamodule.whisking_units
        )
        behavior_module.add(whisking_trace)
    
    # -- Save NWB file --
    if SAVE_NWB:
        nwb_filename = metadata[session]['filename'].replace('.h5', '.nwb')
        output_fullpath = os.path.join(output_path, nwb_filename)                           
        print(f'Saving {output_fullpath}')
        with pynwb.NWBHDF5IO(output_fullpath, 'w') as io:
            io.write(nwbfile)
            print(f'Done.\n')

'''
# -- Check the contents of the NWB object --
nwbfile.trials.to_dataframe()
nwbfile.units.to_dataframe()
nwbfile.processing['behavior']['PupilTracking']['pupil_diameter']
nwbfile.processing['behavior']['running_speed']
'''

# -- Useful for debugging --            
# with pynwb.NWBHDF5IO('/tmp/test.nwb', 'w') as io: io.write(nwbfile)

