import os

# List all files in the current directory
files = [f for f in os.listdir('.') if os.path.isfile(f)]

# Print the file names and their contents
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        print(f"Contents of {file}:\n{f.read()}\n")
