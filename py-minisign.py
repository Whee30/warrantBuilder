import minisign
import tempfile
import requests
import shutil

prefix = "https://forrestcook.net/v208/"

dest = "sources/"

targets = [
    'skeleton.docx',
    'remote_refs.json',
    'cv_sources.json'
]

public_key = minisign.PublicKey.from_base64("RWSXSB6hvpsA4mlr9wBmopJObFXttfcyvJN6micbhwtMH96qPOyZ84u4")

with tempfile.TemporaryDirectory() as tempdir:
    for t in targets:
        temp_path = f"{tempdir}/{t}"
        temp_sig = f"{temp_path}.minisig"

        r = requests.get(f"{prefix}{t}")
        r.raise_for_status()
        with open(temp_path, 'wb') as f:
            f.write(r.content)

        r = requests.get(f"{prefix}{t}.minisig")
        r.raise_for_status()
        with open(temp_sig, 'wb') as f:
            f.write(r.content)

        try:
            public_key.verify_file(temp_path)
            print(f"{t} signature verified.")
            shutil.move(temp_path, f"{dest}{t}")
        except Exception as err:
            print(f"Verification for {t} failed: {err}")
