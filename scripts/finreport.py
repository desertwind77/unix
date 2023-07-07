#!/usr/bin/env python3

from collections import defaultdict
from datetime import datetime
from pathlib import Path
import argparse
import csv
import os
import re

# pylint: disable=import-error
from tabulate import tabulate
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

    def load_transactions( self ):
        '''Read and categorize all transactions from a statement'''
        if self.filename.endswith( 'pdf' ):
            self.load_pdf_file()
        elif self.filename.endswith( 'csv' ):
            self.load_csv_file()
        else:
            pass

    def load_csv_file( self ):
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

    def load_pdf_file( self ):
        '''Read and categorize all transactions from a .pdf file'''
        field_date = self.credit_card.fields[ 'Transaction Date' ]
        field_desc = self.credit_card.fields[ 'Description' ]
        field_amount = self.credit_card.fields[ 'Amount' ]

        # HACK: get the year from filename
        year = str( Path( self.filename ).name )[ :4 ] \
                if not self.credit_card.has_year_in_date else None

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
                amount = round( float( obj.group( field_amount ) ), 2 )
                category = self.get_category( description )
                transaction = Transaction( self, date, description, category, amount )
                self.transactions.append( transaction )

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

    def update_spreadsheet( self ):
        '''Update the Expense google spreadsheet'''
        pass

    def load_all_transactions( self ):
        '''Load all transactions in all statements and add them to the right categories'''
        for statement in self.statements:
            statement.load_transactions()

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
            for transaction in unknown_transactions:
                print( Path( transaction.statement.filename ).name, transaction.date, transaction.description )
            raise UnknownTransactionsException
        known_categories = list( set( known_categories ) )

        self.calculate_expenses_by_category( known_categories )

    def print_expense_summary( self ):
        table = []
        header = [ 'Category', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
                   'Oct', 'Nov', 'Dec' ]
        for category in sorted( self.expense_by_category.keys() ):
            if category in [ 'Payment' ]:
                continue
            expenses = self.expense_by_category[ category ]
            row = [ category ] + [ round( expenses.get( i, 0 ) ) for i in range( 1, 13 ) ]
            table.append( row )

        total_row = [ 'Total' ]
        for month in range( 1, 13 ):
            monthly_expenses = 0
            for category, expenses in self.expense_by_category.items():
                if category in [ 'Payment' ]:
                    continue
                monthly_expenses += self.expense_by_category[ category ].get( month, 0 )
            total_row.append( round( monthly_expenses ) )
        table.append( total_row )

        print( tabulate( table, header, tablefmt="presto" ) )

    def run( self ):
        self.load_credit_card_config()
        self.load_category_config()
        self.generate_statements_from_files()
        self.load_all_transactions()
        self.print_expense_summary()
        self.update_spreadsheet()

def process_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument( "-l", "--location", required=True, action='store', dest='location',
                         help="Locaiton of the statement files" )
    return parser.parse_args()

def main():
    args = process_command_line_arguments()
    reporter = CreditReport( CONFIG_FILENAME, args.location )
    reporter.run()

if __name__ == '__main__':
    main()
