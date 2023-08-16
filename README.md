# Analysis of REF 2021 submissions

Data source: https://results2021.ref.ac.uk/ (accessed 2023-08-10)

Preliminary study: [notebook](notebooks/STUDY_data.ipynb), [md](notebooks/study.md)

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