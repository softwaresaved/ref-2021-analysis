""" Prepares the extracted environment statements. """
import argparse
import os
import logging
import pandas as pd

from REF2021_processing import utils
import REF2021_processing.read_write as rw
import REF2021_processing.codebook as cb

# include all that was noticed in the actual statements
TO_DELETE_HEADERS = [
    item.replace(" ", "").lower()
    for item in [
        "Institutional level environment template (REF5a)",
        "Institutional level environment template (REF5b)",
        "Unit-level environment template (REF5a)",
        "Unit-level environment template (REF5b)",
        "REF5a - Institution Environment Statement",
        "Institutional-Level Environment Statement (REF5a)",
    ]
]

CHARS_TO_DELETE_FROM_HEADER = [" ", "\t", ".", ",", ":", ";", "-", "and", "&"]

TO_DELETE_PAGES = [f"Page{i}".lower() for i in range(1, 100)]

SECTIONS_INSTITUTION = {
    "Context and mission": [
        "1. Institutional context and mission",
        "1. Context and mission",
        "a) Context and mission",
        "Context and mission",
        "Section 1: Context and mission",
        "1. Context and Vision",
        "1. Institutional overview",
        "1, 2. Context and mission; Strategy",
        "1B 1. Context and mission",
    ],
    "Strategy": [
        "2. Strategy",
        "b) Strategy",
        "2. Research and Impact Strategy",
        "2. Research strategy",
        "2B 2. Strategy",
        "Section 2: Strategy",
        "Strategy",
        "2. Strategy and Achievements",
        "2. Institutional Research and Impact Strategy",
        "2. Research and Knowledge Exchange Strategy",
        "Research at Cambridge",  # Cambridge merges the first two sections into one section
    ],
    "People": [
        "3. People",
        "c) People",
        "3B 3. People",
        "Section 3: People",
        "People",
        "3. Staffing",
    ],
    "Income, infrastructure and facilities": [
        "4. Income, infrastructure and facilities",
        "d) Income, infrastructure and facilities",
        "4B 4. Income, infrastructure and facilities",
        "Section 4: Income, infrastructure and facilities",
        "Income, infrastructure and facilities",
        "4.1 Income",
    ],
}

SECTIONS_UNIT = {
    "Unit context and structure, research and impact strategy": [
        "1. Unit context and structure, research and impact strategy",
        "1. Unit Context and Structure, Research and Impact Strategies",
        "1. Context and structure, research and impact strategy",
        "1. Unit Context, Research and Impact Strategy",
        "1. Unit Context & Structure, Research and impact",
        "1. Unit overview",
        "1. Unit context",
        "1. Overview and mission",
        "1. Context, Structure, and Strategy",
        "1. Unit Context and structure:",
        "1. Context, Strategy, and Structure: Overview",
        "1.0 Unit Context and structure",
        "1.0 Unit context and structure, research and impact strategy:",
        "1.1. Context and structure",
        "1.1 Unit context and structure, research and impact strategy",
        "1.1: Institutional Context and Structure",  # The Glasgow School of Art
        "1. Unit Context and Structure; Research and Impact strategy",
        "1 Unit context and structure, research and impact",
        "1B 1. Unit context and structure, research and impact strategy",
        "2B 1. Unit context and structure, research and impact strategy",
        "Section 1.",
        "Section 1. Unit context and structure, research and impact strategy",
        "Section 1. Unit structure, research and impact strategy",
        "Section 1: Unit Context, Research and Impact Strategy",
        "Section 1: Unit Context",
        "Section 1: Context and Structure",
        "Section 1: Unit Context and Structure",
        "Section 1 (S1). Unit context and structure, research and impact strategy",
        "Unit Context",
        "Unit context and structure",
        "Unit context and structure, research and impact strategy",
        "1. Unit context, structure, research, open research environment, "
        "strategic aims and",  # two lines
        "• Unit context and structure, research and impact strategy",
    ],
    "People": [
        "2. People",
        "2. 2. People",
        "2. People, including:",
        "c. People, including:",
        "2. People Staffing strategy",
        "2. Staffing strategy and staff development",
        "2. People: Staffing strategy and staff development",
        "People",
        "Section 2.",
        "Section 2. People",
        "Section 2: Staffing",
        "Section 2 (S2). People",
        "2.0 People",
        "2B 2. People",
        "3B 2. People",
        "Section 2: People – Note: All staff-related data in this section refer to "
        "Cat. A submitted staff",
    ],
    "Income, infrastructure and facilities": [
        "3. Income, infrastructure and facilities",
        "Section 3. Income, infrastructure and facilities",
        "Section 3 (S3). Income, infrastructure and facilities",
        "Section 3. Income and infrastructure",
        "Income, infrastructure and facilities",
        "Section 3.",
        "4B 3. Income, infrastructure and facilities",
        "3.0 Income, infrastructure and facilities",
        "2. 3.0 Income, infrastructure and facilities",
        "3B 3. Income, infrastructure and facilities",
        "Section 3. Research Income, Infrastructure and Facilities",
    ],
    "Collaboration and contribution to the research base, economy and society": [
        "4. Collaboration and contribution to the research base, economy and society",
        "4. Collaboration and contribution to research base, economy and society",
        "4 Collaboration and contribution to the research base, economy",
        "4. Collaboration and contribution to the discipline or research base",
        "4. Collaboration and contribution to the research base, alumni, economy and society",
        "4. Collaboration and Contributions to the Research Base, Economy and Society",
        "4. Collaboration and contribution to the research base,",  # two lines
        "4. Section 4: Collaboration and contribution to the research base, economy and society",
        "4. Collaboration with and contribution to the research base, economy and society",
        "4. Collaborations and contributions to the research base, economy and society",
        "4. Collaboration, impact, engagement, responsiveness to emerging priorities and",
        "4. Collaboration and contribution to the research base, the economy and to society",
        "4.0 Collaboration and contribution to the research base, economy and society",
        "2B 4. Collaboration and contribution to the research base, economy and society",
        "Collaboration and contribution to the research base, economy and society",
        "Section 4. Collaboration and contribution to the research base, economy and society",
        "Section 4. Collaboration and contribution to the discipline or research base",
        "Section 4. Collaboration and contribution to the research base, economy and",  # two lines
        "SECTION 4. Collaboration and contribution to the research base,",  # two lines
        "Section 4: Collaboration or contribution to the research base, economy and society",
        "Section 4 (S4). Collaboration and contribution to the research base, economy and society",
        "Section D. Collaboration and contribution to the research base, economy, and society",
        "4.4 Contributions to, and recognition by, the research base",
        "5B 4. Collaboration and contribution to the research base, economy and society",
    ],
}


