from abc import ABC


class BaseSQLTool(ABC):

    def __init__(self):
        raise NotImplemented

    def __call__(self, *args, **kwds):
        raise NotImplemented

    def __repr__(self):
        return f"""
            Tool Name:  {self.name}
            Tool Desc:  {self.desc}
            Init Variables: {self.init_variables}
            Input Variables: {self.input_variables}
            Response Variables: {self.response_variables}
        """

    def _validate_query(self, query: str):
        raise NotImplemented

    def fetch_metadata(self, tables: list = []):
        raise NotImplemented
