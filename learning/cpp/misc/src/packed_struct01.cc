#include <stddef.h>
#include <stdio.h>
#include <stdint.h>

struct unpacked_struct {
    uint8_t chr;
    uint16_t id;
    uint64_t lun; 
    uint16_t reserved1; 
    uint32_t reserved2;  
} unpacked_struct;

struct packed_struct {
    uint8_t chr;
    uint16_t id;
    uint64_t lun; 
    uint16_t reserved1; 
    uint32_t reserved2;  
} __attribute__ ((packed)) packed_struct;

int main( int argc, char **argv ) { 
    printf( "offset     \tunpacked\tpacked\n" );
    printf( "chr       :\t%lu\t\t%lu\n",
            offsetof( struct unpacked_struct, chr ),
            offsetof( struct packed_struct, chr ) );
    printf( "id        :\t%lu\t\t%lu\n",
            offsetof( struct unpacked_struct, id ),
            offsetof( struct packed_struct, id ) );
    printf( "lun       :\t%lu\t\t%lu\n",
            offsetof( struct unpacked_struct, lun ),
            offsetof( struct packed_struct, lun ) );
    printf( "reserved1 :\t%lu\t\t%lu\n",
            offsetof( struct unpacked_struct, reserved1 ),
            offsetof( struct packed_struct, reserved1 ) );
    printf( "reserved2 :\t%lu\t\t%lu\n",
            offsetof( struct unpacked_struct, reserved2 ),
            offsetof( struct packed_struct, reserved2 ) );
    printf( "size      :\t%lu\t\t%lu\n",
            sizeof( unpacked_struct ),
            sizeof( packed_struct ) );

    return 0;
}
