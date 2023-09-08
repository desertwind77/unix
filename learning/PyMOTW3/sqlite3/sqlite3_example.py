#!/usr/bin/env python3

import csv
import os
import sqlite3

DB_FILENAME = 'example.db'
CSV_FILENAME = 'tasks.csv'
SCHEMA_FILENAME = 'todo_schema.sql'

def create_db():
    db_exist = os.path.exists( DB_FILENAME )
    with sqlite3.connect( DB_FILENAME ) as conn:
        if not db_exist:
            with open( SCHEMA_FILENAME, 'rt' ) as schema_file:
                schema = schema_file.read()
            conn.executescript( schema )

            insert_query = '''
            insert into project (name, description, deadline)
            values ('pymotw', 'Python Module of the Week', '2016-11-01');

            insert into task (details, status, deadline, project)
            values ('write about select', 'done', '2016-04-25', 'pymotw');

            insert into task (details, status, deadline, project)
            values ('write about random', 'waiting', '2016-08-22', 'pymotw');

            insert into task (details, status, deadline, project)
            values ('write about sqlite3', 'active', '2017-07-31', 'pymotw');
            '''
            conn.executescript( insert_query )

    # From the command line, we can do the following:
    # $ sqlite3 todo.db 'select * from task'

def query_metadata():
    # The DB-API 2.0 specification says that after execute() has been called,
    # the Cursor should set its description attribute to hold information about
    # the data that will be returned by the fetch methods. The API
    # specification say that the description value is a sequence of tuples
    # containing the column name, type, display size, internal size, precision,
    # scale, and a flag that says whether null values are accepted. Because
    # sqlite3 does not enforce type or size constraints on data inserted into a
    # database, only the column name value is filled in.
    with sqlite3.connect( DB_FILENAME ) as conn:
        cursor = conn.cursor()
        select_query = "select * from task where project = 'pymotw'"
        cursor.execute( select_query )
        print('Task table has these columns:')
        for colinfo in cursor.description:
            print( colinfo )

def retrieve_data( project_name ):
    with sqlite3.connect( DB_FILENAME ) as conn:
        # Change the row factory to use Row so that the fetch methods return
        # the Row objects instead of tuples. The benefit is that we don't have
        # to remember the order of the fields in the tuples.
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # using positional parameters in the query
        # select_query = '''
        # select id, priority, details, status, deadline from task
        # where project = ?
        # '''
        # cursor.execute( select_query, ( project_name, ) )
        # using named parameters in the query
        query = '''
        select id, priority, details, status, deadline from task
        where project = :project_name
        order by deadline, priority
        '''
        cursor.execute(query, {'project_name': project_name } )

        print( '\Content:' )
        # fetchall() retrieves all row while fetchmany( num ) retrieves as many
        # as num rows.
        for row in cursor.fetchall():
            task_id, priority, details, status, deadline = row
            # When using the default row factory where the fetch methods return tuples.
            # print( '{:2d} [{:d}] {:<25} [{:<8}] ({})'.format(
            #        task_id, priority, details, status, deadline))
            print('{:2d} [{:d}] {:<25} [{:<8}] ({})'.format(
                  row['id'], row['priority'], row['details'],
                  row['status'], row['deadline'] ) )

def update_data( id, status ):
    with sqlite3.connect( DB_FILENAME ) as conn:
        cursor = conn.cursor()
        query = "update task set status = :status where id = :id"
        cursor.execute(query, {'status': status, 'id': id})

def bulk_loading():
    query = """
    insert into task (details, priority, status, deadline, project)
    values (:details, :priority, 'active', :deadline, :project)
    """

    with open( CSV_FILENAME, 'rt' ) as csv_file:
        csv_reader = csv.DictReader( csv_file )
        with sqlite3.connect( DB_FILENAME ) as conn:
            cursor = conn.cursor()
            # To apply the same SQL instruction to a large set of data, use
            # executemany(). This is useful for loading data, since it avoids
            # looping over the inputs in Python and lets the underlying library
            # apply loop optimizations.
            cursor.executemany( query, csv_reader )

def type_detection():
    def show_deadline( conn ):
        query = 'select id, details, deadline from task'
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute( query )
        row = cursor.fetchone()
        for col in [ 'id', 'details', 'deadline' ]:
            print( '   {:<8}   {!r:<26}  {}'.format(
                   col, row[ col ], type( row[ col ] ) ) )

    print( 'Without type detection:' )
    with sqlite3.connect( DB_FILENAME ) as conn:
        show_deadline( conn )

    # Although SQLite only supports a few data types internally, sqlite3
    # includes facilities for defining custom types to allow a Python
    # application to store any type of data in a column. Conversion for types
    # beyond those supported by default is enabled in the database connection
    # using the detect_types flag. Use PARSE_DECLTYPES if the column was
    # declared using the desired type when the table was defined
    print('\nWith type detection:')
    with sqlite3.connect( DB_FILENAME,
                          detect_types=sqlite3.PARSE_DECLTYPES ) as conn:
        show_deadline( conn )

def main():
    create_db()
    query_metadata()
    retrieve_data( project_name='pymotw' )

    update_data( 2, 'done' )
    retrieve_data( project_name='pymotw' )

    bulk_loading()
    retrieve_data( project_name='pymotw' )

    type_detection()

if __name__ == '__main__':
    main()
