# Hubstaff report

This project contains a Python script that processes hubstaff api data and generate a report for a specific date (yesterday by default).

## Requirements

* Python >=3.11

## Installation

Follow these steps to set up the project locally:


1.  **Create a virtual environment:**

    It's highly recommended to use a virtual environment to manage dependencies.

    ```bash
    python3 -m venv hubstaff_client
    ```

2.  **Activate the virtual environment:**

    * **On Windows:**

        ```bash
        .\hubstaff_client\Scripts\activate
        ```

    * **On macOS/Linux:**

        ```bash
        source hubstaff_client/bin/activate
        ```

3.  **Install dependencies:**

    Once your virtual environment is active, install the required packages.

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the script

To run the script, activate your virtual environment (if not already active) and then execute the main Python file.

```bash
python index.py
```

### Command line options

* Optional ```--report_date=YYYY-MM-DD```

## Known issues

* pagination doesn't tell you how many records or pages it has and docs doesn't give eny hints about what would happen at the end so i just use my best guess the there won't be next page pointers there
* day end is calculated by UTC so it need to be run before that time zone switch to next day otherwise request would be for current day on the server with UTC time zone it should work fine. 
* as i don't know nothing about eviremont it is hard to configure login or write a script acorningly so i've made only basic for further improvement if that would even be necesary as mentioned wraper might handle all the stderr output properly

## Used Guidlines

* https://github.com/reef-technologies/handbook/blob/master/docs/maturity_levels.md
* https://github.com/reef-technologies/handbook/blob/master/docs/release-process.md