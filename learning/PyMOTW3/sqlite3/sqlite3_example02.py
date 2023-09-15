#!/usr/bin/env python3

import sqlite3

DB_FILENAME = 'example.db'

def show_projects( conn ):
    cursor = conn.cursor()
    query = 'select name, description from project'
    cursor.execute( query )
    for name, desc in cursor.fetchall():
        print( f'  {name}' )

with sqlite3.connect( DB_FILENAME ) as conn1:
    print('Before changes:')
    show_projects(conn1)

    try:
        # Insert in one cursor
        cursor = conn1.cursor()
        query = """
        insert into project (name, description, deadline)
        values ('virtualenvwrapper', 'Virtualenv Extensions', '2011-01-01')
        """
        cursor.execute( query )

        print('\nAfter changes in conn1:')
        show_projects( conn1 )

        # Select from another connection, without committing first
        # conn2 will not see the change made in conn1.
        print( '\nBefore commit in conn2:' )
        with sqlite3.connect( DB_FILENAME ) as conn2:
            show_projects( conn2 )

        # Pretend the processing caused an error to test rollback.
        # raise RuntimeError('simulated error')
    except Exception as err:
        # Discard the changes
        print('ERROR:', err)
        conn1.rollback()
    else:
        # Commit then select from another connection.
        # conn3 will see the change made in conn1.
        conn1.commit()

    print( '\nAfter commit in conn3:' )
    with sqlite3.connect( DB_FILENAME ) as conn3:
        show_projects( conn3 )
