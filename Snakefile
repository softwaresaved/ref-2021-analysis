
import REF2021_processing.read_write as rw

rule all:
    input:
        rw.rule_all()

rule outputs:
    input:
        rw.rule_submission_sheet("outputs", "input")
    output:
        rw.rule_submission_sheet("outputs", "output")
    shell:
        rw.rule_submission_sheet("outputs", "shell")

rule impacts:
    input:
        rw.rule_submission_sheet("impacts", "input")
    output:
        rw.rule_submission_sheet("impacts", "output")
    shell:
        rw.rule_submission_sheet("impacts", "shell")


rule degrees:
    input:
        rw.rule_submission_sheet("degrees", "input")
    output:
        rw.rule_submission_sheet("degrees", "output")
    shell:
        rw.rule_submission_sheet("degrees", "shell")

rule income:
    input:
        rw.rule_submission_sheet("income", "input")
    output:
        rw.rule_submission_sheet("income", "output")
    shell:
        rw.rule_submission_sheet("income", "shell")

rule income_in_kind:
    input:
        rw.rule_submission_sheet("income_in_kind", "input")
    output:
        rw.rule_submission_sheet("income_in_kind", "output")
    shell:
        rw.rule_submission_sheet("income_in_kind", "shell")

rule groups:
    input:
        rw.rule_submission_sheet("groups", "input")
    output:
        rw.rule_submission_sheet("groups", "output")
    shell:
        rw.rule_submission_sheet("groups", "shell")

rule institution:
    input:
        rw.rule_envstatements("institution", "input")
    output:
        rw.rule_envstatements("institution", "output")
    shell:
        rw.rule_envstatements("institution", "shell")

rule unit:
    input:
        rw.rule_envstatements("unit", "input")
    output:
        rw.rule_envstatements("unit", "output")
    shell:
        rw.rule_envstatements("unit", "shell")

rule results:
    input:
        rw.rule_results("input")
    output:
        rw.rule_results("output")
    shell:
        rw.rule_results("shell")

# this rule is defined for completeness
# but it is not run because the unzipping fails due to the encoding
# rule unzip_environment:
#     input:
#         rw.ENV_FNAME
#     output:
#         rw.LOG_UNZIP
#     shell:
#         "unzip {rw.ENV_FNAME} -O GB18030 -d {rw.RAW_ENV_PATH} 1> {rw.LOG_UNZIP}"
#         "mv {rw.RAW_ENV_PATH}/Institution* {rw.ENV_INST_PATH}"
#         "mv {rw.RAW_ENV_PATH}/Unit* {rw.ENV_UNIT_PATH}"
