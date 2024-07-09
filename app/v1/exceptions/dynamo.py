class DynamoTableDoesNotExist(Exception):
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.message = f"Tabella {table_name} non trovata"
        super().__init__(self.message)


class DynamoTableAlreadyExists(Exception):
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.message = f"Tabella {table_name} già esistente"
        super().__init__(self.message)


class UserNotFound(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.message = f"Utente con ID {user_id} non trovato"
        super().__init__(self.message)


class EmptyTable(Exception):
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.message = f"Tabella {table_name} vuota"
        super().__init__(self.message)
