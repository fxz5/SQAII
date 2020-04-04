# Android Test Suite

Maintained by Luis Correa
luiscorrea9614@gmail.com

## Run Instructions
1. Create a new venv environment using Python 2.7.x and venv
2. Install project dependencies using
```console
pip install -r requirements.txt
```  
3. Run main file
```console
python main.py
```

## Project Structure
* models: project classes that will instantiate complex object and handle object logic.
* suites: all the testing suites for the project, each module will be contained in a python file that follows the structure {module}_suite.py
* utils: common routines repeated across multiple testing suites in the project, for easy instantiation and use.
* main.py: main program, docs for flags to run will be detailed in further sections.

## External Files
* Test Plan: file describing test plan.
* Release Notes: summary for the testing activities and reporting of such.


## Framework Reporting
@TODO