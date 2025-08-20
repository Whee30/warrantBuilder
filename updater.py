import hashlib
import json
import requests


no_cache_headers = {
    'Cache-Control': 'no-cache'
}

remote_hash_list = "https://raw.githubusercontent.com/Whee30/warrantBuilder/refs/heads/main/sources/hash_list.json"

response = requests.get(remote_hash_list, headers=no_cache_headers)
hash_references = response.json()

# The files needing hash validation
remote_files = {
    "program": "https://raw.githubusercontent.com/Whee30/warrantBuilder/refs/heads/main/warrantBuilder.py",
    "verbiage": "https://raw.githubusercontent.com/Whee30/warrantBuilder/refs/heads/main/sources/cv_sources.json",
    "template": "https://github.com/Whee30/warrantBuilder/raw/refs/heads/main/sources/skeleton.docx"
}

for k, v in hash_references.items():
    hash_to_compare = hash_references[k]
    remote_sha256_hash = hashlib.sha256()
    response = requests.get(remote_files[k], headers=no_cache_headers)
    remote_sha256_hash.update(response.content)
    if remote_sha256_hash.hexdigest() == hash_to_compare:
        print("The hashes match")
    elif remote_sha256_hash.hexdigest() != hash_to_compare:
        print("The hashes don't match!")
        print(f"{k} calculated: {remote_sha256_hash.hexdigest()}")
        print(f"{k} Stored:     {hash_to_compare}")