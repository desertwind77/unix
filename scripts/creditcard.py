#!/usr/bin/env python3
import argparse
from collections import defaultdict
import csv
import json
import os
from pprint import pprint
import re
import sys

def loadConfig():
    command = sys.argv[ 0 ]
    dirName = os.path.dirname( command )
    defaultConfig = dirName + '/config.json'

    config = None
    with open( defaultConfig ) as f:
        config = json.load( f )
    assert( config )

    return config

def cleanupExpense( expenseDict, modifier=1 ):
    expenseDict = dict( expenseDict )
    for category, amount in expenseDict.items():
        expenseDict[ category ] = modifier * round( amount, 2 )
    return expenseDict

def printDict( myDict ):
    keys = sorted( myDict.keys() )
    for key in keys:
        print( "%s\t%.2f" % ( key, myDict[ key ] ) )

class CreditCardHandler( object ):
    def __init__( self, name, config, statementFile ):
        self.name = name
        self.config = config
        self.statementFile = statementFile
        self.categoryConfig = self.config[ 'Category' ]
        self.cardConfig = self.config[ "Credit Card" ][ self.name ]

    def processTransaction( self ):
        positiveAmount = self.cardConfig.get( 'Positive Amount', None ) 
        fieldDesc = self.cardConfig[ 'Fields' ][ 'Description' ]
        fieldAmount = self.cardConfig[ 'Fields' ][ 'Amount' ]

        def isKnownCategory( transaction ):
            knownCategory = None

            for vendor, category in self.categoryConfig.items():
                if re.search( vendor.lower(), transaction ):
                    knownCategory = category
                    break

            return knownCategory

        expenseDict = defaultdict( float )
        unknownVendors = []
        miscList = []

        with open( self.statementFile, 'rt' ) as f:
            reader = csv.reader( f )

            skipHeader = True
            for row in reader:
                if skipHeader:
                    skipHeader = False
                    continue

                transaction = row[ fieldDesc ].lower()
                amount = float( row[ fieldAmount ] )
                category = isKnownCategory( transaction )
                if category == 'Ignore':
                    continue
                if category == 'Misc':
                    miscList.append( row )
                if category:
                    # To print 'Food'
                    #if category == 'Food':
                    #    print( row )
                    expenseDict[ category ] += amount 
                else:
                    unknownVendors.append( row )

        # Clean up
        modifier = 1 if not positiveAmount else -1
        expenseDict = cleanupExpense( expenseDict, modifier )

        return expenseDict, unknownVendors, miscList

def main():
    parser = argparse.ArgumentParser( description='Credit Card statement processing' )
    parser.add_argument( '-a', '--amex', action='store', dest='amex',
                         help='American Express statement' )
    parser.add_argument( '-f', '--freedom', action='store', dest='freedom', 
                         help='Chase Freedom statement' )
    parser.add_argument( '-s', '--sapphire', action='store', dest='sapphire', 
                         help='Chase Sapphire statement' )
    args = parser.parse_args() 

    config = loadConfig()

    cards = []
    if args.amex:
        cards.append( CreditCardHandler( 'Amex', config, args.amex ) )
    if args.freedom:
        cards.append( CreditCardHandler( 'Freedom', config, args.freedom ) )
    if args.sapphire:
        cards.append( CreditCardHandler( 'Sapphire', config, args.sapphire ) )

    hasUnknown = False
    allExpenses = []
    allMisc = []
    for card in cards:
        expenses, unknowns, miscList = card.processTransaction()
        if unknowns:
            hasUnknown = True
            for row in unknowns:
                print( 'Unknown transaction in %s' % card.statementFile )
                print( row )
            print()
        else:
            allExpenses.append( expenses )
            allMisc += miscList

    if hasUnknown:
        sys.exit()

    allCategories = []
    for expense in allExpenses:
        allCategories += expense.keys()

    expenseSummary = defaultdict( float )
    for category in allCategories:
        total = 0
        for expense in allExpenses:
            total += expense.get( category, 0 )
        expenseSummary[ category ] = total
    expenseSummary = cleanupExpense( expenseSummary )

    print( 'Summary:' )
    printDict( expenseSummary )

    print( '\nMiscellenous:' )
    for row in allMisc:
        print( row )

if __name__ == "__main__":
    main()
