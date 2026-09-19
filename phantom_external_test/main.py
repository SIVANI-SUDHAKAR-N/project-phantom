import os
import json

def main():
    print(json.dumps(os.listdir('.')))
