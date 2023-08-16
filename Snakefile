
rule setup:
    shell:
        "python src/setup.py"
rule extract_sheets:
    shell:
        "python src/extract_sheets.py"
rule preprocess_data:
    shell:
        "python src/preprocess_data.py"