def get_and_clean_lines(statement):
    """Splits the statement into lines and cleans them.

    Args:
        statement (str): the statement to be cleaned

    Returns:
        list: the cleaned lines
    """

    # split the statement into lines
    lines = statement.splitlines()

    # delete empty lines
    lines = [line for line in lines if line.strip()]

    # replace tabs with spaces
    lines = [line.replace("\t", " ") for line in lines]

    # replace multiple spaces with a single space
    lines = [" ".join(line.split()) for line in lines]

    # delete lines with specified content
    lines = [
        line
        for line in lines
        if line.replace(" ", "").replace("\t", "").lower() not in TO_DELETE_PAGES
    ]
    lines = [line for line in lines if line.lower() not in TO_DELETE_HEADERS]

    return lines


def clean_header(header):
    """Cleans the header.

    Args:
        header (str): the header to be cleaned

    Returns:
        str: the cleaned header
    """

    header = header.lower()
    for chars in CHARS_TO_DELETE_FROM_HEADER:
        header = header.replace(chars, "")

    return header


def section_indices(statement, sections):
    """Finds the indices of the sections in the statement.

    Args:
        statement (str): the statement to be searched
        sections (dict): the sections to be searched for

    Returns:
        tuple: the indices of the sections in the statement and the lines of the statement
    """

    indices = [None for section in sections]

    lines = get_and_clean_lines(statement)

    for isection, (section, headers) in enumerate(sections.items()):
        for header in [clean_header(header) for header in headers]:
            for iline, line in enumerate(lines):
                if header == clean_header(line):
                    indices[isection] = iline
                    break
            if indices[isection] is not None:
                break

    return (indices, lines)


def prepare_institution_statements():
    """Prepares the institution statements."""

    source_config = rw.SOURCES["environment_statements"]["institution"]

    # get the file names
    fnames = os.listdir(os.path.join(rw.PROJECT_PATH, source_config["extracted_path"]))

    # remove the prefix and the extension
    fnames = [
        fname.replace(source_config["prefix"], "").replace(
            source_config["input_extension"], ""
        )
        for fname in fnames
    ]
    logging.info(
        "%s - read data from '%s' ",
        source_config["name"],
        source_config["extracted_path"],
    )
    logging.info(
        "%s - statements: %d, sections: %d",
        source_config["name"],
        len(fnames),
        len(SECTIONS_INSTITUTION.keys()),
    )

    # initialise the dataset and the counts
    dset = pd.DataFrame()
    counts = [0 for section in SECTIONS_INSTITUTION]
    for institution_name in fnames:
        infname = os.path.join(
            source_config["extracted_path"],
            f"{source_config['prefix']}{institution_name}{source_config['input_extension']}",
        )

        with open(infname, "r+", encoding="utf-8") as file:
            statement = file.read()
            (indices, lines) = section_indices(statement, SECTIONS_INSTITUTION)

        # assign the institution name
        data = {cb.COL_INST_NAME: [institution_name]}

        # extract the content of the sections
        for isection, section in enumerate(SECTIONS_INSTITUTION):
            if indices[isection] is not None:
                counts[isection] += 1
                if isection == len(SECTIONS_INSTITUTION) - 1:
                    section_lines = lines[indices[isection] :]
                else:
                    section_lines = lines[indices[isection] : indices[isection + 1]]
                section_content = " ".join(section_lines)
            else:
                section_content = None
            data[section] = section_content
            if section_content is None:
                logging.warning(
                    "%s - no content for '%s' in '%s'",
                    source_config["name"],
                    section,
                    institution_name,
                )

        # add the current extracted data to the dataset
        dset = pd.concat([dset, pd.DataFrame(data)], ignore_index=True)

    logging.info(
        "%s - prepared institution statements: %d records, %d columns",
        source_config["name"],
        dset.shape[0],
        dset.shape[1],
    )

    # report mistamatches in the number of prepared statements
    if dset.shape[0] != len(fnames):
        logging.warning(
            "%s - prepared statements %d/%d statements",
            source_config["name"],
            dset.shape[0],
            len(fnames),
        )

    # set the index name and save the prepared data
    dset.index.name = "Record"
    rw.export_dataframe(
        dset,
        os.path.join(
            rw.SOURCES["environment_statements"]["institution"]["output_path"],
            source_config["name"],
        ),
        source_config["name"],
    )


