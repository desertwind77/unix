#include <algorithm>
#include <functional>
#include <iostream>
#include <vector>
#include "shape.h"
using namespace std;

class myshape : public rectangle {
    line *l_eye, *r_eye, *mouth;
 public:
    myshape( point, point );
    void draw();
    void move( int, int );
};

myshape::myshape( point a, point b ) : rectangle( a, b ) {
    int ll = neast().x - swest().x + 1;
    int hh = neast().y - swest().y + 1;
    l_eye = new line( point( swest().x + 2, swest().y + hh * 3/4 ), 2 );
    r_eye = new line( point( swest().x + ll - 4, swest().y + hh * 3/4 ), 2 );
    mouth = new line( point( swest().x + 2, swest().y + hh / 4 ), ll - 4 );
}

void myshape::draw() {
    rectangle::draw();
    int a = ( swest().x + neast().x ) / 2;
    int b = ( swest().y + neast().y ) / 2;
    put_point( point( a, b ) );
}

void myshape::move( int a, int b ) {
    rectangle::move( a, b );
    l_eye->move( a, b );
    r_eye->move( a, b );
    mouth->move( a, b );
}

struct CompWestX : binary_function<shape*, shape*, bool> {
    bool operator()( shape *p, shape *q ) const {
        return p->west().x < q->west().x;
    }
} compWestX;

void outputWestX( const vector<shape*> &vs ) {
    vector<shape*>::const_iterator i;
    for( i = vs.begin() ; i != vs.end() ; ++i ) {
        cout << "The x-coordinate of the west point of shape "
             << i - vs.begin() << " is " << (*i)->west().x << endl;
    }
}

int main() {
    screen_init();

    shape *p1 = new rectangle( point( 0, 0 ), point( 10, 10 ) );
    shape *p2 = new line( point( 0, 15 ), 17 );
    shape *p3 = new myshape( point( 15, 10 ), point( 27, 18 ) );
    shape_refresh();

    p3->move( -10, -10 );
    stack( p2, p3 );
    stack( p1, p2 );
    shape_refresh();

    vector<shape*> vs;
    vs.push_back( p1 );
    vs.push_back( p2 );
    vs.push_back( p3 );

    vector<shape*>::iterator i;
    for( i = vs.begin() ; i != vs.end() ; ++i ) {
        ( *i )->move( 20, 0 );
    }
    shape_refresh();

    outputWestX( vs );
    cout << "Sorting the shape according to the x-coordinate of "
         << "their west points" << endl;
    sort( vs.begin(), vs.end(), compWestX );
    cout << "After sorting:" << endl;
    outputWestX( vs );
    screen_destroy();

    return 0;
}
