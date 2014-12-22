This is the only interface with the NFC reader, as it can only be accessed by one process at a time
It:
 * reads data.json for exsting mappings between uids and feedUrls
  - if it finds a match with the current uid
  - it sends a command to the server to tell it that the card for a feedUrl is present
 * it also saves its state continuously for other apps to read.

It assumes radiodan-client-podcast is present (i.e. the server it sends information to)

It triggers the POST to the server as long as the card ahs changed or been removed
since it was seen last.

Installation 

- requires nxppy - see https://github.com/svvitale/nxppy for installation of that.
