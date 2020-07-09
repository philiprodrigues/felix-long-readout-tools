#!/usr/bin/env python

import argparse
import json
import re
import sys
import os.path
from pprint import pprint

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="""
    Create metadata in json format for long-readout dump files in a directory.
    The metadata created can be provided to FTS for cataloguing in samweb
    """)
    parser.add_argument("infiles", metavar="file", nargs="+", type=str)
    parser.add_argument("--outdir", type=str, required=True)
    parser.add_argument("--run", type=int, required=True)
    parser.add_argument("--apa", type=int, required=True)

    re_str=r"felix-([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9][0-9][0-9]).([0-9])\.([0-9])\.([0-9])\.bin"
    fname_re=re.compile(re_str)

    args=parser.parse_args()

    # key is link id, value is list of files with that link id
    link_files={}

    # First we get all the files and gather them by link ID. Within a
    # link, we have to sort the items by time to find the fake event
    # number
    for filename in args.infiles:
        base=os.path.basename(filename)
        m=fname_re.search(base)
        if not m:
            print("Couldn't parse filename {}. Expecting it to match regex '{}'".format(f, re_str))
            sys.exit(1)
        datetime=m.group(1)
        link=(m.group(2), m.group(3), m.group(4))
        link_files.setdefault(link, []).append(base)

    for link,files in link_files.iteritems():
        sorted_files=sorted(files)
        for i,f in enumerate(sorted_files):
            event=i+1
            metadata={
                "file_name": f,
                "data_stream": "Test",
                "data_tier": "raw",
                "file_format": "binary",
                "dune_data.daqconfigname": "N/A",
                "dune_data.detector_config": '{"FELIX":["APA%d.%d"]}' % (args.apa, int(link[1])),
                "dune_data.comment": "Long-readout test run for DAQ studies. Contact dune-fd-daq-cnsrt@listserv.fnal.gov",
                "event_count": 1,
                "events": [event],
                "file_type": "detector",
                "first_event": event,
                "last_event": event,
                "runs": [[args.run,1,"protodune-sp"]]
            }

            outfilename=os.path.join(args.outdir, f)+".json"
            outfile=open(outfilename, "w")
            outfile.write(json.dumps(metadata))
            
