#!/usr/bin/env python3

from collections import defaultdict
from datetime import datetime
from pathlib import Path
import argparse
import csv
import os
import re

# tabulate doc : https://pypi.org/project/tabulate/
# pylint: disable=import-error
from tabulate import tabulate, SEPARATING_LINE
import PyPDF2

from genutils import load_config

CONFIG_FILENAME="config/finreport.json"

class MissingRegexException( Exception ):
    pass

class UnknownCreditCardException( Exception ):
    pass

class UnknownTypeException( Exception ):
    pass

class UnknownTransactionsException( Exception ):
    pass

class CreditCard:
    def __init__( self, name, filename, regex, has_year_in_date, has_negative_amount, has_header, fields ):
        self.name = name
        self.filename = filename
        self.regex = regex
        self.has_year_in_date = has_year_in_date
        self.has_negative_amount = has_negative_amount
        self.has_header = has_header
        self.fields = fields

        if self.filename.endswith( '.pdf' ) and not self.regex:
            raise MissingRegexException( self.name )

class Transaction:
    def __init__( self, statement, date, description, category, amount ):
        self.statement = statement
        self.date = date
        self.description = description
        self.category = category
        self.amount = amount

    def __str__( self ):
        return f'{self.date.strftime( "%m/%d/%Y")}   {self.amount}   {self.description}'

class Statement:
    def __init__( self, filename, credit_card, category_info, replace_info ):
        self.filename = filename
        self.credit_card = credit_card
        self.category_info = category_info
        self.replace_info = replace_info
        self.transactions = []

    def get_category( self, description ):
        '''Get the category of a transaction'''
        known_category = None
        for merchant, category in self.category_info.items():
            if re.search( merchant.lower(), description.lower() ):
                known_category = category
                break
        return known_category

    def cleanup_description( self, description ):
        result = description
        for src, dst in self.replace_info.items():
            result = result.replace( src, dst )
        return result

    def load_transactions( self, verbose=False ):
        '''Read and categorize all transactions from a statement'''
        if self.filename.endswith( 'pdf' ):
            self.load_pdf_file( verbose=verbose )
        elif self.filename.endswith( 'csv' ):
            self.load_csv_file( verbose=verbose )
        else:
            pass

    def load_csv_file( self, verbose=False ):
        '''Read and categorize all transactions from a .csv file'''
        field_date = self.credit_card.fields[ 'Transaction Date' ]
        field_desc = self.credit_card.fields[ 'Description' ]
        field_amount = self.credit_card.fields[ 'Amount' ]

        skip_header = self.credit_card.has_header
        with open( self.filename, 'rt', encoding='utf-8' ) as file:
            reader = csv.reader( file )
            for row in reader:
                if skip_header:
                    skip_header = False
                    continue
                date = datetime.strptime( row[ field_date ], '%m/%d/%Y' )
                description = self.cleanup_description( row[ field_desc ] )
                amount = round( float( row[ field_amount ] ), 2 )
                amount = -1 * amount if self.credit_card.has_negative_amount else amount
                category = self.get_category( description )
                transaction = Transaction( self, date, description, category, amount )
                self.transactions.append( transaction )

    def load_pdf_file( self, verbose=False ):
        '''Read and categorize all transactions from a .pdf file'''
        field_date = self.credit_card.fields[ 'Transaction Date' ]
        field_desc = self.credit_card.fields[ 'Description' ]
        field_amount = self.credit_card.fields[ 'Amount' ]

        # Get the year from filename for credit card statement in which
        # no year in the transaction date
        file_path = Path( self.filename )
        year = str( file_path.name )[ :4 ] \
                if not self.credit_card.has_year_in_date else None

        count = 0
        reader = PyPDF2.PdfReader( self.filename )
        for page in reader.pages:
            text = page.extract_text()
            for line in text.splitlines():
                obj = re.match( self.credit_card.regex, line )
                if not obj:
                    continue
                date = obj.group( field_date )
                # pylint: disable=fixme
                # FIXME: assuming the date is in the format mm/dd
                date = f'{date}/{year}' if year else date
                date = datetime.strptime( date, '%m/%d/%Y' )
                description = self.cleanup_description( obj.group( field_desc ) )
                amount = obj.group( field_amount ).replace( ',', '' )
                amount = round( float( amount ), 2 )
                category = self.get_category( description )
                transaction = Transaction( self, date, description, category, amount )
                self.transactions.append( transaction )
                count += 1
        if verbose:
            print( f'{str( file_path.name )} : transactions = {count}' )

