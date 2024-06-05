import re


def transition_quick_name(fsm_obj):
    query_name = re.sub(r'--\s*', '', fsm_obj.current_line)
    fsm_obj.current_query.name = query_name

def transition_skip_header(fsm_obj):
    pass

def transition_start_header(fsm_obj):
    pass

def transition_skip_metadata(fsm_obj):
    pass

def transition_metadata(fsm_obj):
    result = re.search(r'^@(?P<name>\w+)\s+(?P<value>.*)$', fsm_obj.current_line)
    # TODO: Handle errors
    match result.group("name").lower():
        case "name":
            fsm_obj.current_query.name = result.group("value")
        case "author":
            fsm_obj.current_query.author = result.group("value")
        case "db":
            fsm_obj.current_query.db = result.group("value")
        case None:
            pass
        case _:
            fsm_obj.current_query.extraData[result.group("name")] = result.group("value")

# def transition_metadata_repeat(fsm_obj):
#     pass

def transition_skip_description(fsm_obj):
    pass

def transition_description(fsm_obj):
    fsm_obj.current_query.description += " " + fsm_obj.current_line
    pass

# def transition_description_continue(fsm_obj):
#     pass

def transition_end_header(fsm_obj):
    pass

def transition_skip_query(fsm_obj):
    pass

def transition_query(fsm_obj):
    fsm_obj.current_query.content += "\n" + fsm_obj.current_line
    pass

# def transition_query_continue(fsm_obj):
#     pass

def transition_new_query(fsm_obj):
    fsm_obj.current_query.content += "\n" + fsm_obj.current_line
    fsm_obj.queries.append(fsm_obj.current_query)
    fsm_obj.current_query = Query()
    fsm_obj.query_count += 1

def transition_next(fsm_obj):
    pass


# Transitions
T_QUICK_NAME = transition_quick_name
T_SKIP_HEADER = transition_skip_header
T_START_HEADER = transition_start_header
T_SKIP_METADATA = transition_skip_metadata
T_METADATA = transition_metadata
# T_METADATA_REPEAT = transition_metadata_repeat
T_SKIP_DESCRIPTION = transition_skip_description
T_DESCRIPTION = transition_description
# T_DESCRIPTION_CONTINUE = transition_description_continue
T_END_HEADER = transition_end_header
T_SKIP_QUERY = transition_skip_query
T_QUERY = transition_query
# T_QUERY_CONTINUE = transition_query_continue
# T_END_QUERY = transition_end_query
T_NEW_QUERY = transition_new_query

# T__NEXT = transition_next


# States
S_NEW_QUERY = "STATE: NEW_QUERY" 
S_START_HEADER = "STATE: START_HEADER"
S_METADATA = "STATE: METADATA"
S_DESCRIPTION = "STATE: DESCRIPTION"
S_END_HEADER = "START: END_HEADER"
S_QUICK_NAME = "STATE: QUICK_NAME"
S_QUERY = "STATE: QUERY"
S_END_QUERY = "STATE: END_QUERY"


FSM_MAP = [
    # {'src':, 'dst':, 'pattern':, 'callback': },
    # ******ORDER MATTERS*****
    {
        'src': S_NEW_QUERY,
        'dst': S_QUICK_NAME,
        'pattern': '^--',
        'callback': T_QUICK_NAME
    },
    {
        'src': S_NEW_QUERY,
        'dst': S_START_HEADER,
        'pattern': '^/\*',
        'callback': T_START_HEADER
    },
    {
        'src': S_NEW_QUERY,
        'dst': S_QUERY,
        'pattern': '.*',
        'callback': T_QUERY
    },
    {
        'src': S_START_HEADER,
        'dst': S_METADATA,
        'pattern': '^@',
        'callback': T_METADATA
    },
    {
        'src': S_START_HEADER,
        'dst': S_DESCRIPTION,
        'pattern': '.*',
        'callback': T_SKIP_METADATA
    },
    {
        'src': S_METADATA,
        'dst': S_METADATA,
        'pattern': '^@',
        'callback': T_METADATA
    },
    {
        'src': S_METADATA,
        'dst': S_END_HEADER,
        'pattern': '\*/',
        'callback': T_SKIP_DESCRIPTION
    },
    {
        'src': S_METADATA,
        'dst': S_DESCRIPTION,
        'pattern': '.*',
        'callback': T_DESCRIPTION
    },
    # {
    #     # TODO: FAULT IF "*/" is found
    # },
    {
        'src': S_DESCRIPTION,
        'dst': S_END_HEADER,
        'pattern': '\*/',
        'callback': T_END_HEADER
    },
    {
        'src': S_DESCRIPTION,
        'dst': S_DESCRIPTION,
        'pattern': '.*',
        'callback': T_DESCRIPTION,
    },
    { # Doesn't work rn
        'src': S_END_HEADER,
        'dst': T_SKIP_QUERY,
        'pattern': 'EOF',
        'callback': T_SKIP_QUERY
    },
    {
        'src': S_END_HEADER,
        'dst': S_QUERY,
        'pattern': '.*',
        'callback': T_QUERY
    },
    {
        'src': S_QUICK_NAME,
        'dst': S_QUERY,
        'pattern': '.*',
        'callback': T_QUERY
    },
    {
        'src': S_QUERY,
        'dst': S_NEW_QUERY,
        'pattern': '^.*;$',
        'callback': T_NEW_QUERY
    },
    {
        'src': S_QUERY,
        'dst': S_QUERY,
        'pattern': '.*',
        'callback': T_QUERY
    },
]

for map_item in FSM_MAP:
    map_item['pattern_re_compiled'] = re.compile(map_item['pattern'])


class Query:
    def __init__(self):
        self.name = None
        self.author = None
        self.db = None
        self.extraData = {}
        self.description = ""
        self.content = ""

    def __repr__(self) -> str:
        return f"<Query: {self.__dict__}>"


class Query_Parse_FSM:
    def __init__(self, file_str: str) -> None:
        self.file_str = file_str
        self.current_state = S_NEW_QUERY
        self.query_count = 0
        self.current_query = Query()
        self.queries = []
        self.current_line = ""

    def run(self):
        for line in self.file_str.split('\n'):
            # print(f"PROGRESS == {self.current_query}")
            if not self.process_next(line.lstrip()):
                print(f"**SKIP** in {self.current_state} :: \"{line}\"")

    def process_next(self, aline):
        self.current_line = aline
        frozen_state = self.current_state
        if len(self.current_line.lstrip()) == 0:
            return False
        for transition in FSM_MAP:
            if transition['src'] == frozen_state:
                if self.iterate_re_evaluators(aline, transition):
                    return True
        return False

    def iterate_re_evaluators(self, aline, transition):
        pattern = transition['pattern_re_compiled']
        if pattern.match(aline):
            self.update_state(transition['dst'], transition['callback'])
            return True
        return False

    def update_state(self, new_state, callback):
        print(f"{self.current_state} -> {new_state} :: \"{self.current_line}\"")
        self.current_state = new_state
        callback(self)
