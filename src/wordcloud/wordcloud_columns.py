"""
Generate wordcloud from Pandas columns

By default generates for all columns

Use -e, --exclude with a comma separated list to
exclude columns.

Requirements: wordcloud pandas
Install: pip install -r requirements.txt

Usage:

python wordcloud_columns.py <file> [--exclude=COLUMNS]
"""

import argparse
from pathlib import Path

import wordcloud
import pandas as pd

# Additional stopwords
STOPWORDS = {"research", "University", "School", "Centre", "UK", "Institute"}

# Set global wordcloud settings here
# https://amueller.github.io/word_cloud/generated/wordcloud.WordCloud.html#wordcloud.WordCloud
W = wordcloud.WordCloud(stopwords=set(wordcloud.STOPWORDS) | STOPWORDS)


def generate_column(df, column: str):
    assert column in df.columns, f"Column {column} not found in dataframe"
    return W.generate(" ".join(df[column]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate wordcloud for data columns")
    parser.add_argument("file", help="Filename to parse")
    parser.add_argument("-e", "--exclude", help="Exclude columns")
    args = parser.parse_args()

    df = pd.read_csv(args.file)
    columns = df.columns
    excluded_columns = []
    if args.exclude:
        excluded_columns = args.exclude.split(",")
    columns = [c for c in columns if c not in excluded_columns]
    for c in columns:
        output_filename = Path(args.file).stem + "_" + c.replace(" ", "-").replace(",", "") + ".jpg"
        generate_column(df, c).to_file(output_filename)
        print(output_filename)
