from .sql_reader import SQLReader
from .FSM import Query_Parse_FSM
# from .scanner import Scanner

def process_sql_file(file_path: str, verbose = False) -> list:
    reader = SQLReader(file_path=file_path)
    sql_text = reader.read_file()

    # scanner = Scanner()
    # queries = scanner.process(sql_text)

    fsm = Query_Parse_FSM(sql_text, verbose=verbose)
    fsm.run()
    
    return fsm.queries


