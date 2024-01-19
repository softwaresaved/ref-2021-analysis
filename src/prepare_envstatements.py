""" Prepares the extracted environment statements. """
import argparse
from io import StringIO
import sys
import os
import pandas as pd

import read_write as rw
import codebook as cb
import logs as lg

# include all that was noticed in the actual statements
TO_DELETE_HEADERS = [item.replace(" ", "").lower()
                     for item in [
                                "Institutional level environment template (REF5a)",
                                "Institutional level environment template (REF5b)",
                                "Unit-level environment template (REF5a)",
                                "Unit-level environment template (REF5b)",
                                "REF5a - Institution Environment Statement",
                                'Institutional-Level Environment Statement (REF5a)',]]

CHARS_TO_DELETE_FROM_HEADER = [" ", "\t", ".", ",", ":", ";", "-", "and", "&"]

TO_DELETE_PAGES = [f"Page{i}".lower() for i in range(1, 100)]

SECTIONS_INSTITUTION = {
    'Context and mission': [
        '1. Institutional context and mission',
        '1. Context and mission',
        'a) Context and mission',
        'Context and mission',
        'Section 1: Context and mission',
        '1. Context and Vision',
        '1. Institutional overview',
        '1, 2. Context and mission; Strategy',
        '1B 1. Context and mission'],
    'Strategy': [
        '2. Strategy',
        'b) Strategy',
        '2. Research and Impact Strategy',
        '2. Research strategy',
        '2B 2. Strategy',
        'Section 2: Strategy',
        'Strategy',
        '2. Strategy and Achievements',
        '2. Institutional Research and Impact Strategy',
        '2. Research and Knowledge Exchange Strategy',
        'Research at Cambridge'  # Cambridge merges the first two sections into one section
        ],
    'People': [
        '3. People',
        'c) People',
        '3B 3. People',
        'Section 3: People',
        'People',
        '3. Staffing'],
    'Income, infrastructure and facilities': [
        '4. Income, infrastructure and facilities',
        'd) Income, infrastructure and facilities',
        '4B 4. Income, infrastructure and facilities',
        'Section 4: Income, infrastructure and facilities',
        'Income, infrastructure and facilities',
        '4.1 Income'
        ]
}

SECTIONS_UNIT = {
    'Unit context and structure, research and impact strategy': [
        '1. Unit context and structure, research and impact strategy',
        '1. Unit Context and Structure, Research and Impact Strategies',
        '1. Context and structure, research and impact strategy',
        '1. Unit Context, Research and Impact Strategy',
        '1. Unit Context & Structure, Research and impact',
        '1. Unit overview',
        '1. Unit context',
        '1. Overview and mission',
        '1. Context, Structure, and Strategy',
        '1. Unit Context and structure:',
        '1. Context, Strategy, and Structure: Overview',
        '1.0 Unit Context and structure',
        '1.0 Unit context and structure, research and impact strategy:',
        '1.1. Context and structure',
        '1.1 Unit context and structure, research and impact strategy',
        '1.1: Institutional Context and Structure',  # The Glasgow School of Art
        '1. Unit Context and Structure; Research and Impact strategy',
        '1 Unit context and structure, research and impact',
        '1B 1. Unit context and structure, research and impact strategy',
        '2B 1. Unit context and structure, research and impact strategy',
        'Section 1.',
        'Section 1. Unit context and structure, research and impact strategy',
        'Section 1. Unit structure, research and impact strategy',
        'Section 1: Unit Context, Research and Impact Strategy',
        'Section 1: Unit Context',
        'Section 1: Context and Structure',
        'Section 1: Unit Context and Structure',
        'Section 1 (S1). Unit context and structure, research and impact strategy',
        'Unit Context',
        'Unit context and structure',
        'Unit context and structure, research and impact strategy',
        '1. Unit context, structure, research, open research environment, '\
        'strategic aims and',  # two lines
        '• Unit context and structure, research and impact strategy'
    ],
    'People': [
        '2. People',
        '2. 2. People',
        '2. People, including:',
        'c. People, including:',
        '2. People Staffing strategy',
        '2. Staffing strategy and staff development',
        '2. People: Staffing strategy and staff development',
        "People",
        'Section 2.',
        'Section 2. People',
        'Section 2: Staffing',
        'Section 2 (S2). People',
        "2.0 People",
        '2B 2. People',
        '3B 2. People',
        'Section 2: People – Note: All staff-related data in this section refer to '\
        'Cat. A submitted staff',
    ],
    'Income, infrastructure and facilities': [
        '3. Income, infrastructure and facilities',
        'Section 3. Income, infrastructure and facilities',
        'Section 3 (S3). Income, infrastructure and facilities',
        'Section 3. Income and infrastructure',
        'Income, infrastructure and facilities',
        'Section 3.',
        '4B 3. Income, infrastructure and facilities',
        '3.0 Income, infrastructure and facilities',
        '2. 3.0 Income, infrastructure and facilities',
        '3B 3. Income, infrastructure and facilities',
        'Section 3. Research Income, Infrastructure and Facilities',
        ],
    'Collaboration and contribution to the research base, economy and society': [
        '4. Collaboration and contribution to the research base, economy and society',
        '4. Collaboration and contribution to research base, economy and society',
        '4 Collaboration and contribution to the research base, economy',
        '4. Collaboration and contribution to the discipline or research base',
        '4. Collaboration and contribution to the research base, alumni, economy and society',
        '4. Collaboration and Contributions to the Research Base, Economy and Society',
        '4. Collaboration and contribution to the research base,',  # two lines
        '4. Section 4: Collaboration and contribution to the research base, economy and society',
        '4. Collaboration with and contribution to the research base, economy and society',
        '4. Collaborations and contributions to the research base, economy and society',
        '4. Collaboration, impact, engagement, responsiveness to emerging priorities and',
        '4. Collaboration and contribution to the research base, the economy and to society',
        '4.0 Collaboration and contribution to the research base, economy and society',
        '2B 4. Collaboration and contribution to the research base, economy and society',
        'Collaboration and contribution to the research base, economy and society',
        'Section 4. Collaboration and contribution to the research base, economy and society',
        'Section 4. Collaboration and contribution to the discipline or research base',
        'Section 4. Collaboration and contribution to the research base, economy and',  # two lines
        'SECTION 4. Collaboration and contribution to the research base,',  # two lines
        'Section 4: Collaboration or contribution to the research base, economy and society',
        'Section 4 (S4). Collaboration and contribution to the research base, economy and society',
        'Section D. Collaboration and contribution to the research base, economy, and society',
        '4.4 Contributions to, and recognition by, the research base',
        '5B 4. Collaboration and contribution to the research base, economy and society',
    ]
}