class MonthlyExpenses:
    def __init__( self, month ):
        self.month = month
        self.transactions = {}
        self.expense_by_category = {}

class CreditReport:
    def __init__( self, config_filename, statement_location ):
        self.config = load_config( config_filename )
        self.statement_location = statement_location
        self.creditcard_info = {}
        self.replace_info = {}
        self.category_info = {}
        self.statements = []
        # expense_by_category[ category ][ month ] -> amount
        self.expense_by_category = {}

    def load_credit_card_config( self ):
        '''Create a credit card object for each credit card'''
        credit_card_config = self.config[ 'Credit Card' ]
        for name, info in credit_card_config.items():
            filename = info[ 'Filename' ]
            regex = info.get( 'Regex', None )
            has_year_in_date = info.get( 'Transaction Year', False )
            has_negative_amount = info.get( 'Negative Amount', False )
            has_header = info.get( 'Header', False )
            fields = info[ 'Fields' ]
            self.creditcard_info[ name ] = CreditCard( name, filename, regex,
                                                       has_year_in_date,
                                                       has_negative_amount,
                                                       has_header, fields )

        self.replace_info = self.config[ 'Replace' ]

    def load_category_config( self ):
        '''Create a dictionary from 'expense' to category'''
        category_data = self.config[ 'Category' ]
        for category, expenses in category_data.items():
            for expense in expenses:
                if isinstance( expense, dict ):
                    for key in expense.keys():
                        self.category_info[ key ] = category
                elif isinstance( expense, str ):
                    self.category_info[ expense ] = category
                else:
                    raise UnknownTypeException( type( expense ) )

    def generate_statements_from_files( self ):
        '''Create a Statement object for each available statement files on the drive'''
        statement_path = Path( self.statement_location )

        statement_files = list( statement_path.glob( '*.pdf' ) )
        statement_files += list( statement_path.glob( '*.csv' ) )

        for statement_file in statement_files:
            filename = str( statement_file.name )
            statement = None
            for _, card in self.creditcard_info.items():
                obj = re.match( card.filename, filename )
                if obj:
                    statement = Statement( str( statement_file ), card, self.category_info, self.replace_info )
            if not statement:
                raise UnknownCreditCardException( str( statement_file ) )
            self.statements.append( statement )

    def calculate_expenses_by_category( self, known_categories ):
        for category in known_categories:
            self.expense_by_category[ category ] = defaultdict( float )

        for statement in self.statements:
            for transaction in statement.transactions:
                amount = self.expense_by_category[ transaction.category ][ transaction.date.month ]
                amount += transaction.amount
                amount = round( amount, 2 )
                self.expense_by_category[ transaction.category ][ transaction.date.month ] = amount

    def load_all_transactions( self, verbose=False ):
        '''Load all transactions in all statements and add them to the right categories'''
        for statement in sorted( self.statements, key=lambda x: x.filename, reverse=False ):
            statement.load_transactions( verbose=verbose )

        # See if there are any transactions without category
        unknown_transactions = []
        known_categories = []
        for statement in self.statements:
            for transaction in statement.transactions:
                if transaction.category is None:
                    unknown_transactions.append( transaction )
                else:
                    known_categories.append( transaction.category )
        if unknown_transactions:
            print( 'Unknown transactions:' )
            for transaction in unknown_transactions:
                print( Path( transaction.statement.filename ).name,
                       transaction.date, transaction.description )
            raise UnknownTransactionsException
        known_categories = list( set( known_categories ) )

        self.calculate_expenses_by_category( known_categories )

    def print_expense_summary( self ):
        '''Print the financial report'''
        table = []
        header = [ 'Category', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
                   'Oct', 'Nov', 'Dec', 'Total' ]
        for category in sorted( self.expense_by_category.keys() ):
            if category in [ 'Payment' ]:
                continue
            expenses = self.expense_by_category[ category ]
            row = [ round( expenses.get( i, 0 ) ) for i in range( 1, 13 ) ]
            total = sum( row )
            row = [ category ] + row + [ total ]
            table.append( row )
        table.append( SEPARATING_LINE )

        total_row = []
        for month in range( 1, 13 ):
            monthly_expenses = 0
            for category, expenses in self.expense_by_category.items():
                if category in [ 'Payment' ]:
                    continue
                monthly_expenses += expenses.get( month, 0 )
            total_row.append( round( monthly_expenses ) )
        total = sum( total_row )
        total_row = [ 'Subtotal' ] + total_row + [ total ]
        table.append( total_row )

        print( tabulate( table, header, tablefmt="simple", intfmt="," ) )

    def query( self, card=None, month=None, category=None, groupByCreditCard=False, verbose=False ):
        if verbose:
            query_str = 'Query: '
            if card:
                query_str += f'card = {card}, '
            if month:
                query_str += f'month = {month}, '
            if category:
                query_str += f'category = {category}'
            print( query_str )
            print()

        result = defaultdict( list ) if groupByCreditCard else []

        for statement in self.statements:
            for transaction in statement.transactions:
                if card and transaction.statement.credit_card.name != card:
                    continue
                if month and transaction.date.month != month:
                    continue
                if category and transaction.category != category:
                    continue
                if isinstance( result, list ):
                    result.append( transaction )
                else:
                    credit_card = transaction.statement.credit_card.name
                    result[ credit_card ].append( transaction )

        if isinstance( result, list ):
            result = sorted( result, key=lambda x: x.date )
            list( map( print, result ) )
        elif isinstance( result, defaultdict ):
            for card, expenses in result.items():
                print( card )
                expenses = sorted( expenses, key=lambda x: x.date )
                list( map( print, expenses ) )
                print()

    def run( self, card=None, month=None, category=None,
             groupByCreditCard=False, verbose=False ):
        '''Generate the financial report'''
        self.load_credit_card_config()
        self.load_category_config()
        self.generate_statements_from_files()
        self.load_all_transactions( verbose=verbose )
        if not any( [ card, month, category ] ):
            self.print_expense_summary()
        else:
            self.query( card=card, month=month, category=category,
                        groupByCreditCard=groupByCreditCard,
                        verbose=verbose )

