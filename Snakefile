# add src to PYTHONPATH
# ---------------------
import sys
sys.path.append('src/')
import read_write as rw

rule all:
    input:
        rw.RAW_SUBMISSIONS_FNAME,
        f"{rw.LOG_PATH}{rw.LOG_PPROC_RGROUPS}",
        f"{rw.LOG_PATH}{rw.LOG_PPROC_DEGREES}",
        f"{rw.LOG_PATH}{rw.LOG_PPROC_INCOME}",
        f"{rw.LOG_PATH}{rw.LOG_PPROC_INCOMEINKIND}",
        f"{rw.LOG_PATH}{rw.LOG_PPROC_OUTPUTS}",
        # f"{rw.LOG_PATH}{rw.LOG_PPROC_IMPACTS}",
        # f"{rw.LOG_PATH}{rw.LOG_PREPARE_ENV_INSTITUTION}",
        # f"{rw.LOG_PATH}{rw.LOG_PREPARE_ENV_UNIT}",
        # f"{rw.LOG_PATH}{rw.LOG_PPROC_RESULTS}"

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

rule preprocess_rgroups:
    input:
        rw.RAW_SUBMISSIONS_FNAME
    output:
        f"{rw.LOG_PATH}{rw.LOG_PPROC_RGROUPS}"
    shell:
        "python src/preprocess_sheet.py -s {rw.SHEET_RGROUPS}"    

rule preprocess_degrees:
    input:
        rw.RAW_SUBMISSIONS_FNAME
    output:
        f"{rw.LOG_PATH}{rw.LOG_PPROC_DEGREES}"
    shell:
        "python src/preprocess_sheet.py -s {rw.SHEET_DEGREES}" 

rule preprocess_income:
    input:
        rw.RAW_SUBMISSIONS_FNAME
    output:
        f"{rw.LOG_PATH}{rw.LOG_PPROC_INCOME}"
    shell:
        "python src/preprocess_sheet.py -s {rw.SHEET_INCOME}" 

rule preprocess_incomeinkind:
    input:
        rw.RAW_SUBMISSIONS_FNAME
    output:
        f"{rw.LOG_PATH}{rw.LOG_PPROC_INCOMEINKIND}"
    shell:
        "python src/preprocess_sheet.py -s {rw.SHEET_INCOMEINKIND}"  

rule preprocess_outputs:
    input:
        rw.RAW_SUBMISSIONS_FNAME
    output:
        f"{rw.LOG_PATH}{rw.LOG_PPROC_OUTPUTS}"
    shell:
        "python src/preprocess_sheet.py -s {rw.SHEET_OUTPUTS}"

rule preprocess_impacts:
    input:
        rw.RAW_SUBMISSIONS_FNAME
    output:
        f"{rw.LOG_PATH}{rw.LOG_PPROC_IMPACTS}"
    shell:
        "python src/preprocess_sheet.py -s {rw.SHEET_IMPACTS}"

# prepare the environment statements
# ----------------------------------
rule prepare_environments_institution:
    output:
        rw.LOG_PREPARE_ENV_INSTITUTION
    shell:
        "python src/prepare_envstatements.py -e {rw.ENV_INSTITUTION}"

rule prepare_environments_unit:
    output:
        rw.LOG_PREPARE_ENV_UNIT
    shell:
        "python src/prepare_envstatements.py -e {rw.ENV_UNIT}"


rule preprocess_results:
    input:
        rw.RAW_RESULTS_FNAME,
        f"{rw.LOG_PATH}{rw.LOG_PPROC_RGROUPS}",
        f"{rw.LOG_PATH}{rw.LOG_PPROC_RGROUPS}",
        f"{rw.LOG_PATH}{rw.LOG_PPROC_DEGREES}",
        f"{rw.LOG_PATH}{rw.LOG_PPROC_INCOME}",
        f"{rw.LOG_PATH}{rw.LOG_PPROC_INCOMEINKIND}",
        f"{rw.LOG_PATH}{rw.LOG_PPROC_OUTPUTS}",
        f"{rw.LOG_PATH}{rw.LOG_PPROC_IMPACTS}",
        f"{rw.LOG_PATH}{rw.LOG_PREPARE_ENV_INSTITUTION}",
        f"{rw.LOG_PATH}{rw.LOG_PREPARE_ENV_UNIT}"
    output:
        f"{rw.LOG_PATH}{rw.LOG_PPROC_RESULTS}"
    shell:
        "python src/preprocess_sheet.py -s {rw.SHEET_RESULTS}" 
        
