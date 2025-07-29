# MORPHO/modeSelect.py

from enum import Enum, auto
from loadingBar import LoadingBar
from colorama import Fore, Style, init
import logging
import json
import os

logging.basicConfig(filename = 'app.log',
                    filemode = 'w',
                    format = '%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO, 
                    datefmt='%Y-%m-%d %H:%M:%S')

init(autoreset=True)

CONFIG_DIR = "config"
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)
    logging.info(f"Created directory: {CONFIG_DIR}")
else:
    logging.info(f"Directory already exists: {CONFIG_DIR}")

MODE_FILE = os.path.join(CONFIG_DIR, "modeSelection.json")

""" ENUMS """

class Mode(Enum):
    TEST_MODE = auto()
    USER_MODE = auto()
    MAINTENANCE_MODE = auto()
    
class Operation(Enum):
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULUS = auto()
    EXPONENT = auto()
    FLOOR_DIVIDE = auto()
    BITWISE_AND = auto()
    BITWISE_OR = auto()
    BITWISE_XOR = auto()
    BITWISE_NOT = auto()
    BITWISE_LEFT_SHIFT = auto()
    BITWISE_RIGHT_SHIFT = auto()
    LOGICAL_AND = auto()
    LOGICAL_OR = auto()
    LOGICAL_NOT = auto()
    CONCAT = auto()
    
""" FUNCTIONS """

def convertInput(inputVal):
    """
    Converts input to most appropriate data type
    """
    if inputVal.isdigit(): #check if its a number (int)
        return int(inputVal)
    try:
        return float(inputVal) #convert to float
    except ValueError:
        return inputVal #return as string

def getUserVals():
    """
    Prompts for own values
    """
    print("Enter your values.\n")
    try:
        values = {}
        continueAdding = True
        valCount = 1
        
        while continueAdding:
            val1 = input(f"Enter value for val{valCount}: ")
            val1 = convertInput(val1)
            values[f'val{valCount}'] = val1
            print(f"Value of val{valCount}: {val1}\nData type: {type(val1)}")
            valCount += 1
        
            val2 = input(f"Enter value for val{valCount}: ")
            val2 = convertInput(val2)
            values[f'val{valCount}'] = val2
            print(f"Value of val{valCount}: {val2}\nData type: {type(val2)}")
            valCount += 1
            
            continueAdding = input("Do you want to add more values (y/n): ").strip().lower()
            if continueAdding != 'y':
                continueAdding = False 
        return values
    except Exception as e:
        print("ERROR whilst getting values: {e}")
        return{}
    
def getModeSelection():
    """
    Returns:
        Mode: either Mode.TEST_MODE, Mode.USER_MODE or Mode.MAINTENANCE_MODE
    """
    while True:
          print(f"Select mode:\n")
          print("1. TEST MODE (Preset values)\n")
          print("2. USER MODE (User values)\n")
          print("3. MAINTENANCE MODE")
          print("Enter '1' for TEST MODE or '2' for USER MODE.\n")
          choice = input("Enter choice: ").strip().lower()
          
          if choice == '1':
              return Mode.TEST_MODE
          elif choice == '2':
              return Mode.USER_MODE
          elif choice == '3':
              logging.info("MAINTENANCE MODE selected.\n")
              return Mode.MAINTENANCE_MODE
          else:
            logging.warning("Invalid choice input: %s", choice)
            print("Invalid choice. Please enter 1, 2, or 3.")

def saveModeSelection(mode: Mode):
    """
    Saves the selected mode to a JSON file in the config folder, and logs the action.

    Args:
        mode (Mode): The selected mode (either TEST_MODE or USER_MODE).
    """
    os.makedirs(CONFIG_DIR, exist_ok=True) 
    logging.info(f"Directory created: {CONFIG_DIR}\n")
    modeData = {'mode': mode.name}
    with open(MODE_FILE, "w") as f:
        json.dump(modeData, f)
    logging.info(f"Mode selection saved as {mode.name}\n")
    
def loadModeSelection():
    try:
        with open(MODE_FILE, "r") as f:
            modeData = json.load(f)
            mode = Mode[modeData['mode']]
            logging.info(f"Loaded saved mode: {mode.name}\n")
            return mode
    except FileNotFoundError:
        logging.warning("No saved mode selection found!\n")
        return None

