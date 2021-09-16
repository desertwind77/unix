int main() {
    int a[ 1000 ];
    int i;

    for( i = 0 ; i < 1000 ; ++i ) {
        a[ i ] = i;
    }
    random_shuffle( &a[ 0 ], &a[ 1000 ] );

    // sort into ascending order
    sort( &a[ 0 ], &a[ 1000 ] );

    for( i = 0 ; i < 1000 ; ++i ) {
        assert( a[ i ] == i );
    }
    random_shuffle( &a[ 0 ], &a[ 1000 ] );

    // sort into descending order
    // greater<int> is a functional object
    sort( &a[ 0 ], &a[ 1000 ], greater<int>() );
    for( i = 0 ; i < 1000 ; ++i ) {
        assert( a[ i ] == 1000 - i - 1 );
    }

    return 0;
}
