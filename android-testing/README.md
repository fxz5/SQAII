# Android Test Suite

Maintained by Luis Correa
luiscorrea9614@gmail.com

## Run Instructions
1. Clone the repo  
```bash
git clone https://github.com/PrettyBoyHelios/SQAII
cd SQAII/android-testing
```  
2. Create a new venv environment using Python 2.7.x and venv, and then proceed to activate the new virtual environment.  
```bash
pip install virtualenv
virtualenv --python=<path/to/installed/python2.7+/> <venv/>
source env/bin/activate
```  
3. Install project dependencies using  
```bash
pip install -r requirements.txt
```  
4. Run main file  
```bash
python main.py
```

## Project Structure
* data: holds the data for data-driven tests in json format.
* models: project classes that will instantiate complex object and handle object logic.
* suites: all the testing suites for the project, each module will be contained in a python file that follows the structure {module}_suite.py
* utils: common routines repeated across multiple testing suites in the project, for easy instantiation and use.
* main.py: main program, docs for flags to run will be detailed in further sections.

## External Files
* Test Plan: file describing test plan.
* Release Notes: summary for the testing activities and reporting of such.


## Framework Reporting
@TODO