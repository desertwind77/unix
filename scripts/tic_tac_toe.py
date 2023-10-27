#!/usr/bin/env python
'''
A script to play Tic Tac Toe against the computer.
This script demonstrates the Minimax algorithm.

TODO:
- 4 x 4 is to slow for the algorithm to compute the complete decision tree
'''

import uuid

class TicTacToe:
    '''The classic Tic Tac Toe board game'''
    def __init__( self, size=3 ):
        self.size = size
        self.human = 'O'
        self.machine = 'X'
        self.empty = ' '
        self.tie = 'T'
        self.board = [ [ self.empty for _ in range( self.size ) ]
                       for _ in range( self.size ) ]

    def draw( self ):
        '''Draw the board'''
        col = [ str( i ) for i in range( self.size ) ]
        col_str = '    ' + '   '.join( col )
        print( col_str )
        for row in range( self.size ):
            content = f'{row} | ' + ' | '.join( self.board[ row ] ) + ' |'
            print( content )
        print()

    def check_winner( self ):
        '''Check if there is a winner

        return:
            the winner or None
        '''
        # horizontal
        for row in range( self.size ):
            value = list( set( self.board[ row ][ i ] for i in range( self.size ) ) )
            if len( value ) == 1 and value[ 0 ] != self.empty:
                return value[ 0 ]

        # vertical
        for col in range( self.size ):
            value = list( set( self.board[ i ][ col ] for i in range( self.size ) ) )
            if len( value ) == 1 and value[ 0 ] != self.empty:
                return value[ 0 ]

        # diagonal
        value = list( set( self.board[ row ][ row ] for row in range( self.size ) ) )
        if len( value ) == 1 and value[ 0 ] != self.empty:
            return value[ 0 ]
        value = list( set( self.board[ row ][ self.size - row - 1 ]
                           for row in range( self.size ) ) )
        if len( value ) == 1 and value[ 0 ] != self.empty:
            return value[ 0 ]

        empty_count = [ self.board[ r ][ c ] for r in range( self.size )
                        for c in range( self.size ) if self.board[ r ][ c] == self.empty ]
        if len( empty_count ) == 0:
            return self.tie

        return None

    def minimax( self, depth, is_maximizing ):
        '''The minimax algorithm to calculate the score of the current move

        Minimax is a kind of backtracking algorithm that is used in decision
        making and game theory to find the optimal move for a player, assuming
        that your opponent also plays optimally. It is widely used in two
        player turn-based games such as Tic-Tac-Toe, Backgammon, Mancala,
        Chess, etc.

        Since this is a backtracking based algorithm, it tries all possible
        moves, then backtracks and makes a decision.

        Time complexity : O(b^d) b is the branching factor and d is count of
        depth or ply of graph or tree.

        Space Complexity : O(bd) where b is branching factor into d is maximum
        depth of tree similar to DFS.
        '''
        result = self.check_winner()
        if result:
            if result == self.tie:
                return 0
            if result == self.human:
                return -1
            return 1

        if is_maximizing:
            best_score = -10
            for row in range( self.size ):
                for col in range( self.size ):
                    if self.board[ row ][ col ] != self.empty:
                        continue
                    self.board[ row ][ col ] = self.machine
                    score = self.minimax( depth + 1, False )
                    best_score = max( best_score, score )
                    self.board[ row ][ col ] = self.empty
        else:
            best_score = 10
            for row in range( self.size ):
                for col in range( self.size ):
                    if self.board[ row ][ col ] != self.empty:
                        continue
                    self.board[ row ][ col ] = self.human
                    score = self.minimax( depth + 1, True )
                    best_score = min( best_score, score )
                    self.board[ row ][ col ] = self.empty
        return best_score

    def best_move( self ):
        '''For the computer to choose his next best move, one with the
        highest score according to the minimax algorithm'''
        best_score = -10
        move_row = move_col = None
        for row in range( self.size ):
            for col in range( self.size ):
                if self.board[ row ][ col ] != self.empty:
                    continue
                self.board[ row ][ col ] = self.machine
                score = self.minimax( 0, False )
                self.board[ row ][ col ] = self.empty

                if score >= best_score:
                    best_score = score
                    move_row, move_col = row, col
        self.board[ move_row ][ move_col ] = self.machine

    def play( self, human_first=None ):
        '''Play the game agaist the computer'''
        def coin_toss():
            '''Return either True or False 50% of the times'''
            gen_id = str( uuid.uuid4() )
            while not gen_id[ 0 ].isnumeric():
                gen_id = str( uuid.uuid4() )
            return int( gen_id[ 0 ] ) >= 5

        count = 0
        human = human_first if human_first else coin_toss()

        if human:
            self.draw()

        while count < self.size * self.size:
            if human:
                input_str  = input( "row col = ").strip()
                if input_str == 'q':
                    return
                row, col = input_str.split( ' ')
                row, col = int( row ), int( col )
                if row >= self.size or col >= self.size:
                    continue
                if self.board[ row ][ col ] != self.empty:
                    continue
                self.board[ row ][ col ] = self.human
            else:
                self.best_move()
            self.draw()
            count += 1
            human = not human

            winner = self.check_winner()
            if not winner:
                continue
            if winner == self.tie:
                print( 'Tie!' )
            else:
                print( f'{winner} won!' )
            break

def main():
    '''The main program'''
    game = TicTacToe()
    game.play()

if __name__ == '__main__':
    main()
