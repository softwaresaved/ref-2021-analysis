rule all:
    input:
        "data/raw/REF-2021-Submissions-All-2022-07-27.xlsx",
        "logs/setup_log.txt",
        "logs/extract_Outputs_log.txt",
        "logs/extract_ImpactCaseStudies_log.txt"
        
rule setup:
    output:
        "logs/setup_log.txt"
    shell:
        "python src/setup.py"

rule extract_outputs:
    input:
        rules.setup.output,
    output:
        "logs/extract_Outputs_log.txt"
    shell:
        "python src/extract_sheet.py -f {rules.all.input[0]} -s Outputs"

rule extract_impacts:
    input:
        rules.setup.output,
    output:
        "logs/extract_ImpactCaseStudies_log.txt"
    shell:
        "python src/extract_sheet.py -f {rules.all.input[0]} -s ImpactCaseStudies"