def get_and_clean_lines(statement):

    # split the statement into lines
    lines = statement.splitlines()

    # delete empty lines
    lines = [line for line in lines if line.strip()]

    # replace tabs with spaces
    lines = [line.replace('\t', ' ') for line in lines]

    # replace multiple spaces with a single space
    lines = [' '.join(line.split()) for line in lines]

    # delete lines with specified content
    lines = [line for line in lines
             if line.replace(" ", "").replace("\t", "").lower() not in TO_DELETE_PAGES]
    lines = [line for line in lines if line.lower() not in TO_DELETE_HEADERS]

    return lines


def clean_header(header):

    header = header.lower()
    for chars in CHARS_TO_DELETE_FROM_HEADER:
        header = header.replace(chars, "")

    return header


def section_indices(statement, sections):

    indices = [None for section in sections]

    lines = get_and_clean_lines(statement)

    for isection, (section, headers) in enumerate(sections.items()):
        headers_to_compare = [clean_header(header) for header in headers]

        for header in headers_to_compare:
            for iline, line in enumerate(lines):
                if header == clean_header(line):
                    indices[isection] = iline
                    break
            if indices[isection] is not None:
                break

    return (indices, lines)


def prepare_institution_statements(prefix="Institution environment statement - ", extension=".txt"):

    lg.print_tstamp("PPROC actions for institution environment statements")
    inputpath = os.path.join(rw.PROCESSED_ENV_EXTRACTED_PATH, "institution")
    outputpath = rw.PROCESSED_ENV_PREPARED_PATH
    # get the file names
    fnames = os.listdir(os.path.join(rw.PROJECT_PATH, inputpath))
    statement_count = len(fnames)
    fnames = [fname.replace(prefix, "").replace(extension, "") for fname in fnames]

    lg.print_tstamp(f"- read data from '{inputpath}' ")
    lg.print_tstamp(f"- statements: {statement_count}, "
                    f"sections: {len(SECTIONS_INSTITUTION.keys())}")

    dset = pd.DataFrame()
    counts = [0 for section in SECTIONS_INSTITUTION]
    for fname in fnames:
        institution_name = fname
        infname = os.path.join(inputpath, f"{prefix}{fname}{extension}")

        with open(infname, 'r+') as file:
            statement = file.read()
            (indices, lines) = section_indices(statement, SECTIONS_INSTITUTION)

        data = {cb.COL_INST_NAME: [institution_name]}
        for isection, section in enumerate(SECTIONS_INSTITUTION):
            if indices[isection] is not None:
                counts[isection] += 1
                if isection == len(SECTIONS_INSTITUTION) - 1:
                    section_lines = lines[indices[isection]:]
                else:
                    section_lines = lines[indices[isection]:indices[isection+1]]
                section_content = ' '.join(section_lines)
            else:
                section_content = None
            data[section] = section_content
            if section_content is None:
                lg.print_tstamp(f"- WARNING: no content for '{section}' in '{institution_name}'")

        dset = pd.concat([dset, pd.DataFrame(data)], ignore_index=True)

    lg.print_tstamp(f"- prepared institution statements: {dset.shape[0]} records, "
                    f"{dset.shape[1]} columns")
    if dset.shape[0] != statement_count:
        lg.print_tstamp(f"- WARNING: prepared institution statements "
                        f"{dset.shape[0]}/{statement_count}")

    fname = os.path.join(rw.PROJECT_PATH, outputpath,
                         "EnvStatementsInstitutionLevel.csv.gz")
    lg.print_tstamp(f"- write to '{fname}'")
    dset.to_csv(fname, index=False,
                compression='gzip')


