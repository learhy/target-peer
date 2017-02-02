Script to produce a report on target peers. Script requires two files:
source_nets.json and dest_nets.json to be located in the same directory.
These files are generated from a like query in Kentik's UI.

```
usage: target-peer.py [-h] filename email api {source,dest}

Script to produce a report on target peers. Script requires two files:
source_nets.json and dest_nets.json to be located in the same directory.
These files are generated from a like query in Kentik's UI.

positional arguments:
  filename       Filename to write output to. Must be of type .csv or .json.
                 Defaults to report.csv
  email          Admin user email
  api            API key for configured user
  {source,dest}  Select inbound report or outbound peering report

optional arguments:
  -h, --help     show this help message and exit
```
