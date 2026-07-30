import json
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "documents.json")

def run_crawler():
    """
    Simulates a web crawler by ensuring the data directory exists
    and verifying the documents.json file.
    """
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data file not found at {DATA_PATH}.")
    
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"Crawler verified {len(data)} documents in {DATA_PATH}.")
    return data

if __name__ == "__main__":
    run_crawler()