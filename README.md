# Processing of REF 2021 submissions

Team members can access [https://docs.google.com/document/d/1HBTiIFS5aqfwd8OonJDXF0MirpWMyczKEfb1jbSvY4c/edit](the running notes for meetings), which provide details of the project goals and decisions.

## Data explorer

Data explorer available at [https://ref-2021-data-explorer.streamlit.app](https://ref-2021-data-explorer.streamlit.app) hosted on [Streamlit Sharing](https://streamlit.io/sharing).

Data source: https://results2021.ref.ac.uk/ (accessed 2023-08-10)

Information on submission system data requirements: https://ref.ac.uk/guidance-and-criteria-on-submissions/guidance/submission-system-data-requirements/ (accesed 2023-08-30). The local copy of the download page at the time of access: [Submission_system_data_requirements-REF2021.pdf](info/Submission_system_data_requirements-REF2021.pdf)

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
