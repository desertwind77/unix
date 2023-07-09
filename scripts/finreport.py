#!/usr/bin/env python3
'''Show or queyr my expense summary'''

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
    '''No regular expression to parse a pdf file'''

class UnknownAccountException( Exception ):
    '''A statement doesn't match with accounts defined in the config'''

class UnknownDataTypeInConfigException( Exception ):
    '''Unknown data type found in the config (expectint str or dict)'''

class UnknownTransactionCategoryException( Exception ):
    '''Transactions with unknown categories exists'''

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
class Account:
    '''Represent an account'''
    # pylint: disable=too-many-arguments
    def __init__( self, name, enabled, filename, account_type, regex,
                  has_year_in_date, has_positive_expenses, has_header,
                  fields ):
        self.name = name
        self.enabled = enabled
        self.filename = filename
        self.account_type = account_type
        self.regex = regex
        self.has_year_in_date = has_year_in_date
        self.has_positive_expenses = has_positive_expenses
        self.has_header = has_header
        self.fields = fields

        if self.filename.endswith( '.pdf' ) and not self.regex:
            raise MissingRegexException( self.name )

# pylint: disable=too-few-public-methods
class Transaction:
    '''Represents a transaction'''
    # pylint: disable=too-many-arguments
    def __init__( self, statement, date, description, category, amount ):
        self.statement = statement
        self.date = date
        self.description = description
        self.category = category
        self.amount = amount

    def __str__( self ):
        return f'{self.date.strftime( "%m/%d/%Y")}   {self.amount}   {self.description}'

class Statement:
    '''Represent a credit card or a bank statement containing transactions'''
    def __init__( self, filename, account, category_info ):
        self.filename = filename
        self.account = account
        self.category_info = category_info
        self.transactions = []

    def get_category( self, description ):
        '''Get the category of a transaction'''
        account_type = self.account.account_type
        known_category = None
        for merchant, category in self.category_info[ account_type ].items():
            if re.search( merchant.lower(), description.lower() ):
                known_category = category
                break
        return known_category

    def cleanup_description( self, description ):
        '''Replace unwanted characters that may confuse the regular expression'''
        result = description
        for src, dst in self.category_info[ 'Replace' ].items():
            result = result.replace( src, dst )
        return result

    def load_transactions( self, verbose=False ):
        '''Read and categorize all transactions from a statement'''
        if not self.account.enabled:
            return
        if self.filename.endswith( 'pdf' ):
            self.load_pdf_file( verbose=verbose )
        elif self.filename.endswith( 'csv' ):
            self.load_csv_file( verbose=verbose )
        else:
            pass

    # pylint: disable=too-many-locals
    def load_csv_file( self, verbose=False ):
        '''Read and categorize all transactions from a .csv file'''
        field_date = self.account.fields[ 'Transaction Date' ]
        field_desc = self.account.fields[ 'SEARCH' ]
        field_amount = self.account.fields[ 'Amount' ]

        account_type = self.account.account_type
        ignored_categories = self.category_info[ 'Ignored' ][ account_type ]

        skip_header = self.account.has_header
        with open( self.filename, 'rt', encoding='utf-8' ) as file:
            reader = csv.reader( file )
            for row in reader:
                if skip_header:
                    skip_header = False
                    continue
                if not row:
                    continue
                date = datetime.strptime( row[ field_date ], '%m/%d/%Y' )
                description = self.cleanup_description( row[ field_desc ] )
                amount = row[ field_amount ].replace( '$', '' )
                modifier = 1
                obj = re.match( r'\(([0-9.]+)\)', amount )
                if obj:
                    amount = obj.group( 1 )
                    modifier = -1
                amount = modifier * round( float( amount ), 2 )
                amount = -1 * amount if self.account.has_positive_expenses else amount
                category = self.get_category( description )
                if category in ignored_categories:
                    continue
                transaction = Transaction( self, date, description, category, amount )
                self.transactions.append( transaction )

    # pylint: disable=too-many-locals
    def load_pdf_file( self, verbose=False ):
        '''Read and categorize all transactions from a .pdf file'''
        field_date = self.account.fields[ 'Transaction Date' ]
        field_desc = self.account.fields[ 'Description' ]
        field_amount = self.account.fields[ 'Amount' ]

        account_type = self.account.account_type
        ignored_categories = self.category_info[ 'Ignored' ][ account_type ]

        # Get the year from filename for the statements in which
        # no year in the transaction date
        file_path = Path( self.filename )
        year = str( file_path.name )[ :4 ] \
                if not self.account.has_year_in_date else None

        count = 0
        reader = PyPDF2.PdfReader( self.filename, strict=False )
        for page in reader.pages:
            text = page.extract_text()
            for line in text.splitlines():
                obj = re.match( self.account.regex, line )
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
                amount = -1 * amount if self.account.has_positive_expenses else amount
                category = self.get_category( description )
                if category in ignored_categories:
                    continue
                transaction = Transaction( self, date, description, category, amount )
                self.transactions.append( transaction )
                count += 1
        if verbose:
            print( f'{str( file_path.name )} : transactions = {count}' )

