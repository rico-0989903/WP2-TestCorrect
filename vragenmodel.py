import sqlite3


class VragenModel:
    def __init__(self, database_file):
        self.database_file = database_file

    def run_query(self, sql_query):
        conn = sqlite3.connect(self.database_file)
        c = conn.cursor()
        c.execute(sql_query)
        tables = c.fetchall()
        conn.close()
        return tables

    def run_update(self, sql_query):
        try:
            conn = sqlite3.connect(self.database_file)
            c = conn.cursor()
            c.execute(sql_query)
            conn.commit()
        except sqlite3.Error as error:
            print(error)
        finally:
            conn.close()
            print("Connection closed")

    def get_tables(self):
        sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
        result = self.run_query(sql_query)
        table_list = []
        for table in result:
            table_list.append(table[0])
        return table_list
    
    def get_questions(self):
        sql_query = "SELECT * FROM vragen WHERE vraag LIKE '%<br>%' OR vraag LIKE '%&nbsp;%' OR leerdoel > 7 OR auteur > 17;" 
        results = self.run_query(sql_query)
        return results 
    
    def get_typfout(self):
        sql_query = "SELECT * FROM vragen WHERE vraag LIKE '%<br>%' OR vraag LIKE '%&nbsp;%';" 
        results = self.run_query(sql_query)
        return results 
    
    def get_auteurfout(self):
        sql_query = "SELECT * FROM vragen WHERE auteur > 17;" 
        results = self.run_query(sql_query)
        return results
    
    def get_leerdoelfout(self):
        sql_query = "SELECT * FROM vragen WHERE leerdoel > 7;" 
        results = self.run_query(sql_query)
        return results 
    
    def get_auteurs(self):
        sql_query = "SELECT * FROM auteurs WHERE geboortejaar < 1940 OR medewerker = 0 OR medewerker = 1;" 
        results = self.run_query(sql_query)
        return results 

    def get_leerdoelen(self):
        sql_query = "SELECT * FROM leerdoelen;" 
        results = self.run_query(sql_query)
        return results 

    def get_details(self, id, table):
        sql_query = "SELECT * FROM " + table + " WHERE id = " + id + ";"
        print(sql_query)
        results = self.run_query(sql_query)
        return results

    def get_username(self):
        sql_query = "SELECT * FROM inlog;"
        results = self.run_query(sql_query)
        return results
    
    def set_admin(self, username, admin):
        sql_query = f'UPDATE inlog SET rights = "{admin}" WHERE gebruikersnaam = "{username}";' 
        print (sql_query)
        results = self.run_update(sql_query)
        print (results)
        return results
    
    def check_rights(self, username):
        sql_query = f'SELECT rights FROM inlog WHERE gebruikersnaam = "{username}";'
        results = self.run_query(sql_query)
        return results

    def login(self, table_name, username, password):
        sql_query = f"SELECT * FROM {table_name}"
        table_content = self.run_query(sql_query)

        for login in table_content:
            if login[0] == username and login[1] == password:
                return True
        return False
