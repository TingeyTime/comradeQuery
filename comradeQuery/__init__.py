from .sql_reader import SQLReader
# from .scanner import Scanner

def process_sql_file(file_path: str) -> list:
    reader = SQLReader(file_path=file_path)
    sql_text = SQLReader.read_file()

    scanner = Scanner()
    queries = scanner.process(sql_text)

    
