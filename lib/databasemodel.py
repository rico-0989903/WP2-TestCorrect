import sqlite3

class DatabaseModel():

    def __init__(self, database_file):
        self.database_file = database_file

    def query(self, sql_query):
        conn = sqlite3.connect(self.database_file)
        c = conn.cursor()
        c.execute(sql_query)
        tables = c.fetchall()
        conn.close()
        return tables

    def login(self, table_name, username, password):
        sql_query = f"SELECT * FROM {table_name}"
        table_content = self.query(sql_query)

        for login in table_content:
            if login[0] == username and login[1] == password:
                return f"Login succesfull! Welcome {username}!"
        return "Login unsuccesfull"
