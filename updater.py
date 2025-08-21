import hashlib
import json
import time
import requests


no_cache_headers = {
    'Cache-Control': 'no-cache'
}

remote_hash_list = f"https://raw.githubusercontent.com/Whee30/warrantBuilder/refs/heads/main/sources/hash_list.json?nocache={int(time.time())}"
remote_version_list =f"https://raw.githubusercontent.com/Whee30/warrantBuilder/refs/heads/main/sources/remote_version.json?nocache={int(time.time())}"
local_version_list = "./sources/local_version.json"

h_response = requests.get(remote_hash_list, headers=no_cache_headers)
hash_references = h_response.json()

v_response = requests.get(remote_version_list, headers=no_cache_headers)
remote_versions = v_response.json()

# Load local version numbers
with open(local_version_list, 'r') as file:
    local_versions = json.load(file)

# The files needing hash validation
remote_files = {
    "program": "https://raw.githubusercontent.com/Whee30/warrantBuilder/refs/heads/main/warrantBuilder.py",
    "verbiage": "https://raw.githubusercontent.com/Whee30/warrantBuilder/refs/heads/main/sources/cv_sources.json",
    "template": "https://github.com/Whee30/warrantBuilder/raw/refs/heads/main/sources/skeleton.docx"
}

local_files = {
    "program":"./dist/warrantBuilder.exe",
    "verbiage":"./sources/cv_sources.json",
    "template":"./sources/skeleton.docx"
}

def compare_version(k):
    if local_versions[k] >= remote_versions[k]:
        print("The versions are equal or the local version is newer")
    elif local_versions[k] < remote_versions[k]:
        print("The remote version is newer")
        compare_hashes(k)
    #print(f"Local: {local_versions[k]} - Remote: {remote_versions[k]}")

def compare_hashes(k):
    hash_to_compare = hash_references[k]
    remote_sha256_hash = hashlib.sha256()
    response = requests.get(remote_files[k], headers=no_cache_headers)
    remote_sha256_hash.update(response.content)
    if remote_sha256_hash.hexdigest() == hash_to_compare:
        #replace_file(k)
        print(f"The hash for {k} matches, it would be replaced")
    elif remote_sha256_hash.hexdigest() != hash_to_compare:
        print("The hashes don't match!")
        print(f"{k} calculated: {remote_sha256_hash.hexdigest()}")
        print(f"{k} Stored:     {hash_to_compare}")

def replace_file(k):
    file_response = requests.get(remote_files[k], headers=no_cache_headers)
    with open(local_files[k], 'wb') as file:
        file.write(file_response.content)
    # update the version number now
    local_versions[k] = remote_versions[k]
    with open(local_version_list, 'w') as file:
        json.dump(local_versions, file, indent=4)
    print(f"{file} was updated.")

for k,v in local_files.items():
    compare_version(k)