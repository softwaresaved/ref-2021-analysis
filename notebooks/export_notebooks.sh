rm -rd preprocess.md
rm -rf preprocess_files
jupyter nbconvert --to markdown --no-input PREPROCESS_data.ipynb --output preprocess.md 