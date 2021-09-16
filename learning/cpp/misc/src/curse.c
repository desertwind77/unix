// psax.c : illustration of curses library
//
// runs the shell command 'ps ax' and saves the last lines of its output,
// as many as the window will fit; allow the user to move up and down
// within the window, with the option to kill whichever process is currently
// highlighted
//
// user cammonds:
//      'u' : move the highlight up a line
//      'd' : move the highlight down a line
//      'k' : kill process in currently highlighted line
//      'r' : re-run 'ps ax' for update
//      'q' : quit
//
//  possible extensions: allowing scrolling, so that the user could go
//  through all the 'ps ax' output, not just the last lines ; allow wraparound
//  for long lines; ask user to confirm before killing a process
#include <curses.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <unistd.h>

#define MAXROW 1000
#define MAXCOL 500

// will point to curses window object
WINDOW *scrn;
// output of 'ps ax' (better to use malloc()
char cmdoutlines[ MAXROW ][ MAXCOL ];   
int ncmdlines,      // number of rows in cmdoutlines
    nwinlines,      // number of rows our 'ps ax' output occupies in the
                    // xterm (or equiv.) window
    winrow,         // current row position in screen
    cmdstartrow,    // index of first row in cmdoutlines to be displayed
    cmdlastrow;     // index of last row in cmdoutlines to be displayed

// rewrites the line at winrow in bold font
void highlight() {
    int clinenum;

    // This curses library call says that whatever we write from now on
    // (until we say otherwise) will be in bold font
    attron( A_BOLD );

    // We'll need to rewrite the cmdoutlines line currently displayed
    // at line winrow in the screen, so as to get the bold font.
    clinenum = cmdstartrow + winrow;
    mvaddstr( winrow, 0, cmdoutlines[ clinenum ] );

    // OK, leave bold mode
    attroff( A_BOLD );
    // make the change appear on the screen
    refresh();
}

// run "ps ax" and stores the output in cmdoutlines
void runpsax() {
    FILE *p;
    char ln[ MAXCOL ];
    int row;
    char *tmp;

    // open UNIX pipe (enables one program to read output of another
    // as if it were a file )
    p = popen( "ps ax", "r" );

    for( row = 0 ; row < MAXROW ; row++ ) {
        // read one line from the pipe
        tmp = fgets( ln, MAXCOL, p );
        // if end of pipe, break
        if( tmp == NULL ) break;
        // don't want stored line to exceed width of screen, which the
        // curses library provides to us in the variables COLS, so truncate
        // to at most COLS characters
        strncpy( cmdoutlines[ row ], ln, COLS );
        cmdoutlines[ row ][ MAXCOL - 1 ] = 0;
    }

    ncmdlines = row;
    pclose( p );
}

// displays last part of command output (as much as fits in screen)
void showlastpart() {
    int row;

    // curses clear-screen call
    clear();

    // prepare to paint the (last part of the) 'ps ax' output on the screen;
    // two cases, depending on whether there is more output than screen rows;
    // first, the case in which the entire output fits in one screen:
    if( ncmdlines <= LINES ) {
        // LINES is an int maintained by the curses library, equal
        // to the number of lines in the screen
        cmdstartrow = 0;
        nwinlines = ncmdlines;
    } else {
        // now the case in which the output is bigger than one screen
        cmdstartrow = ncmdlines - LINES;
        nwinlines = LINES;
    }
    cmdlastrow = cmdstartrow + nwinlines - 1;

    // now paint the rows to the screen
    for( row = cmdstartrow, winrow = 0 ; row <= cmdlastrow ; row++, winrow++ ) {
        // curses call to move to the specified position and paint a string
        // there
        mvaddstr( winrow, 0, cmdoutlines[ row ] );
    }

    // now make the changes actually appear on the screen,
    // using this call to the curses library
    refresh();

    // highlight the last line
    winrow--;
    highlight();
}

// moves cursor up/down one line
void updown( int inc ) {
    int tmp = winrow + inc;

    // ignore attempts to go off the edge of the screen
    if( tmp >= 0 && tmp < LINES ) {
        // rewrite the current line before moving; since our current font
        // is non-BOLD (actually A_NORMAL), the effect is to unhighlight this
        // line
        mvaddstr( winrow, 0, cmdoutlines[ cmdstartrow + winrow ] );
        // highlight the line we're moving to
        winrow = tmp;
        highlight();
    }
}

// run or re-run "ps ax"
void rerun() {
    runpsax();
    showlastpart();
}

void prockill() {
    char *pid;

    pid = strtok( cmdoutlines[ cmdstartrow + winrow ], " " );
    kill( atoi( pid ), 9 );
    rerun();
}

int main( void ) {
    char c;

    // window setup which is a standard initializing sequence for curse programs
    scrn = initscr();
    // don't echo keystrokes
    noecho();
    // keyboard input valid immediately, not after hit Enter
    cbreak();
    // run 'ps ax' and process the output
    runpsax();
    // display in the window
    showlastpart();

    // user command loop
    while( 1 ) {
        c = getch();
        if( c == 'u' ) {
            updown( -1 );
        } else if( c == 'd' ) {
            updown( 1 );
        } else if( c == 'r' ) {
            rerun();
        } else if( c == 'k' ) {
            prockill();
        } else {
            break;
        }
    }

    // restore original settings
    endwin();

    return 0;
}
