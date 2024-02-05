
import REF2021_processing.read_write as rw

rule all:
    input:
        rw.rule_config("all", "input")

rule outputs:
    input:
        rw.rule_config("outputs", "input")
    output:
        rw.rule_config("outputs", "output")
    shell:
        rw.rule_config("outputs", "shell")

rule impacts:
    input:
        rw.rule_config("impacts", "input")
    output:
        rw.rule_config("impacts", "output")
    shell:
        rw.rule_config("impacts", "shell")


rule degrees:
    input:
        rw.rule_config("degrees", "input")
    output:
        rw.rule_config("degrees", "output")
    shell:
        rw.rule_config("degrees", "shell")

rule income:
    input:
        rw.rule_config("income", "input")
    output:
        rw.rule_config("income", "output")
    shell:
        rw.rule_config("income", "shell")

rule income_in_kind:
    input:
        rw.rule_config("income_in_kind", "input")
    output:
        rw.rule_config("income_in_kind", "output")
    shell:
        rw.rule_config("income_in_kind", "shell")

rule groups:
    input:
        rw.rule_config("groups", "input")
    output:
        rw.rule_config("groups", "output")
    shell:
        rw.rule_config("groups", "shell")

rule institution:
    input:
        rw.rule_config("institution", "input")
    output:
        rw.rule_config("institution", "output")
    shell:
        rw.rule_config("institution", "shell")

rule unit:
    input:
        rw.rule_config("unit", "input")
    output:
        rw.rule_config("unit", "output")
    shell:
        rw.rule_config("unit", "shell")

rule results:
    input:
        rw.rule_config("results", "input")
    output:
        rw.rule_config("results", "output")
    shell:
        rw.rule_config("results", "shell")

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
