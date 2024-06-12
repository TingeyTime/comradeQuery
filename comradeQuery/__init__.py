from .sql_reader import SQLReader
from .sqlFileScanner import SQLFileScanner

def process_sql_file(file_path: str, verbose = False) -> list:
    reader = SQLReader(file_path=file_path)
    sql_text = reader.read_file()

    scanner = SQLFileScanner(sql_text, verbose=verbose)
    scanner.run()
    
    return scanner.queries


