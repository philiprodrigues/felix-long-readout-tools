#include "FelixFormat.hh"
#include "FrameFile.h"

#include <iostream>
#include <cstdio>
#include <inttypes.h>

int main(int argc, char** argv)
{
    for(int iarg=1; iarg<argc; ++iarg){
        try{
            FrameFile frame_file(argv[iarg]);
            const dune::FelixFrame* frame=frame_file.frame(0);
            uint64_t timestamp=frame->timestamp();
            uint8_t crate = frame->crate_no();
            uint8_t fiber = frame->fiber_no();
            uint8_t slot  = frame->slot_no();
            printf("%-30s %#" PRIx64 " %d %d %d\n", argv[iarg], timestamp, crate, fiber, slot);
        } catch(std::runtime_error){
            printf("%-30s empty\n", argv[iarg]);
        }
    }
}
