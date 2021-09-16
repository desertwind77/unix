#include <fstream>
#include <iostream>
#include <string>
using namespace std;

int main() {
    string filename = "TCS-genealogy.txt";
    ifstream input( filename );
    if( !input.is_open() ) {
        cerr << "Unable to open file " << filename << endl;
    }

    // while readline
    //  if #, ingore
    //  match name\t+advisor\t+place\t+year\n
    // student -> advisor
    // advisor -> list of student sorted by year

    return 0;
}
