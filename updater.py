import hashlib
import json
import time
import requests


no_cache_headers = {
    'Cache-Control': 'no-cache'
}

remote_hash_list = f"https://raw.githubusercontent.com/Whee30/warrantBuilder/refs/heads/main/sources/hash_list.json?nocache={int(time.time())}"
remote_version_list = 

response = requests.get(remote_hash_list, headers=no_cache_headers)
hash_references = response.json()



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


def compare_hashes(k):
    hash_to_compare = hash_references[k]
    remote_sha256_hash = hashlib.sha256()
    response = requests.get(remote_files[k], headers=no_cache_headers)
    remote_sha256_hash.update(response.content)
    if remote_sha256_hash.hexdigest() == hash_to_compare:
        replace_file(k)
    elif remote_sha256_hash.hexdigest() != hash_to_compare:
        print("The hashes don't match!")
        print(f"{k} calculated: {remote_sha256_hash.hexdigest()}")
        print(f"{k} Stored:     {hash_to_compare}")

def replace_file(new_file):
    print(f"{local_files[new_file]} would be replaced")
    file_response = requests.get(remote_files[new_file], headers=no_cache_headers)
    with open(local_files[new_file], 'wb') as file:
        file.write(file_response.content)
    # update the version number now
    local_version_data[file] = remote_data[target]
    with open('local_version.json', 'w') as file:
        json.dump(local_version_data, file, indent=4)
    print(f"{file} was updated.")

