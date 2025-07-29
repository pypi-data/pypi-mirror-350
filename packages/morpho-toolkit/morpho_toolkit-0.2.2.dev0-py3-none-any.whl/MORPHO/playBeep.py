import os
import platform

def play_beep():
    # Get the current operating system
    current_os = platform.system().lower()

    if current_os == "linux": # Linux
        os.system("beep")
    
    elif current_os == "darwin": # macOS
        os.system("osascript -e 'beep'")

    else:
        print(f"Unsupported OS: {current_os}")

if __name__ == "__main__":
    play_beep()
    print("Beep sound played successfully.")