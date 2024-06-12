class Query:
    def __init__(self):
        self.name = None
        self.author = None
        self.db = None
        self.description = ""
        self.extra = {}
        self.content = ""

    def __repr__(self) -> str:
        return f"<Query: {self.__dict__}>"
