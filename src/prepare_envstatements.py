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

TO_DELETE_PAGES = [f"Page{i}".lower() for i in range(1, 100)]

SECTIONS_INSTITUTION = {
    'Context and mission': [
        '1. Institutional context and mission',
        '1. Context and mission',
        '1 Context and mission',
        '1: Context and mission',
        'a) Context and mission',
        'Context and mission',
        'Section 1: Context and mission',
        '1. Context and Vision',
        '1. Institutional overview',
        '1, 2. Context and mission; Strategy',
        '1B 1. Context and mission'],
    'Strategy': [
        '2. Strategy',
        '2 Strategy',
        '2: Strategy',
        'b) Strategy',
        '2. Research and Impact Strategy',
        '2. Research strategy',
        '2B 2. Strategy',
        'Section 2: Strategy',
        'Strategy',
        '2. Strategy and Achievements',
        '2. Institutional Research and Impact Strategy',
        '2. Research and Knowledge Exchange Strategy',
        'Research at Cambridge'],
    'People': [
        '3. People',
        '3 People',
        '3: People',
        'c) People',
        '3B 3. People',
        'Section 3: People',
        'People',
        '3. Staffing'],
    'Income, infrastructure and facilities': [
        '4. Income, infrastructure and facilities',
        '4 Income, infrastructure and facilities',
        '4: Income, infrastructure and facilities',
        'd) Income, infrastructure and facilities',
        '4B 4. Income, infrastructure and facilities',
        'Section 4: Income, infrastructure and facilities',
        'Income, infrastructure and facilities',
        '4. Income, infrastructure, and facilities',
        'd) Income, infrastructure, and facilities',
        '4.1 Income'
        ]
}