def prepare_unit_statements(prefix="Unit environment statement - ", extension=".txt"):

    lg.print_tstamp("PPROC actions for unit environment statements")
    inputpath = os.path.join(rw.PROCESSED_ENV_EXTRACTED_PATH, "unit")
    outputpath = rw.PROCESSED_ENV_PREPARED_PATH
    # get the file names
    fnames = os.listdir(os.path.join(rw.PROJECT_PATH, inputpath))
    statement_count = len(fnames)
    fnames = [fname.replace(prefix, "").replace(extension, "") for fname in fnames]

    lg.print_tstamp(f"- read data from '{inputpath}' ")
    lg.print_tstamp(f"- statements: {statement_count}, sections: {len(SECTIONS_UNIT.keys())}")

    dset = pd.DataFrame()
    counts = [0 for section in SECTIONS_UNIT]
    for fname in fnames:
        institution_name, unit_code = fname.split(" - ")
        # strip any alphabetical characters from the unit code
        unit_code = ''.join([i for i in unit_code if not i.isalpha()])
        unit_name = cb.UOA_NAMES[int(unit_code)]
        infname = os.path.join(inputpath, f"{prefix}{fname}{extension}")

        with open(infname, 'r+') as file:
            statement = file.read()
            (indices, lines) = section_indices(statement, SECTIONS_UNIT)

        data = {cb.COL_INST_NAME: [institution_name],
                cb.COL_UOA_NAME: [unit_name]
                }
        for isection, section in enumerate(SECTIONS_UNIT):
            if indices[isection] is not None:
                counts[isection] += 1
                if isection == len(SECTIONS_UNIT) - 1:
                    section_lines = lines[indices[isection]:]
                else:
                    section_lines = lines[indices[isection]:indices[isection+1]]
                section_content = ' '.join(section_lines)
            else:
                section_content = None
            data[section] = section_content
            if section_content is None:
                lg.print_tstamp(f"- WARNING: no content for "
                                f"'{section}' in '{institution_name}' - '{unit_code}'")

        dset = pd.concat([dset, pd.DataFrame(data)], ignore_index=True)

    lg.print_tstamp(f"- prepared institution statements: {dset.shape[0]}")
    if dset.shape[0] != statement_count:
        lg.print_tstamp(f"- WARNING: prepared institution statements "
                        f"{dset.shape[0]}/{statement_count}")

    fname = os.path.join(rw.PROJECT_PATH, outputpath,
                         "EnvStatementsUnitLevel.csv.gz")
    lg.print_tstamp(f"- write to '{fname}'")
    dset.to_csv(fname, index=False,
                compression='gzip')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepares the extracted environment statements and saves them as csv file."
        )

    parser.add_argument("-e", "--envname",
                        required=True,
                        help="type of statements to prepare")

    args = parser.parse_args()
    ename = args.envname

    # redirect stdout to a buffer
    # ---------------------------
    buffer = StringIO()
    sys.stdout = buffer

    if ename == "institution":
        logfname = f"{rw.LOG_PREPARE_ENV_INSTITUTION}"
        prepare_institution_statements()
    elif ename == "unit":
        logfname = f"{rw.LOG_PREPARE_ENV_UNIT}"
        prepare_unit_statements()

    # restore stdout
    # --------------
    sys.stdout = sys.__stdout__

    print(buffer.getvalue())

    # save the log file
    # -----------------
    with open(os.path.join(rw.PROJECT_PATH, logfname), 'w') as f:
        f.write(buffer.getvalue())
