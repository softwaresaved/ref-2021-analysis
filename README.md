# Processing of REF 2021 submissions

Team members can access [the running notes for meetings](https://docs.google.com/document/d/1HBTiIFS5aqfwd8OonJDXF0MirpWMyczKEfb1jbSvY4c/edit), which provide details of the project goals and decisions.

## Data source

Data source: https://results2021.ref.ac.uk/ (accessed 2023-08-10)

Information on submission system data requirements: https://ref.ac.uk/guidance-and-criteria-on-submissions/guidance/submission-system-data-requirements/ (accesed 2023-08-30). 

Local copy of the download page: [Submission_system_data_requirements-REF2021.pdf](info/Submission_system_data_requirements-REF2021.pdf) (accessed 2023-08-10)


## Data explorer

Streamlit data explorer hosted on Azure is available at [https://ref2021explorer.azurewebsites.net/Research_Groups].

## Setting up the environment

Follow these steps to set up the environment for this project:

1. Install Python 3.x on your system if it is not already installed.

2. Clone this project from GitHub.

3. Navigate to the project root directory in your terminal or command prompt.

4. Create a new virtual environment with 
    ```bash
    python3 -m venv venv
    ```

    This will create a new virtual environment named `venv` in the current directory.

5. Activate the virtual environment with:

    On Windows

    ```
    venv\Scripts\activate.bat
    ```

    On Unix/Linux/MacOS:

    ```
    source venv/bin/activate
    ```

    This will activate the virtual environment and change your prompt to indicate that you are now working inside the virtual environment.

6. Install the project dependencies with:

    ```bash
    pip install -r requirements.txt
    ```

    This will install all of the required packages and their versions listed in the `requirements.txt` file.

## Processing of environment statements

The raw PDF format [environment statements](data/raw/environment_statements) have been processed with [pdftotext(1)](https://manpages.debian.org/bookworm/poppler-utils/pdftotext.1.en.html) tool from poppler-utils

Package used to convert to text is
[poppler-utils 22.12.0](https://packages.debian.org/bookworm/poppler-utils).

The conversion was done on a Debian bookworm system on a x86_64 architecture.

The script is not dockerised but can be done based on the `debian:bookworm-slim` image if required.

To convert the PDFs to *.txt files run this script in the folder containing the PDFs

```shell
#!/bin/sh

for i in *.pdf; do
  pdftotext -layout "$i"
done
```

Then the `*.txt` files are then copied into [data/processed/environment_statements](data/processed/environment_statements) folder.
