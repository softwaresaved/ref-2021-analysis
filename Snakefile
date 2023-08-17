raw_fname = "data/raw/REF-2021-Submissions-All-2022-07-27.xlsx"
sheets = ["Outputs", "ImpactCaseStudies"]


rule all:
    input:
        {raw_fname},
        "logs/setup_log.txt",
        f"logs/extract_{sheets[0]}_log.txt",
        f"logs/extract_{sheets[1]}_log.txt"
        
rule setup:
    output:
        "logs/setup_log.txt"
    shell:
        "python src/setup.py"

rule extract_outputs:
    input:
        rules.setup.output,
    output:
        f"logs/extract_{sheets[0]}_log.txt"
    shell:
        f"python src/extract_sheet.py -f {rules.all.input[0]} -s {sheets[0]}"

rule extract_impacts:
    input:
        rules.setup.output,
    output:
        f"logs/extract_{sheets[1]}_log.txt"
    shell:
        f"python src/extract_sheet.py -f {rules.all.input[0]} -s {sheets[1]}"