SECTIONS_UNIT = {
    # 'Unit context and structure, research and impact strategy': [
    #     '1. Unit context and structure, research and impact strategy',
    #     '1 Unit context and structure, research and impact strategy',
    #     'Section 1. Unit context and structure, research and impact strategy',
    #     '1.1 Unit context and structure, research and impact strategy',
    #     'Section 1: Unit context and structure, research and impact strategy',
    #     '1. Unit context and structure, research, and impact strategy',
    #     'Unit context and structure, research and impact strategy',
    #     'A. Unit context and structure, research and impact strategy',
    #     '1: UNIT CONTEXT AND STRUCTURE, RESEARCH AND IMPACT STRATEGY',
    #     'Section 1. Unit context and structure',
    #     '1 Unit context and structure, research, and impact strategy',
    #     'Section 1. Unit context and structure, research, and impact strategy',
    #     '1. Unit Context and structure:',
    #     'Section 1: Unit context and structure, research, and impact strategy',
    #     '2B 1. Unit context and structure, research and impact strategy',
    #     '1. Unit context, research and impact strategy',
    #     '• Unit context and structure, research and impact strategy',
    #     'Section 1. Unit context and structure; research and impact strategy',
    #     'Unit Context',
    #     'Section 1: Unit context, research and impact strategy',
    #     'Section 1.',
    #     'Section 1 (S1). Unit context and structure, research and impact strategy',
    #     '1.0 Unit context and structure, research and impact strategy:',
    #     '1. 1. Unit context and structure, research and impact strategy',
    #     '1. Unit Context and Structure, Research and Impact Strategies',
    #     '1.0 Unit Context and structure',
    #     '1.1: Institutional Context and Structure',  # The Glasgow School of Art
    #     '1: Context, structure, research and impact strategy',
    #     '1.Unit context and structure, research and impact strategy',
    #     '1. Unit context and structure',
    #     'Section 1 Unit context and structure, research and impact strategy',
    #     'Section 1: Context and Structure',
    #     'Section 1. Unit context and structure, research and impact strategy.',
    #     '1B 1. Unit context and structure, research and impact strategy',
    #     '1. Unit context and structure research and impact strategy',
    #     '1. Context and mission',
    #     'Unit context and structure, research, and impact strategy',
    #     '1. UNIT CONTEXT & STRUCTURE, RESEARCH AND IMPACT',
    #     '1. Context, Strategy, and Structure: Overview',
    #     '1.1. Context and structure',
    #     '1. Unit context',
    #     '1.Unit Context, Structure, Research And Impact Strategy',
    #     'Section 1. UNIT STRUCTURE, RESEARCH AND IMPACT STRATEGY',
    #     '1. Unit context, structure, research, open research environment, strategic aims and',
    #     '1.1. Overview',
    #     '1. Unit Context and Structure; Research and Impact strategy',
    #     '1. UNIT CONTEXT AND STRUCTURE, RESEARCH AND IMPACT',
    #     '1. Context, structure and strategy',
    #     'SECTION 1. UNIT CONTEXT, RESEARCH AND IMPACT STRATEGY',
    #     '1. Unit context and structure, research and impact strategy.',
    #     'Section 1. Unit context, structure, and research and impact strategy',
    #     '1. Unit context, structure, research, and impact strategy',
    #     '1. Unit context and structure, research strategy',
    #     '1. Context, Structure, and Strategy',
    #     '1: Context and structure, research and impact strategy',
    #     '1. Overview and mission',
    #     '1 Unit context and structure, research and impact',
    #     '1. Unit context, structure, research and impact strategy',
    #     'Section 1: Unit Context',
    #     '1. Unit overview',
    #     'Section 1: Unit Context and Structure',
    #     'Overview',
    # ]
    "People": [
        '2. People',
        "2 People",
        "2: People",
        "2. People.",
        '2. 2. People',
        '2.People',
        "Section 2. People",
        "Section 2: People",
        "2.0 People",
        "People",
        '3B 2. People',
        '2. People, including:',
        'Section 2 (S2). People',
        '2. Staffing strategy and staff development',
        '2. People Staffing strategy',
        'Section 2 - People',
        '2B 2. People',
        'Section 2.',
        '2. People: Staffing strategy and staff development',
        'Section 2: People – Note: All staff-related data in this section refer to Cat. A submitted staff',
        'c. People, including:',
        'Section 2: Staffing'
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


def section_indices(statement, sections):

    indices = [None for section in sections]

    lines = get_and_clean_lines(statement)

    for isection, (section, headers) in enumerate(sections.items()):
        for header in headers:
            for iline, line in enumerate(lines):
                if header.lower() == line.lower():
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

    lg.print_tstamp(f"- '{inputpath}' statements: {statement_count}")

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
                    section_lines = lines[(indices[isection]+1):]
                else:
                    section_lines = lines[indices[isection]+1:indices[isection+1]]
                section_content = ' '.join(section_lines)
            else:
                section_content = None
            data[section] = section_content
            if section_content is None:
                lg.print_tstamp(f"- WARNING: no content for '{section}' in '{institution_name}'")

        dset = pd.concat([dset, pd.DataFrame(data)], ignore_index=True)

    lg.print_tstamp(f"- prepared institution statements: {dset.shape[0]}")
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

    lg.print_tstamp(f"- '{inputpath}' statements: {statement_count}")

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
                    section_lines = lines[(indices[isection]+1):]
                else:
                    section_lines = lines[indices[isection]+1:indices[isection+1]]
                section_content = ' '.join(section_lines)
            else:
                section_content = None
            data[section] = section_content
            if section_content is None:
                lg.print_tstamp(f"- WARNING: no content for '{section}' in '{institution_name}' - '{unit_code}'")
                print(infname)
                break

        dset = pd.concat([dset, pd.DataFrame(data)], ignore_index=True)
    print(counts, statement_count)
    # lg.print_tstamp(f"- prepared institution statements: {dset.shape[0]}")
    # if dset.shape[0] != statement_count:
    #     lg.print_tstamp(f"- WARNING: prepared institution statements "
    #                     f"{dset.shape[0]}/{statement_count}")

    # fname = os.path.join(rw.PROJECT_PATH, outputpath,
    #                      "EnvStatementsInstitutionLevel.csv.gz")
    # lg.print_tstamp(f"- write to '{fname}'")
    # dset.to_csv(fname, index=False,
    #             compression='gzip')


# def prepare_unit_statements_old(prefix="Unit environment statement - ", extension=".txt"):

#     lg.print_tstamp("PPROC actions for unit envinroment statements")
#     inputpath = os.path.join(rw.PROCESSED_ENV_EXTRACTED_PATH, "unit")
#     outputpath = rw.PROCESSED_ENV_PREPARED_PATH
#     fnames = os.listdir(os.path.join(rw.PROJECT_PATH, inputpath))
#     lg.print_tstamp(f"- '{inputpath}' statements: {len(fnames)}")
#     fnames = [fname.replace(prefix, "").replace(extension, "") for fname in fnames]

#     dset = pd.DataFrame()
#     for fname in fnames:
#         institution_name, unit_code = fname.split(" - ")
#         # strip any alphabetical characters from the unit code
#         unit_code = ''.join([i for i in unit_code if not i.isalpha()])
#         unit_name = cb.UOA_NAMES[int(unit_code)]

#         infname = os.path.join(inputpath, f"{prefix}{fname}{extension}")

#         with open(infname, 'r+') as file:
#             content = file.read()
#             content = clean_content(content)
#         dset = pd.concat([dset,
#                           pd.DataFrame({cb.COL_INST_NAME: [institution_name],
#                                         cb.COL_UOA_NAME: [unit_name],
#                                         cb.COL_ENV_STATEMENT: [content]}
#                                        )],
#                          ignore_index=True)
#     lg.print_tstamp(f"- aggregated {dset.shape[0]} statements")

#     fname_root = "EnvStatementsUnitLevel"
#     # save all the statements to a single csv file
#     fname = os.path.join(rw.PROJECT_PATH, outputpath,
#                          f"{fname_root}.csv.gz")
#     lg.print_tstamp(f"- write to '{fname}'")
#     dset.to_csv(fname, index=False, compression='gzip')

#     # split the DataFrame in four and save them to separate CSV files
#     quarter_index = len(dset) // 4
#     fname = os.path.join(rw.PROJECT_PATH, outputpath,
#                          f"{fname_root}_1.csv.gz")
#     lg.print_tstamp(f"- write to '{fname}'")
#     dset.iloc[:quarter_index].to_csv(fname, index=False,
#                                      compression='gzip')

#     fname = os.path.join(rw.PROJECT_PATH, outputpath,
#                          f"{fname_root}_2.csv.gz")
#     lg.print_tstamp(f"- write to '{fname}'")
#     dset.iloc[quarter_index:2*quarter_index].to_csv(fname, index=False,
#                                                     compression='gzip')

#     fname = os.path.join(rw.PROJECT_PATH, outputpath,
#                          f"{fname_root}_3.csv.gz")
#     lg.print_tstamp(f"- write to '{fname}'")
#     dset.iloc[2*quarter_index:3*quarter_index].to_csv(fname, index=False,
#                                                       compression='gzip')

#     fname = os.path.join(rw.PROJECT_PATH, outputpath,
#                          f"{fname_root}_4.csv.gz")
#     lg.print_tstamp(f"- write to '{fname}'")
#     dset.iloc[3*quarter_index:].to_csv(fname, index=False,
#                                        compression='gzip')


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
