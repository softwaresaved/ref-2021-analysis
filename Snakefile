# add src to PYTHONPATH
# ---------------------
import sys
sys.path.append('src/')
import read_write as rw

rule all:
    input:
        rw.RAW_SUBMISSIONS_FNAME,
        rw.LOG_SETUP,
        rw.LOG_PREPARE_ENV_INSTITUTION,
        rw.LOG_PREPARE_ENV_UNIT,
        rw.LOG_PPROC_OUTPUTS,
        rw.LOG_PPROC_IMPACTS,
        rw.LOG_PPROC_DEGREES,
        rw.LOG_PPROC_INCOME,
        rw.LOG_PPROC_INCOMEINKIND,
        rw.LOG_PPROC_RGROUPS,
        rw.LOG_PPROC_RESULTS
        
rule setup:
    output:
        rw.LOG_SETUP
    shell:
        "python src/setup.py"

# this rule is defined for completeness
# but it is not run because the unzipping fails due to the encoding
rule unzip_environment:
    input:
        rw.ENV_FNAME
    output:
        rw.LOG_UNZIP
    shell:
        "unzip {rw.ENV_FNAME} -O GB18030 -d {rw.RAW_ENV_PATH} 1> {rw.LOG_UNZIP}"
        "mv {rw.RAW_ENV_PATH}/Institution* {rw.ENV_INST_PATH}"
        "mv {rw.RAW_ENV_PATH}/Unit* {rw.ENV_UNIT_PATH}"

# prepare the environment statements
# ----------------------------------
rule prepare_environments_institution:
    input:
        rules.setup.output
    output:
        rw.LOG_PREPARE_ENV_INSTITUTION
    shell:
        "python src/prepare_envstatements.py -e {rw.ENV_INSTITUTION}"

rule prepare_environments_unit:
    input:
        rules.setup.output
    output:
        rw.LOG_PREPARE_ENV_UNIT
    shell:
        "python src/prepare_envstatements.py -e {rw.ENV_UNIT}"

# extract & preprocess OUTPUTS
# ----------------------------
rule extract_outputs:
    input:
        rules.setup.output
    output:
        rw.DATA_EXTRACT_OUTPUTS,
        rw.LOG_EXTRACT_OUTPUTS
    shell:
        "python src/extract_sheet.py -f {rw.RAW_SUBMISSIONS_FNAME} -s {rw.SHEET_OUTPUTS} -hr {rw.RAW_SUBMISSIONS_HEADER_INDEX}"

rule preprocess_outputs:
    input:
        rules.extract_outputs.output
    output:
        rw.LOG_PPROC_OUTPUTS
    shell:
        "python src/preprocess_sheet.py -s {rw.SHEET_OUTPUTS}"

# extract & preprocess IMPACT CASE STUDIES
# ----------------------------------------
rule extract_impacts:
    input:
        rules.setup.output
    output:
        rw.DATA_EXTRACT_IMPACTS,
        rw.LOG_EXTRACT_IMPACTS
    shell:
        "python src/extract_sheet.py -f {rw.RAW_SUBMISSIONS_FNAME} -s {rw.SHEET_IMPACTS} -hr {rw.RAW_SUBMISSIONS_HEADER_INDEX}"

rule preprocess_impacts:
    input:
        rules.extract_impacts.output
    output:
        rw.LOG_PPROC_IMPACTS
    shell:
        "python src/preprocess_sheet.py -s {rw.SHEET_IMPACTS}"  

# extract and preprocess RESEARCH DEGREES AWARDED
# -----------------------------------------------
rule extract_degrees:
    input:
        rules.setup.output
    output:
        rw.DATA_EXTRACT_DEGREES,
        rw.LOG_EXTRACT_DEGREES
    shell:
        "python src/extract_sheet.py -f {rw.RAW_SUBMISSIONS_FNAME} -s {rw.SHEET_DEGREES} -hr {rw.RAW_SUBMISSIONS_HEADER_INDEX}"

rule preprocess_degrees:
    input:
        rules.extract_degrees.output
    output:
        rw.LOG_PPROC_DEGREES
    shell:
        "python src/preprocess_sheet.py -s {rw.SHEET_DEGREES}"

# extrct and preprocess RESEARCH INCOME
# -------------------------------------
rule extract_income:
    input:
        rules.setup.output
    output:
        rw.DATA_EXTRACT_INCOME,
        rw.LOG_EXTRACT_INCOME
    shell:
        "python src/extract_sheet.py -f {rw.RAW_SUBMISSIONS_FNAME} -s {rw.SHEET_INCOME} -hr {rw.RAW_SUBMISSIONS_HEADER_INDEX}"

rule preprocess_income:
    input:
        rules.extract_income.output
    output:
        rw.LOG_PPROC_INCOME
    shell:
        "python src/preprocess_sheet.py -s {rw.SHEET_INCOME}"

# extract and preprocess RESEARCH INCOME IN KIND
# ----------------------------------------------
rule extract_income_in_kind:
    input:
        rules.setup.output
    output:
        rw.DATA_EXTRACT_INCOMEINKIND,
        rw.LOG_EXTRACT_INCOMEINKIND
    shell:
        "python src/extract_sheet.py -f {rw.RAW_SUBMISSIONS_FNAME} -s {rw.SHEET_INCOMEINKIND} -hr {rw.RAW_SUBMISSIONS_HEADER_INDEX}"

rule preprocess_income_in_kind:
    input:
        rules.extract_income_in_kind.output
    output:
        rw.LOG_PPROC_INCOMEINKIND
    shell:
        "python src/preprocess_sheet.py -s {rw.SHEET_INCOMEINKIND}"

# extract and preprocess RESEARCH GROUPS
# --------------------------------------
rule extract_rgroups:
    input:
        rules.setup.output
    output:
        rw.DATA_EXTRACT_RGROUPS,
        rw.LOG_EXTRACT_RGROUPS
    shell:
        "python src/extract_sheet.py -f {rw.RAW_SUBMISSIONS_FNAME} -s {rw.SHEET_RGROUPS} -hr {rw.RAW_SUBMISSIONS_HEADER_INDEX}"

rule preprocess_rgroups:
    input:
        rules.extract_rgroups.output
    output:
        rw.LOG_PPROC_RGROUPS
    shell:
        "python src/preprocess_sheet.py -s {rw.SHEET_RGROUPS}"    

# extract and preprocess RESULTS
# ------------------------------
rule extract_results:
    input:
        rules.setup.output
    output:
        rw.DATA_EXTRACT_RESULTS,
        rw.LOG_EXTRACT_RESULTS
    shell:
        "python src/extract_sheet.py -f {rw.RAW_RESULTS_FNAME} -s {rw.SHEET_RESULTS} -hr {rw.RAW_RESULTS_HEADER_INDEX}"

rule preprocess_results:
    input:
        rules.extract_results.output
    output:
        rw.LOG_PPROC_RESULTS
    shell:
        "python src/preprocess_sheet.py -s {rw.SHEET_RESULTS}"    
