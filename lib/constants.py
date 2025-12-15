import os

PROJECT_DIR = os.getcwd()[: (os.getcwd().rfind("/src"))]
print(PROJECT_DIR)