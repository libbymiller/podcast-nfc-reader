'''
This is the only interface with the NFC reader, as it can only be accessed by one process at a time
It: 
 * reads data.json for exsting mappings between uids and feedUrls 
  - if it finds a match with the current uid
  - it sends a command to the server to tell it that the card for a feedUrl is present
 * it also saves its state continuously for other apps to read.

It assumes client-huffduffer is present (i.e. the server it sends information to)

It triggers the POST to the server as long as the card ahs changed or been removed 
since it was seen last.

'''
import nxppy
import sys
import requests
import os
import json
from pprint import pprint

# this script's directory
dn = os.path.dirname(os.path.realpath(__file__))

# data file mapping uids and RSS feed urls. Read-only from this python script
print "opening nfc config file "+dn+"/data.json"
json_data=open(dn+"/data.json")

data = json.load(json_data)
print data
json_data.close()

reader = nxppy.Mifare()
print "Loaded mifare device"
currentId = None

# loop forever
while True:
  try:
    # read the card uid
    uid = reader.select()

    # we don't want to read it if we've just seen it
    if(uid is not None and currentId!=uid):
      currentId = uid
      url = None
      payload = None
      print "New card ID:" +currentId
      for d in data:
         id = d
         url = data[d]
         print "id is "+id+".."
         print "uid is "+uid+".."
         print "url is "+url+".."
         # we've already seen this uid, so we know it has a url
         # so we post it
         if(uid==id):
            print "ok"
            payload = {'feedUrl': url}
            print "posting "+url
            r = requests.post("http://localhost:5000/rssFromNFC", data=payload)
            print r
            break
         else:
            print "uuid != url"
            url = ""

  except:
    # we always get an exception if the card reader isn't reading anything
    # so we just pass it through
    uid = ""
    url = ""
    currentId = None
    pass

  finally:
    # write our uid to a file, whatever it is
    # so that other apps can use it, including if not present
    state = {"uid":uid, "feedUrl": url}
    out_file = open(dn+"/uid.json","w")
    json.dump(state,out_file, indent=4) 
    out_file.close()

