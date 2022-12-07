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

    def get_tables(self):
        sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
        result = self.run_query(sql_query)
        table_list = []
        for table in result:
            table_list.append(table[0])
        return table_list

    def get_unconvertable_values(self, table_name, column_name, datatype):
        sql_query = "SELECT id, " + column_name + " FROM " + table_name
        results = self.run_query(sql_query)
        unconvertable_values = []
        for result in results:
            if datatype == "boolean":
                if result[1] != "0" and result[1] != "1":
                    unconvertable_values.append(result)
        return unconvertable_values
    
    def get_questions(self):
        sql_query = "SELECT * FROM vragen WHERE vraag LIKE '%<br>%' OR vraag LIKE '%&nbsp;%' OR leerdoel > 7 OR auteur > 17;" 
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
        results = self.run_query(sql_query)
        return results
