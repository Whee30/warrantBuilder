import subprocess

pub_key = 'RWSXSB6hvpsA4mlr9wBmopJObFXttfcyvJN6micbhwtMH96qPOyZ84u4'

result = subprocess.run(
    ['./sources/minisign.exe', '-V', '-m', './sources/skeleton.docx', '-P', pub_key],
    capture_output=True,
    text=True,
    check=True)

print(result)