def runTest(testName, val1, val2, operation: Operation, duration=5):
    """
    Runs a test operation (addition, multiplication, etc.) with a loading bar.

    Args:
        test_name (str): Name of the test operation.
        val1 (int, str, etc.): First value for the test.
        val2 (int, str, etc.): Second value for the test.
        operation (str): Type of operation ('add', 'multiply', 'concat', etc.).
        duration (int): Duration for the loading bar.
    """
    print(f"Running test: {testName} with values {val1} and {val2}.\n")
    loadingBar = LoadingBar(duration)
    loadingBar.display()

    result = None
    if operation == Operation.ADD:
        result = val1 + val2
    elif operation == Operation.MULTIPLY:
        result = val1 * val2
    elif operation == Operation.SUBTRACT:
        result = val1 - val2
    elif operation == Operation.DIVIDE:
        if val2 == 0:
            raise ValueError("Cannot divide by zero.")
        result = val1 / val2
    elif operation == Operation.MODULUS:
        result = val1 % val2
    elif operation == Operation.EXPONENT:
        result = val1 ** val2
    elif operation == Operation.FLOOR_DIVIDE:
        result = val1 // val2
    elif operation == Operation.BITWISE_AND:
        result = val1 & val2
    elif operation == Operation.BITWISE_OR:
        result = val1 | val2
    elif operation == Operation.BITWISE_XOR:
        result = val1 ^ val2
    elif operation == Operation.BITWISE_NOT:
        result = ~val1
    elif operation == Operation.BITWISE_LEFT_SHIFT:
        result = val1 << val2
    elif operation == Operation.BITWISE_RIGHT_SHIFT:
        result = val1 >> val2
    elif operation == Operation.LOGICAL_AND:
        result = val1 and val2
    elif operation == Operation.LOGICAL_OR:
        result = val1 or val2
    elif operation == Operation.LOGICAL_NOT:
        result = not val1
    elif operation == Operation.CONCAT:
        result = str(val1) + str(val2)
    else:
        raise ValueError(f"Unsupported operation: {operation}")
    print(f"Test {testName} completed.\n")
    return result

def runTestMode():
    print("Running in TEST MODE with preset values.\n")
    testVals = {
        'val1': 1,
        'val2': 2.5,
        'val3': "test"
    }
    for key, value in testVals.items():
        print(f"{key}: {value}\nData type: {type(value)}")

    print("=== Performing Test Operations ===\n")
    loadingDuration = 1 #loading bar duration (in seconds)

    operations = list(Operation)
    
    while True:
        testOpt = input(
            "Choose test mode:\n"
            "1. Full list\n"
            "2. Half list\n"
            "3. Custom\n"
            "To see full operation list, press 'e': "
        ).strip().lower()

        if testOpt == 'e':
            print("\n============== Available Operations ==============")
            for operation in operations:
                print(f"- {operation.name}")
            print("==================================================\n")
            continue  # go back to asking for a valid option
        break  # exit loop if it's not 'e'

    if testOpt == '1':
        selectedOps = operations
    elif testOpt == '2':
        selectedOps = operations[:len(operations) // 2]
    elif testOpt == '3':
        customOperations = input("Enter custom operations (comma-separated): ").strip().split(',')
        selectedOps = []
        for operation in customOperations:
            operation = operation.strip().upper()
            if hasattr(Operation, operation):
                selectedOps.append(Operation[operation])
            else:
                print(f"Invalid operation: {operation}\n")
    else:
        logging.info(f"ERROR - Invalid test mode selection: {testOpt}\n")
        print("Invalid test mode selection.\n")
        return

    for operation in selectedOps:
        try:
            result = runTest(operation.name, testVals['val1'], testVals['val2'], operation, loadingDuration)
            print(f"Result of {operation.name}: {result}\n")
        except Exception as e:
            logging.error(f"ERROR - during operation {operation.name}: {e}\n")
            print(f"Error during operation {operation.name}: {e}\n")

def handleModeSelection(mode: Mode):
    if mode == Mode.TEST_MODE:
        print("Running in TEST MODE with preset values.\n")
        runTestMode()
    elif mode == Mode.USER_MODE:
        print("Running in USER MODE with user-defined values.\n")
        userVals = getUserVals()
        print(f"User values: {userVals}\n")
    elif mode == Mode.MAINTENANCE_MODE:
        print("Running in MAINTENANCE MODE.")
    else:
        print(Fore.RED + "Invalid mode selected.\n")
        logging.error("Invalid mode selected.\n")

def modeSelect():
    logging.info("Program started.\n")
    savedMode = loadModeSelection()  #load saved mode selection, if poss
    
    if savedMode:
        userSelect = input(f"Saved mode detected. Would you like to use the saved mode ({savedMode.name})? (y/n): ").strip().lower()
        if userSelect == 'y':
            mode = savedMode
            logging.info(f"Using saved mode: {mode.name}\n")
        else:
            mode = getModeSelection()
            logging.info(f"Using new mode: {mode.name}\n") 
    else:
        mode = getModeSelection() 
        logging.info(f"Using mode (no prior): {mode.name}\n")
    
    handleModeSelection(mode) 
    saveModeSelection(mode)  

if __name__ == "__main__":
    modeSelect()
