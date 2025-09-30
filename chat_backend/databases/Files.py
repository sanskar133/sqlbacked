from database_connection_management.databases.base import Database, DatabaseFields


class Files(Database):
    display_name: str = "Files"
    description: str = "Upload Your Excel, CSV File"

    @property
    def field_config(self):
        config = []