def process_command_line_arguments():
    '''Process command line arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument( "-l", "--location", required=True, action='store',
                         dest='location', help="Locaiton of the statement files" )
    parser.add_argument( "-C", "--card", action='store',
                         help="Credit card of interest" )
    parser.add_argument( "-c", "--category", action='store',
                         help="Category of interest" )
    parser.add_argument( "-g", "--group", action='store_true',
                         help="Group transactions by card" )
    parser.add_argument( "-m", "--month", action='store',
                         help="Month of interest" )
    parser.add_argument( "-y", "--year", action='store',
                         help="Year of interest" )
    parser.add_argument( "-v", "--verbose", action="store_true",
                         help="Print more information" )
    return parser.parse_args()

def main():
    '''Main program'''
    args = process_command_line_arguments()
    card = args.card
    category = args.category
    group = args.group
    month = int( args.month )
    year = args.year if args.year else datetime.now().year
    verbose = args.verbose
    location = str( Path( args.location )/str( year ) )
    if not os.path.exists( location ):
        print( f'{location} does not exist' )
        return

    reporter = CreditReport( CONFIG_FILENAME, location )
    reporter.run( card=card, month=month, category=category,
                  groupByCreditCard=group, verbose=verbose )

if __name__ == '__main__':
    main()
