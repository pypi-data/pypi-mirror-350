import uuid
import time
import random
import string
import os

COUNTER_FILE = "counter.txt"

def _loadCounter():
    try:
        with open(COUNTER_FILE, "r") as f:
            content = f.read().strip()
            return int(content) if content.isdigit() else 0
    except FileNotFoundError:
        return 0
    
def _saveCounter(counter):
    with open(COUNTER_FILE, "w") as f:
        f.write(str(counter))

def generateUUID():
    return str(uuid.uuid4())

def timestampID():
    return str(int(time.time()))

def randomID():
    timestamp = str(int(time.time()))
    randomChars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"ID-{timestamp}-{randomChars}"

def customID(prefix="ID"):
    counter = _loadCounter()
    counter += 1
    _saveCounter(counter)
    timestamp = str(int(time.time()))
    return f"{prefix}-{counter:06d}"

def resetCounter(): #resets counter
    _saveCounter(0)

if __name__ == "__main__":
    print("Custom ID with prefix':", customID(prefix="SIN"))
    
    resetCounter()  # Reset the counter for demonstration
