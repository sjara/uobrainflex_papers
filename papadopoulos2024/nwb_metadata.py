"""
Metadata for each ephys session used in Papadopoulos et al (2024).
"""

path_to_data = '/mnt/ion-nas2/Brain_Initiative/Neuropixels/Su_NP/processed_data_LP/'

# Common values across sessions
experimenter = 'Jo, Suhyun'
lab = 'McCormick'
institution = 'University of Oregon'
session_description = 'Recordings from mouse auditory cortex during passive exposure to sounds'
experiment_description = session_description
subject_species = 'Mus musculus'
related_publications = 'doi:10.1101/2024.04.04.588209'
keywords = ['auditory cortex', 'arousal', 'pupil', 'neuropixels', 'pure tones']

pupil_description = 'Pupil diameter extracted from the video'
running_description = 'Running speed measured by a rotary encoder on the wheel'
whisking_description = '???'

# NOTES about formatting subjects' sex and age
# subject_sex: M, F or U (for unknown)
# subject_age: P90D (for 90 days old in ISO 8601 Duration format)

# Dictionary for metadata
metadata = {}

# LA3_SESSION3
metadata['LA3_session3'] = {}
metadata['LA3_session3']['identifier'] = 'LA3_session3'
metadata['LA3_session3']['session_id'] = 'LA3_session3'
metadata['LA3_session3']['filename'] = 'LA3_session3_processed_data.h5'
metadata['LA3_session3']['path_to_data'] = path_to_data
metadata['LA3_session3']['session_description'] = session_description
metadata['LA3_session3']['session_start_time'] = '2020-01-28T02:30:03-08:00' # Include time-zone
metadata['LA3_session3']['subject_id'] = 'LA3'
metadata['LA3_session3']['subject_age'] = 'P21D'
metadata['LA3_session3']['subject_description'] = 'mouse 1'
metadata['LA3_session3']['subject_species'] = subject_species
metadata['LA3_session3']['subject_sex'] = 'U'
metadata['LA3_session3']['experiment_description'] = experiment_description
metadata['LA3_session3']['keywords'] = keywords
metadata['LA3_session3']['experimenter'] = experimenter
metadata['LA3_session3']['lab'] = lab
metadata['LA3_session3']['institution'] = institution              
metadata['LA3_session3']['related_publications'] = related_publications



# LA8_SESSION1
metadata['LA8_session1'] = {}



# LA8_SESSION2
metadata['LA8_session2'] = {}



# LA9_SESSION1
metadata['LA9_session1'] = {}



# LA9_SESSION3
metadata['LA9_session3'] = {}




# LA9_SESSION4
metadata['LA9_session4'] = {}




# LA9_SESSION5
metadata['LA9_session5'] = {}



# LA11_SESSION1
metadata['LA11_session1'] = {}



# LA11_SESSION2
metadata['LA11_session2'] = {}




# LA11_SESSION3
metadata['LA11_session3'] = {}




# LA11_SESSION4
metadata['LA11_session4'] = {}



# LA12_SESSION1
metadata['LA12_session1'] = {}



# LA12_SESSION2
metadata['LA12_session2'] = {}




# LA132SESSION3
metadata['LA12_session3'] = {}




# LA12_SESSION4
metadata['LA12_session4'] = {}
