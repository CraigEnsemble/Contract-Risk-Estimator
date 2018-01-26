# CRE_Configuration: Configuration constants in one place for CRE modules

from datetime import datetime

# Error constants
LOGGER_NAME = "CRE_Logger"

# Filename constants
DEFAULT_OUTPUT_DIRECTORY = "/output"

DEFAULT_OUTPUT_FILENAME = "CRE." + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
PREPROCESS_OUTPUT_FILENAME = "CRE_PreProcess." + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
MODEL_OUTPUT_FILENAME = "CRE_Modeling." + datetime.now().strftime('%Y-%m-%d %H:%M:%S')

DEFAULT_PROJECT_DATA_FILE = "ProjectBudget July to Dec 2017 csv.csv"

DEFAULT_MODEL_EXTENSION = ".dataModel"
DEFAULT_DATA_FRAME_EXTENSION = ".dataFrame.csv"

# Risk calculation constants
STD_DEV_FILTER = 1
BIN_COUNT = 5
BIN_STEPSIZE_PERCENTAGE = 10
RISK_THRESHOLD_PERCENTAGE = .1