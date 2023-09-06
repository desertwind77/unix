#!/usr/bin/env python3

import sqlite3

db_filename = 'todo.db'

with sqlite3.connect( db_filename ) as conn:
    cursor = conn.cursor()

    # tell the database engine what data to collect
    cursor.execute( '''
    select id, priority, details, status, deadline from task
    where project = 'pymotw'
    ''' )

    # retrieve the results. Use fetchall() to retrieve all rows. Use fetchmany( num )
    # to retrieve as many as num rows. If the table has less than num rows, all rows
    # will be returned.
    for row in cursor.fetchmany( 5 ):
        task_id, priority, details, status, deadline = row
        print( '{:2d} [{:d}] {:<25} [{:<8}] ({})'.format(
               task_id, priority, details, status, deadline ) )

    # The DB-API 2.0 specification says that after execute() has been called,
    # the Cursor should set its description attribute to hold information about
    # the data that will be returned by the fetch methods. The API
    # specification say that the description value is a sequence of tuples
    # containing the column name, type, display size, internal size, precision,
    # scale, and a flag that says whether null values are accepted. Because
    # sqlite3 does not enforce type or size constraints on data inserted into a
    # database, only the column name value is filled in.
    print( 'Task table has these columns:' )
    for colinfo in cursor.description:
        print( colinfo )
