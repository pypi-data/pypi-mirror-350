import sys
import time

class LoadingBar:
    def __init__(self, duration, length=40):
        self.duration = duration
        self.length = length

    def display(self):
        """
        Displays a loading bar that fills up over the specified duration.
        """
        bar = '[' + ' ' * self.length + ']'
        sys.stdout.write(bar)  #initial empty bar
        sys.stdout.flush()

        for i in range(self.length):
            time.sleep(self.duration / self.length)
            bar = '[' + '=' * (i + 1) + ' ' * (self.length - i - 1) + ']'
            sys.stdout.write('\r' + bar)  
            sys.stdout.flush()

        print("\nLoading complete!\n") 

if __name__ == "__main__":
    defaultDuration = 5.0  # Default duration in seconds
    defaultLength = 40    # Default length
    
    durationInput = input("Enter the duration for the loading bar (in seconds): ")
    lengthInput = input("Enter the length of the loading bar: ")
    
    duration = float(durationInput) if durationInput else defaultDuration
    length = int(lengthInput) if lengthInput else defaultLength
    
    loading_bar = LoadingBar(duration, length)
    loading_bar.display()