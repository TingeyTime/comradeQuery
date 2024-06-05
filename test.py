import time

from comradeQuery import process_sql_file

FILE_NAME = 'test.sql'
START_TIME = time.time()

print(f"Processing SQL file: {FILE_NAME}")
q = process_sql_file(FILE_NAME, verbose=True)
print(f"Processing SQL file took {time.time() - START_TIME: .4} seconds.")
print(q)