# felix-long-readout-tools
Tools for dealing with ProtoDUNE long-readout binary dumps. Currently very hacky. Contributed improvements welcome.

Build with the usual `cmake` steps:

```bash
mkdir build
cd build
cmake /path/to/src
make
# make install step doesn't exist yet
```

`dumpfile-to-text` will convert a binary dump into a text format. `dumpfile-to-text --help` for help; output format is described in the source code.

`check-timestamps /path/to/binary/file.bin` will check that all of the frame timestamps in `file.bin` are contiguous (ie, that they are separated by 25 ticks).

## Input file format

The binary dump files that we use each contain an array of raw WIB frames.  The frame format is described in detail in DUNE docdb 1701, and the `dune::FelixFrame` class in `FelixFormat.hh` provides access to WIB frames.

Each file contains frames from one link, consisting of 256 channels, for 1GB of file size (about 1 second's worth of data). The file format is `felix-YYYY-MM-DD-HHMMSS.x.y.z.bin` where `x.y.z` is a link identifier, and `YYYY-MM-DD-HHMMSS` is the time the file was written to disk (not necessarily the time of the data contained therein): the date/time allows for ordering the files.
