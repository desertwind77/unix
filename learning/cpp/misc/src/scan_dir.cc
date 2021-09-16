// This is equivalent to find <dir> 
#include <algorithm>
#include <cstring>
#include <errno.h>
#include <dirent.h>
#include <iostream>
#include <stdio.h>
#include <sys/types.h>
#include <vector>

using namespace std;

class DirEntry {
    string name_;
    bool isDir_;
 public:
    DirEntry( string n_, bool d_ ) : name_( n_ ), isDir_( d_ ) {}
    string & name() { return name_; }
    bool isDir() { return isDir_; }
    bool operator=( const DirEntry &e_ ) {
        return strcmp( name_.c_str(), e_.name_.c_str() ) == 0;
    }
    bool operator<( const DirEntry &e_ ) {
        return strcmp( name_.c_str(), e_.name_.c_str() ) <= 0;
    }
};

bool compareDirEntry( DirEntry *i, DirEntry *j ) { return *i < *j; }

void scan( const char *path ) {
    struct dirent *entry;
    int ret = 1;
    DIR *dir;
    vector<DirEntry *> dirList;

    dir = opendir( path );
    if( !dir ) {
        fprintf( stderr, "scan: unable to open dir %s\n", path );
        return;
    }

    errno = 0;
    while( ( entry = readdir( dir ) ) != NULL ) {
        if( ( entry->d_type == DT_REG ) || ( entry->d_type == DT_DIR ) ) {
            // skip hidden files
            if( ( entry->d_type == DT_REG ) && ( entry->d_name[ 0 ] == '.' ) ) {
                continue;
            }

            DirEntry *d = new DirEntry( entry->d_name, entry->d_type == DT_DIR );
            dirList.push_back( d );
        }
    }

    if( errno && !entry ){
        perror( "readdir:" );
    }

    closedir( dir );

    sort( dirList.begin(), dirList.end(), compareDirEntry );
    for( vector<DirEntry *>::iterator it = dirList.begin() ; it != dirList.end();
            ++it ) {
        DirEntry *entry = *it;
        char newpath[ 1064 ];

        snprintf( newpath, 1064, "%s/%s", path, entry->name().c_str() );
        if( entry->isDir() ) {
            if( ( strcmp( entry->name().c_str(), "." ) == 0 ) || 
                ( strcmp( entry->name().c_str(), ".." ) == 0 ) ) {
                // skip "." and ".."
            } else {
                scan( newpath );
            }
        } else {
            cout << newpath << endl; 
        }
    }
}

int main( int argc, char *argv[] ) {
    if( argc < 2 ) {
        fprintf( stderr, "usage: %s <file>\n", argv[ 0 ] );
        return 1;
    }

    scan( argv[ 1 ] );

    return 0;
}
