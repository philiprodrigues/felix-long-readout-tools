#!/usr/bin/env python
import argparse
import json
import re
import sys
import struct
import os.path
from os import symlink
from pprint import pprint

def read_file_info(filename):
    if os.path.getsize(filename)==0:
        return None

    f=open(filename)
    b0,b1,b2,b3,ts0,ts1=struct.unpack("BBBBxxxxII", f.read(16))
    assert b0==0
    assert b3==0

    crate=b2 & 0x1f
    slot=(b2>>5) & 0x7

    version=b1 & 0x1f
    assert version==1
    fiber=(b1>>5) & 0x7

    ts=(ts1<<32) | ts0

    return crate,slot,fiber,ts

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="""
    Create metadata in json format for long-readout dump files in a directory.
    The metadata created can be provided to FTS for cataloguing in samweb
    """)
    parser.add_argument("infiles", metavar="file", nargs="+", type=str)
    parser.add_argument("--outdir", type=str, required=True)
    parser.add_argument("--run", type=int, required=True)

    re_str=r"felix-([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9]:?[0-9][0-9]:?[0-9][0-9]).([0-9])\.([0-9]){1,2}\.([0-9])\.bin"
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
            print("Couldn't parse filename {}. Expecting it to match regex '{}'".format(base, re_str))
            sys.exit(1)
        file_info=read_file_info(filename)
        if file_info is not None:
            crate,slot,fiber,ts=file_info
            link_files.setdefault((crate,slot,fiber), []).append((ts, filename))

    for link,files in link_files.iteritems():
        sorted_files=sorted(files)
        # pprint(link)
        # pprint(sorted_files)
        for i,(ts,f) in enumerate(sorted_files):
            apa=link[0]
            base=os.path.basename(filename)
            event=i+1
            linkid=5*(link[2]-1)+link[1]

            new_base_name="np04_raw_run{}_apa{}_link{}_evt{:04d}.bin".format(args.run, apa, linkid, event)
            new_path=os.path.join(args.outdir, new_base_name)
            symlink(f, new_path)

            metadata={
                "file_name": new_base_name,
                "data_stream": "Test",
                "data_tier": "raw",
                "file_format": "binary",
                "dune_data.daqconfigname": "N/A",
                "dune_data.detector_config": '{"FELIX":["APA%d.%d"]}' % (apa, linkid),
                "dune_data.comment": "Long-readout test run for DAQ studies. Contact dune-fd-daq-cnsrt@listserv.fnal.gov",
                "event_count": 1,
                "events": [event],
                "file_type": "detector",
                "first_event": event,
                "last_event": event,
                "runs": [[args.run,1,"protodune-sp"]]
            }

            metadata_name=new_path+".json"
            metadata_file=open(metadata_name, "w")
            metadata_file.write(json.dumps(metadata))
            
