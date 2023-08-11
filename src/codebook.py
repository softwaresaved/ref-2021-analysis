""" Codebook for REF 2021 data """

# about the ref process
COL_PANEL_CODE = 'Main panel'
COL_PANEL_NAME = 'Main panel name'
COL_UOA_NUMBER = 'Unit of assessment number'
COL_UOA_NAME = 'Unit of assessment name'
# about the institution etc
COL_INST_CODE = 'Institution UKPRN code'
COL_INST_NAME = 'Institution name'
COL_RG_CODE = 'Research group code'
COL_RG_NAME = 'Research group name'
# about the output
COL_OUTPUT_TYPE_CODE = 'Output type'
COL_OUTPUT_TYPE_NAME = 'Output type name'
COL_OPEN_ACCESS = 'Open access status'

COL_OUTPUT_TITLE = 'Title'

# value to add if no entry in the data
VALUE_ADDED_NOT_SPECIFIED = 'Not specified - PP ADDED'

# source: website
PANEL_NAMES = {
    "A": "Medicine, health and life sciences",
    "B": "Physical sciences, engineering and mathematics",
    "C": "Social sciences",
    "D": "Arts and humanities"
}

# source: https://results2021.ref.ac.uk/filters/unit-of-assessment
UOA_NAMES = {
    1: 'Clinical Medicine',
    2: 'Public Health, Health Services and Primary Care',
    3: 'Allied Health Professions, Dentistry, Nursing and Pharmacy',
    4: 'Psychology, Psychiatry and Neuroscience',
    5: 'Biological Sciences',
    6: 'Agriculture, Food and Veterinary Sciences',
    7: 'Earth Systems and Environmental Sciences',
    8: 'Chemistry',
    9: 'Physics',
    10: 'Mathematical Sciences',
    11: 'Computer Science and Informatics',
    12: 'Engineering',
    13: 'Architecture, Built Environment and Planning',
    14: 'Geography and Environmental Studies',
    15: 'Archaeology',
    16: 'Economics and Econometrics',
    17: 'Business and Management Studies',
    18: 'Law',
    19: 'Politics and International Studies',
    20: 'Social Work and Social Policy',
    21: 'Sociology',
    22: 'Anthropology and Development Studies',
    23: 'Education',
    24: 'Sport and Exercise Sciences, Leisure and Tourism',
    25: 'Area Studies',
    26: 'Modern Languages and Linguistics',
    27: 'English Language and Literature',
    28: 'History',
    29: 'Classics',
    30: 'Philosophy',
    31: 'Theology and Religious Studies',
    32: 'Art and Design: History, Practice and Theory',
    33: 'Music, Drama, Dance, Performing Arts, Film and Screen Studies',
    34: 'Communication, Cultural and Media Studies, Library and Information Management'
}

# source: https://results2021.ref.ac.uk/outputs
OUTPUT_TYPE_NAMES = {
    'A': 'Authored book',
    'B': 'Edited book',
    'C': 'Chapter in book',
    'D': 'Journal article',
    'E': 'Conference contribution',
    'F': 'Patent/ published patent application',
    'G': 'Software',
    'H': 'Website content',
    'I': 'Performance',
    'J': 'Composition',
    'K': 'Design',
    'L': 'Artefact',
    'M': 'Exhibition',
    'N': 'Research report for external body',
    'P': 'Devices and products',
    'Q': 'Digital or visual media',
    'R': 'Scholarly edition',
    'S': 'Research data sets and databases',
    'T': 'Other',
    'U': 'Working paper',
    'V': 'Translation'
}
