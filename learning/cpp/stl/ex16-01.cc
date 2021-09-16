#include <iostream>
#include <algorithm>
#include <string>
using namespace std;

template <typename ForwardIterator>
class counting_iterator {
 private:
    ForwardIterator current;
    int plus_count;
    string name;
    int version;
 public:
    typedef counting_iterator<ForwardIterator> self;
    // Note: iterator_traits, value_type, reference, difference_type,
    //       forward_iterator_tag 
    typedef typename iterator_traits<ForwardIterator>::value_type value_type;
    typedef typename iterator_traits<ForwardIterator>::reference reference;
    typedef typename iterator_traits<ForwardIterator>::pointer pointer;
    typedef typename
        iterator_traits<ForwardIterator>::difference_type difference_type;
    typedef forward_iterator_tag iterator_category;
    // Constructor
    counting_iterator( ForwardIterator first, const string &n ) : current( first ),
        plus_count( 0 ), name( n ), version( 1 ) {}
    // Copy constructor
    counting_iterator( const self &other ) : current( other.current ),
            plus_count( other.plus_count ), name( other.name ),
            version( other.version + 1 ) {
        cout << "copying " << name << ", new version is " << version << endl;
    }
    // Operator overloading
    reference operator*() { return *current; }
    bool operator==( const self &other ) const { return current == other.current; }
    bool operator!=( const self &other ) const { return current != other.current; }
    // prefix
    self& operator++() {
        ++current;
        ++plus_count;
        return *this;
    }
    // postfix
    self operator++( int ) {
        self tmp = *this;
        ++( * this );
        return tmp;
    }
    // display statistics on stream o
    void report( ostream &o ) const {
        o << "Iterator " << name << ", version " << version
          << ", reporting " << plus_count << " ++ operations" << endl;
    }
};

int main() {
    int x[] = { 12, 4, 3, 7, 17, 9, 11, 6 };
    counting_iterator<int*> i( &x[ 0 ], "Curly" );
    counting_iterator<int*> j( &x[ 0 ], "Moe" );
    counting_iterator<int*> end( &x[ 8 ], "Larry" );

    cout << "Traversing array x from i (Curly) to end (Larry)" << endl;
    while( i != end ) {
        cout << *i << endl;
        ++i;
    }

    cout << "After the traversal:" << endl;
    i.report( cout );
    end.report( cout );

    cout << "Assigning j (Moe) to i (Curly)." << endl;
    i = j;
    cout << "Searching the array from i (Moe) to end (Larry) using find" << endl;
    counting_iterator<int*> k = find( i, end, 9 );
    cout << "After the find:" << endl;
    k.report( cout );
    i.report( cout );
    end.report( cout );

    return 0;
}
