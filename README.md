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
