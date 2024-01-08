import os
import fire
import yaml
import subprocess

def main():
    fats = []

    path = os.getcwd() + "/FATs"
    files = os.listdir(path)

    print("FATs in '", path, "':")

    # Load all yaml-files in the FATs directory
    def readFile(file):
        with open(os.getcwd() + "/FATs/" + file, "r") as f:
            doc = yaml.safe_load(f)
        fatName = doc["fat"]["name"] # Extract specific information (name)
        return fatName, doc

    # Verify each yaml-file
    def validateFile(file):
        _, doc = readFile(file)  # Use only the returned doc, not fatName
        if "name" not in doc["fat"] or doc["fat"]["name"] == None: # Check that yaml-file has name
            print("FAT name undefined in", file)
            validity = False
        else:
            validity = True
        return validity

    # Create a list of dictionaries with "fat" and "status" keys
    for file in files:
        if file.endswith(".yaml"):
            validity = validateFile(file)
            if validity:
                fatName, _ = readFile(file)
                fats.append({"fat": fatName, "status": "Pending"})
            else:
                print(file + " was not validated")

    print(fats)

if __name__ == "__main__":
    fire.Fire(main)
