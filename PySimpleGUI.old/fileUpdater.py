import urllib.request

# This should likely be kept as a separate function as opposed to an integrated solution
# The delay inherent to the operation will likely cause the user multiple launches. Need to explore a timer or progress bar.
# This thing functions but it is taking for.ev.er. why?

source_file_list = (
   'cellphone.txt',
   'computer.txt',
   'fraud.txt',
   'narcotics.txt',
   'social.txt',
   'acquire.txt'
)

localFile = open('./sources/version.txt')
localVersion = float(localFile.read(3))

print(localVersion)

url = "https://raw.githubusercontent.com/Whee30/warrantBuilder/refs/heads/main/sources/version.txt"

data = urllib.request.urlopen(url, None, timeout=5).read(3)

remoteVersion = float(data)

print(remoteVersion)

# this function checks the local version.txt against the remote version.txt and updates all source files
# if the remote version number is larger than the local version number. This also updates the local version number.
if remoteVersion > localVersion:
   f = open('./sources/version.txt', 'w')
   f.write(str(remoteVersion))
   f.close()
   for each_item in source_file_list:
      remote_url = 'https://raw.githubusercontent.com/Whee30/warrantBuilder/refs/heads/main/sources/' + each_item
      remote_source = urllib.request.urlopen(remote_url).read()
      local_update = open(f'./sources/{each_item}', 'w')
      local_update.write(str(remote_source, "utf-8"))
      local_update.close()
elif remoteVersion == localVersion:
   print("The versions are equal")
else:
   print("something went wrong in the update process!")
exit