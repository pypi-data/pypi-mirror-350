import os

def createConfigFolder():
    """
    Creates a configuration folder for the project if it doesn't already exist.
    """
    configFolder = 'config'
    if not os.path.exists(configFolder):
        os.makedirs(configFolder)
        print(f"Created directory: {configFolder}")
    else:
        print(f"Directory already exists: {configFolder}")

    gitignoreFile = '.gitignore'
    
    # Check if .gitignore exists, create it if it doesn't
    if not os.path.exists(gitignoreFile):
        with open(gitignoreFile, 'w') as f:
            print(f"Created the .gitignore file.")
    
    # Add /config/ to .gitignore if it's not already there
    with open(gitignoreFile, 'a') as f:
        # Check if config is already in .gitignore
        with open(gitignoreFile, 'r') as check_f:
            lines = check_f.readlines()
            if '/config/' not in [line.strip() for line in lines]:
                f.write('\n/config/\n')
                print("Added '/config/' to .gitignore.")
            else:
                print("'/config/' is already in .gitignore.")

if __name__ == "__main__": 
    createConfigFolder()
    print("Configuration complete.")