#include "FelixFormat.hh"
#include "FrameFile.h"

#include <iostream>
#include <cstdio>
#include <inttypes.h>

int main(int argc, char** argv)
{
    FrameFile frame_file(argv[1]);

    uint64_t prev_timestamp=0;
    size_t nbad=0;

    for(size_t i=0; i<frame_file.num_frames(); ++i){
        const dune::FelixFrame* frame=frame_file.frame(i);
        uint64_t timestamp=frame->timestamp();
        if(i==0) printf("First timestamp %#016" PRIx64 "\n", timestamp);
        if(i==frame_file.num_frames()-1) printf("Last timestamp %#016" PRIx64 "\n", timestamp);
        if(prev_timestamp!=0 && (timestamp-prev_timestamp!=25)){
            if(timestamp>=prev_timestamp){
                printf("Positive inter-frame timestamp gap at index % 4d.  TS before gap: %#016" PRIx64 ". TS after gap:  %#016" PRIx64 ". Difference:  %#016" PRIx64 "\n",
                       i, prev_timestamp, timestamp, (timestamp-prev_timestamp));
            }

            if(timestamp<prev_timestamp){
                printf("Negative inter-frame timestamp gap at index % 4d.  TS before gap: %#016" PRIx64 ". TS after gap:  %#016" PRIx64 ". Difference:  -%#016" PRIx64 "\n",
                       i, prev_timestamp, timestamp, (prev_timestamp-timestamp));
            }
            
            ++nbad;
        }
        prev_timestamp=timestamp;
    }
    std::cout << argv[1] << ": " << nbad << " bad of " << frame_file.num_frames() << std::endl;
}