def prepare_unit_statements():
    """Prepares the unit statements."""

    source_config = rw.SOURCES["environment_statements"]["unit"]

    # get the file names
    fnames = os.listdir(os.path.join(rw.PROJECT_PATH, source_config["extracted_path"]))
    fnames = [
        fname.replace(source_config["prefix"], "").replace(
            source_config["input_extension"], ""
        )
        for fname in fnames
    ]

    logging.info(
        "%s - read data from '%s' ",
        source_config["name"],
        source_config["extracted_path"],
    )
    logging.info(
        "%s - statements: %d, sections: %d",
        source_config["name"],
        len(fnames),
        len(SECTIONS_UNIT.keys()),
    )

    # initialise dataset
    dset = pd.DataFrame()
    for fname in fnames:
        institution_name, unit_code_original = fname.split(" - ")

        # process tbe unit code and the multiple submission letter
        unit_code = "".join([i for i in unit_code_original if not i.isalpha()])
        multiple_submission_letter = ""
        if len(unit_code) != len(unit_code_original):
            multiple_submission_letter = unit_code_original[-1]

        with open(
            os.path.join(
                source_config["extracted_path"],
                f"{source_config['prefix']}{fname}{source_config['input_extension']}",
            ),
            "r+",
            encoding="utf-8",
        ) as file:
            statement = file.read()
            (indices, lines) = section_indices(statement, SECTIONS_UNIT)

        data = {
            cb.COL_INST_NAME: [institution_name],
            cb.COL_UOA_NAME: [cb.UOA_NAMES[int(unit_code)]],
            cb.COL_MULT_SUB_LETTER: [multiple_submission_letter],
        }
        # extract the content of the sections
        for isection, section in enumerate(SECTIONS_UNIT):
            if indices[isection] is not None:
                if isection == len(SECTIONS_UNIT) - 1:
                    section_lines = lines[indices[isection] :]
                else:
                    section_lines = lines[indices[isection] : indices[isection + 1]]
                section_content = " ".join(section_lines)
            else:
                section_content = None
            data[section] = section_content
            if section_content is None:
                logging.warning(
                    "%s - no content for '%s' in '%s' - '%s'",
                    source_config["name"],
                    section,
                    institution_name,
                    unit_code,
                )

        # add the current extracted data to the dataset
        dset = pd.concat([dset, pd.DataFrame(data)], ignore_index=True)

    logging.info(
        "%s - prepared statements: %d records", source_config["name"], dset.shape[0]
    )

    # report mistamatches in the number of prepared statements
    if dset.shape[0] != len(fnames):
        logging.warning(
            "%s - prepared statements %d/%d statements",
            source_config["name"],
            dset.shape[0],
            len(fnames),
        )

    # set the index name and save the prepared data
    dset.index.name = "Record"
    rw.export_dataframe(
        dset,
        os.path.join(
            rw.SOURCES["environment_statements"]["institution"]["output_path"],
            source_config["name"],
        ),
        source_config["name"],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepares the extracted environment statements and saves them as csv file."
    )

    parser.add_argument(
        "-s", "--source", required=True, help="source for the environment statements"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        required=False,
        default=False,
        help="write logging to console, default false",
    )

    args = parser.parse_args()
    source = args.source
    source_name = rw.SOURCES["environment_statements"][source]["name"]

    STATUS = utils.setup_logger(source_name, verbose=args.verbose)

    if STATUS:
        if source == "institution":
            prepare_institution_statements()
        elif source == "unit":
            prepare_unit_statements()

        utils.complete_logger(source_name, verbose=args.verbose)
    else:
        print(f"{utils.FAILED_ICON} no preparation done")
