raw_fname = "data/raw/REF-2021-Submissions-All-2022-07-27.xlsx"
sheets = ["Outputs", "ImpactCaseStudies"]


rule all:
    input:
        {raw_fname},
        "logs/setup.log",
        f"logs/preprocess_{sheets[0]}.log",
        f"logs/preprocess_{sheets[1]}.log"
        
rule setup:
    output:
        "logs/setup.log"
    shell:
        "python src/setup.py"

rule extract_outputs:
    input:
        rules.setup.output,
    output:
        f"logs/extract_{sheets[0]}.log"
    shell:
        f"python src/extract_sheet.py -f {rules.all.input[0]} -s {sheets[0]}"

rule preprocess_outputs:
    input:
        rules.extract_outputs.output,
    output:
        f"logs/preprocess_{sheets[0]}.log"
    shell:
        f"python src/preprocess_sheet.py -s {sheets[0]}"


rule extract_impacts:
    input:
        rules.setup.output,
    output:
        f"logs/extract_{sheets[1]}.log"
    shell:
        f"python src/extract_sheet.py -f {rules.all.input[0]} -s {sheets[1]}"

rule preprocess_impacts:
    input:
        rules.extract_impacts.output,
    output:
        f"logs/preprocess_{sheets[1]}.log"
    shell:
        f"python src/preprocess_sheet.py -s {sheets[1]}"