class CreditReport:
    def __init__( self, config_filename, statement_location ):
        self.config = load_config( config_filename )
        self.statement_location = statement_location
        self.account_info = {}
        self.category_info = {}
        self.statements = []
        self.expense_by_category = {}

    def load_account_config( self ):
        """Create an Account object whic represents an account"""
        account_config = self.config[ 'Accounts' ]
        for name, info in account_config.items():
            enabled = info[ 'Enabled' ] == 'True'
            filename = info[ 'Filename' ]
            account_type = info[ 'Type' ]
            regex = info.get( 'Regex', None )
            has_year_in_date = info[ 'Has Transaction Year' ] == 'True'
            has_positive_expenses = info['Has Postive Expenses' ] == 'True'
            has_header = info.get( 'Header', False )
            fields = info[ 'Fields' ]
            self.account_info[ name ] = Account( name, enabled, filename, account_type,
                                                 regex, has_year_in_date,
                                                 has_positive_expenses,
                                                 has_header, fields )

    def load_category_config( self ):
        '''Create a dictionary from 'expense' to category'''
        category_data = self.config[ 'Category' ]

        for account_type in [ "Credit Card", "Bank Account" ]:
            self.category_info[ account_type ] = {}
            account_category_data = category_data[ account_type ]
            for category, expenses in account_category_data.items():
                for expense in expenses:
                    if isinstance( expense, dict ):
                        for key in expense.keys():
                            self.category_info[ account_type ][ key ] = category
                    elif isinstance( expense, str ):
                        self.category_info[ account_type ][ expense ] = category
                    else:
                        raise UnknownDataTypeInConfigException( type( expense ) )

        self.category_info[ 'Ignored' ] = category_data[ 'Ignored' ]
        self.category_info[ 'Replace' ] = category_data[ 'Replace' ]

    def generate_statements_from_files( self ):
        '''Create a Statement object for each available statement files on the drive'''
        statement_path = Path( self.statement_location )

        statement_files = list( statement_path.glob( '*.pdf' ) )
        statement_files += list( statement_path.glob( '*.csv' ) )

        for statement_file in statement_files:
            filename = str( statement_file.name )
            statement = None
            for _, account in self.account_info.items():
                obj = re.match( account.filename, filename )
                if obj:
                    statement = Statement( str( statement_file ), account, self.category_info )
            if not statement:
                raise UnknownAccountException( str( statement_file ) )
            self.statements.append( statement )

    def calculate_expenses_by_category( self, known_categories ):
        '''Calculate expenses by ( account type, category )'''
        for account_type, categories in known_categories.items():
            self.expense_by_category[ account_type ] = {}
            for category in categories:
                self.expense_by_category[ account_type ][ category ] = defaultdict( float )

        for statement in self.statements:
            account_type = statement.account.account_type
            for transaction in statement.transactions:
                amount = self.expense_by_category[ account_type ] \
                        [ transaction.category ][ transaction.date.month ]
                amount += transaction.amount
                amount = round( amount, 2 )
                self.expense_by_category[ account_type ][ transaction.category ] \
                        [ transaction.date.month ] = amount

    def load_all_transactions( self, verbose=False ):
        '''Load all transactions in all statements and add them to the right categories'''
        for statement in sorted( self.statements, key=lambda x: x.filename, reverse=False ):
            statement.load_transactions( verbose=verbose )

        # See if there are any transactions without category
        unknown_transactions = []
        known_categories = defaultdict( list )
        for statement in self.statements:
            for transaction in statement.transactions:
                account_type = statement.account.account_type
                if transaction.category is None:
                    unknown_transactions.append( transaction )
                else:
                    known_categories[ account_type ].append( transaction.category )
        if unknown_transactions:
            print( 'Unknown transactions:' )
            for transaction in unknown_transactions:
                print( Path( transaction.statement.filename ).name,
                       transaction.date, transaction.description )
            raise UnknownTransactionCategoryException
        for account_type, categories in known_categories.items():
            known_categories[ account_type ] = list( set( categories ) )

        self.calculate_expenses_by_category( known_categories )

    def print_expense_summary_by_account_type( self, account_type ):
        '''Print the financial report'''
        table = []
        header = [ 'Category', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
                   'Oct', 'Nov', 'Dec', 'Total' ]
        for category in sorted( self.expense_by_category[ account_type ].keys() ):
            expenses = self.expense_by_category[ account_type ][ category ]
            row = [ round( expenses.get( i, 0 ) ) for i in range( 1, 13 ) ]
            total = sum( row )
            row = [ category ] + row + [ total ]
            table.append( row )
        table.append( SEPARATING_LINE )

        total_row = []
        for month in range( 1, 13 ):
            monthly_expenses = 0
            for category, expenses in self.expense_by_category[ account_type ].items():
                monthly_expenses += expenses.get( month, 0 )
            total_row.append( round( monthly_expenses ) )
        total = sum( total_row )
        total_row = [ 'Subtotal' ] + total_row + [ total ]
        table.append( total_row )

        print( tabulate( table, header, tablefmt="simple", intfmt="," ) )

    def print_expense_summary( self ):
        '''Print expense summary'''
        for account_type in sorted( self.expense_by_category.keys() ):
            print( f'[{account_type}]' )
            self.print_expense_summary_by_account_type( account_type )
            print()

    def query( self, account=None, month=None, category=None, group_by_account=False, verbose=False ):
        if verbose:
            query_str = 'Query: '
            if account:
                query_str += f'account = {account}, '
            if month:
                query_str += f'month = {month}, '
            if category:
                query_str += f'category = {category}, '
            if group_by_account:
                query_str += 'grouping = True'
            print( query_str )
            print()

        result = defaultdict( list ) if group_by_account else []

        for statement in self.statements:
            for transaction in statement.transactions:
                if account and transaction.statement.account.name != account:
                    continue
                if month and transaction.date.month != month:
                    continue
                if category and transaction.category != category:
                    continue

                if isinstance( result, list ):
                    result.append( transaction )
                else:
                    result[ transaction.statement.account.name ].append( transaction )

        if isinstance( result, list ):
            result = sorted( result, key=lambda x: x.date )
            list( map( print, result ) )
            total = round( sum( t.amount for t in result ), 2 )
            print( f'Total = {total}' )
        elif isinstance( result, defaultdict ):
            for account_name, expenses in result.items():
                print( account_name )
                expenses = sorted( expenses, key=lambda x: x.date )
                list( map( print, expenses ) )
                total = round( sum( t.amount for t in expenses ), 2 )
                print( f'Total = {total}' )
                print()

    def run( self, account=None, month=None, category=None,
             group_by_account=False, verbose=False ):
        '''Generate the financial report'''
        self.load_account_config()
        self.load_category_config()
        self.generate_statements_from_files()
        self.load_all_transactions( verbose=verbose )
        if not any( [ account, month, category ] ):
            self.print_expense_summary()
        else:
            self.query( account=account, month=month, category=category,
                        group_by_account=group_by_account,
                        verbose=verbose )

def process_command_line_arguments():
    '''Process command line arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument( "-a", "--account", action='store',
                         help="Account of interest" )
    parser.add_argument( "-c", "--category", action='store',
                         help="Category of interest" )
    parser.add_argument( "-g", "--group", action='store_true',
                         help="Group transactions by account" )
    parser.add_argument( "-l", "--location", required=True, action='store',
                         dest='location', help="Locaiton of the statement files" )
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
    account = args.account
    category = args.category
    group = args.group
    month = int( args.month ) if args.month else None
    year = args.year if args.year else datetime.now().year
    verbose = args.verbose
    location = str( Path( args.location )/str( year ) )
    if not os.path.exists( location ):
        print( f'{location} does not exist' )
        return

    reporter = CreditReport( CONFIG_FILENAME, location )
    reporter.run( account=account, month=month, category=category,
                  group_by_account=group, verbose=verbose )

if __name__ == '__main__':
    main()
