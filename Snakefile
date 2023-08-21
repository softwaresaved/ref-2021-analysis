raw_fname = "data/raw/REF-2021-Submissions-All-2022-07-27.xlsx"
log_folder = "logs/"
log_ext = ".log"
log_setup = f"{log_folder}setup{log_ext}"
log_extract = f"{log_folder}extract_"
log_ppreprocess = f"{log_folder}preprocess_"
sheets = ["Outputs", 
          "ImpactCaseStudies",
          "ResearchDoctoralDegreesAwarded",
          "ResearchIncome", 
          "ResearchIncomeInKind",
          "ResearchGroups"]


rule all:
    input:
        {raw_fname},
        log_setup,
        f"{log_ppreprocess}{sheets[0]}{log_ext}",
        f"{log_ppreprocess}{sheets[1]}{log_ext}",
        f"{log_ppreprocess}{sheets[2]}{log_ext}",
        f"{log_ppreprocess}{sheets[3]}{log_ext}",
        f"{log_ppreprocess}{sheets[4]}{log_ext}",
        f"{log_ppreprocess}{sheets[5]}{log_ext}"
        
rule setup:
    output:
        log_setup
    shell:
        "python src/setup.py"

# extract & preprocess OUTPUTS
# ----------------------------
rule extract_outputs:
    input:
        rules.setup.output,
    output:
        f"{log_extract}{sheets[0]}{log_ext}"
    shell:
        f"python src/extract_sheet.py -f {rules.all.input[0]} -s {sheets[0]}"

rule preprocess_outputs:
    input:
        rules.extract_outputs.output,
    output:
        f"{log_ppreprocess}{sheets[0]}{log_ext}"
    shell:
        f"python src/preprocess_sheet.py -s {sheets[0]}"

# extract & preprocess IMPACT CASE STUDIES
# ----------------------------------------
rule extract_impacts:
    input:
        rules.setup.output,
    output:
        f"{log_extract}{sheets[1]}{log_ext}"
    shell:
        f"python src/extract_sheet.py -f {rules.all.input[0]} -s {sheets[1]}"

rule preprocess_impacts:
    input:
        rules.extract_impacts.output,
    output:
        f"{log_ppreprocess}{sheets[1]}{log_ext}"
    shell:
        f"python src/preprocess_sheet.py -s {sheets[1]}"

# extract & preprocess RESEARCH DEGREES AWARDED
# ---------------------------------------------
rule extract_degrees:
    input:
        rules.setup.output,
    output:
        f"{log_extract}{sheets[2]}{log_ext}"
    shell:
        f"python src/extract_sheet.py -f {rules.all.input[0]} -s {sheets[2]}"

rule preprocess_degrees:
    input:
        rules.extract_degrees.output,
    output:
        f"{log_ppreprocess}{sheets[2]}{log_ext}"
    shell:
        f"python src/preprocess_sheet.py -s {sheets[2]}"

# extract & preprocess RESEARCH INCOME
# ------------------------------------
rule extract_income:
    input:
        rules.setup.output,
    output:
        f"{log_extract}{sheets[3]}{log_ext}"
    shell:
        f"python src/extract_sheet.py -f {rules.all.input[0]} -s {sheets[3]}"

rule preprocess_income:
    input:
        rules.extract_income.output,
    output:
        f"{log_ppreprocess}{sheets[3]}{log_ext}"
    shell:
        f"python src/preprocess_sheet.py -s {sheets[3]}"

# extract & preprocess RESEARCH INCOME IN KIND
# --------------------------------------------
rule extract_income_in_kind:
    input:
        rules.setup.output,
    output:
        f"{log_extract}{sheets[4]}{log_ext}"
    shell:
        f"python src/extract_sheet.py -f {rules.all.input[0]} -s {sheets[4]}"

rule preprocess_income_in_kind:
    input:
        rules.extract_income_in_kind.output,
    output:
        f"{log_ppreprocess}{sheets[4]}{log_ext}"
    shell:
        f"python src/preprocess_sheet.py -s {sheets[4]}"

# extract & preprocess RESEARCH GROUPS
# ------------------------------------
rule extract_groups:
    input:
        rules.setup.output,
    output:
        f"{log_extract}{sheets[5]}{log_ext}"
    shell:
        f"python src/extract_sheet.py -f {rules.all.input[0]} -s {sheets[5]}"

rule preprocess_groups:
    input:
        rules.extract_groups.output,
    output:
        f"{log_ppreprocess}{sheets[5]}{log_ext}"
    shell:
        f"python src/preprocess_sheet.py -s {sheets[5]}"