import sys
from termcolor import colored

print("engine: START")
print("trying to open file: ",  sys.argv[1:])
try:
        for l in open(sys.argv[1]):
            #parse the actual script file here
            continue
except FileNotFoundError:
        print(colored("engine: STOP\n\nCause: Failed to open file. This is a critical error.", "red"))