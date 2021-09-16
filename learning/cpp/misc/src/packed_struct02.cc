#include<stdio.h>

struct __attribute__((__packed__)) packedStruct {
    char chrVar;
    long longVar;
};

int main() {
    struct packedStruct structArray[] = { { 'a', 1234 },
                                          { 'b', 2345 },
                                          { 'c', 3456 },
                                        };
    int i;

    for( i = 0; i<3; i++ ) {
        struct packedStruct *cur = &structArray[ i ];
        // structArray[ i ].longVar is a one-byte-aligned long.
        // So a and b are fine. cur knows it is a pointer to 
        // a packed structure.
        long a = structArray[ i ].longVar;
        long b = cur->longVar;
        // c is a pointer to one-byte-aligned int. Compiler can
        // generate the right code for this.
        long *c __attribute__((aligned(1))) = &structArray[ i ].longVar;
        // Dangerous!!! This may not work on some platforms.
        long *d = &structArray[ i ].longVar;

        printf( "cur = %p\n", (void*)cur );
        printf( "a = %ld\n", a );
        printf( "b = %ld\n", b );
        printf( "c = %ld\n", *c );
        printf( "d = %ld\n", *d );
    }

    return 0;
}
