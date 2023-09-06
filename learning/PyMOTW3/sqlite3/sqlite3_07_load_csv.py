#!/usr/bin/env python3
import csv
import sqlite3
import sys

db_filename = 'todo.db'
data_filename = sys.argv[1]

SQL = """
insert into task (details, priority, status, deadline, project)
values (:details, :priority, 'active', :deadline, :project)
"""

with open(data_filename, 'rt') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        # To apply the same SQL instruction to a large set of data, use
        # executemany(). This is useful for loading data, since it avoids
        # looping over the inputs in Python and lets the underlying library
        # apply loop optimizations. This example program reads a list of tasks
        # from a comma-separated value file using the csv module and loads them
        # into the database.
        cursor.executemany(SQL, csv_reader)
