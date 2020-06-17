#include "FelixFormat.hh"
#include "FrameFile.h"

#include <iostream>
int main(int argc, char** argv)
{
    FrameFile frame_file(argv[1]);

    uint64_t prev_timestamp=0;
    size_t nbad=0;

    for(size_t i=0; i<frame_file.num_frames(); ++i){
        const dune::FelixFrame* frame=frame_file.frame(i);
        uint64_t timestamp=frame->timestamp();

        if(prev_timestamp!=0 && (timestamp-prev_timestamp!=25)){
            std::cerr << "Inter-frame timestamp gap of " << (timestamp-prev_timestamp) << " ticks at ts 0x" << std::hex << timestamp << std::dec << ". index=" << i << std::endl;
            ++nbad;
        }
        prev_timestamp=timestamp;
    }
    std::cout << argv[1] << ": " << nbad << " bad of " << frame_file.num_frames() << std::endl;
}
