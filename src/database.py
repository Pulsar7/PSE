"""
Author: Benedikt Fichtner
Python-Version: 3.8.10
PSE (Periodensystem) / German / DATABASE
"""
import sqlite3,sys
from contextlib import closing

class DATABASE():
    def __init__(self,conf,console) -> None:
        (self.conf,self.console) = (conf,console)
        (self.db_path,self.elements_table_name,self.element_infos_table_name) = (conf.get("Database","db_path"),
            conf.get("Database","tables","elements","name"),conf.get("Database","tables","element-infos","name")                                  
        )
        
        
    ### GET
    
    def get_one_element(self,ordnungszahl:int) -> list[str] or bool:
        try:
            with closing(sqlite3.connect(self.db_path)) as connection:
                with closing(connection.cursor()) as cursor:
                    cursor.execute(f"SELECT * FROM {self.elements_table_name} WHERE ordnungszahl = ?;",(
                        ordnungszahl,
                    ))
                    rows = cursor.fetchall()
                    connection.commit()
            if len(rows) > 0:
                rows = rows[0]
            return [row for row in rows]
        except Exception as error:
            self.console.log(f"[red]Couldn't get element '{ordnungszahl}':[bold red] {str(error)}")
            return False
    
    def get_all_elements(self) -> list[list] or bool:
        try:
            elements:list[list] = []
            with closing(sqlite3.connect(self.db_path)) as connection:
                with closing(connection.cursor()) as cursor:
                    cursor.execute(f"SELECT * FROM {self.elements_table_name}")
                    data_rows = cursor.fetchall()
                    connection.commit()
            elements = [element for element in data_rows]
            return elements
        except Exception as error:
            self.console.log(f"[red]Couldn't get all pse-elements from '{self.db_path}':[bold red] {str(error)}")
            return False
    
    def get_element_infos(self,ordnungszahl:int) -> list[list] or bool:
        try:
            element_infos:list[list] = []
            with closing(sqlite3.connect(self.db_path)) as connection:
                with closing(connection.cursor()) as cursor:
                    cursor.execute(f"SELECT * FROM {self.element_infos_table_name} WHERE ordnungszahl = ?;",(
                        ordnungszahl,
                    ))
                    data_rows = cursor.fetchall()
                    connection.commit()
            element_infos = [element for element in data_rows[0]]
            return element_infos
        except Exception as error:
            self.console.log(f"[red]Couldn't get element-infos for element '{ordnungszahl}' from {self.db_path}:[bold red] {str(error)}")
            return False
        
    ### ADD / CREATE
    
    def create_tables(self) -> bool:
        try:
            tables:list[str] = list(self.conf.get("Database","tables").keys())
            with closing(sqlite3.connect(self.db_path)) as connection:
                with closing(connection.cursor()) as cursor:
                    for table in tables:
                        table_name:str = self.conf.get("Database","tables",table,"name")
                        values:list[str] = self.conf.get("Database","tables",table,"values")
                        values = ",".join(values)
                        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({values})")
                        connection.commit()
            self.console.log(f"[green]Created all tables")
            return True
        except Exception as error:
            self.console.log(f"[red]Couldn't create all tables:[bold red] {str(error)}")
            return False
    
    def add_element(self,element_data:dict) -> bool:
        try:
            values:list[str] = self.conf.get("Database","tables","elements","values")
            for value in values:
                value:str = value.split(" ")[0]
                if value not in list(element_data.keys()):
                    raise Exception(f"Invalid arguments! Value '{value}' is missing!")
            ordnungszahl:str = element_data['ordnungszahl']
            rows = self.get_one_element(ordnungszahl = ordnungszahl)
            if isinstance(rows,bool):
                raise Exception("Database error")
            if len(rows) == 0:
                with closing(sqlite3.connect(self.db_path)) as connection:
                    with closing(connection.cursor()) as cursor:
                        table_values:list[str] = self.conf.get("Database","tables","elements","values")
                        table_values = [e.split(" ")[0] for e in table_values]
                        table_values:str = ",".join(table_values)
                        cursor.execute(f"INSERT INTO {self.elements_table_name}({table_values}) VALUES(?,?,?,?,?,?)",
                            (ordnungszahl, element_data['symbol'], element_data['name'], element_data['masse_u'],
                            element_data['aggregatzustand'],element_data['serie'])
                        )
                        table_values:list[str] = self.conf.get("Database","tables","element-infos","values")
                        table_values = [e.split(" ")[0] for e in table_values]
                        table_values:str = ",".join(table_values)
                        cursor.execute(f"INSERT INTO {self.element_infos_table_name}({table_values}) VALUES(?,?,?,?)",
                            (ordnungszahl, element_data['entdeckung'], element_data['vorkommen'],
                            element_data['nebeninfos'])
                        )
                        connection.commit()
                self.console.log(f"[green]Created element '{ordnungszahl}'")
                return True
            else:
                raise Exception(f"The element '{ordnungszahl}' already exists!")
        except Exception as error:
            self.console.log(f"[red]Couldn't add an element:[bold red] {str(error)}")
            return False
        
    ### DELETE
    
    def delete_element(self,ordnungszahl:int) -> bool:
        try:
            rows = self.get_one_element(ordnungszahl = ordnungszahl)
            if isinstance(rows,bool):
                raise Exception("Database error")
            if len(rows) > 0:
                with closing(sqlite3.connect(self.db_path)) as connection:
                    with closing(connection.cursor()) as cursor:
                        cursor.execute(f"DELETE FROM {self.elements_table_name} WHERE 'ordnungszahl' = ?", (
                            ordnungszahl
                        ))
                        cursor.execute(f"DELETE FROM {self.element_infos_table_name} WHERE 'ordnungszahl' = ?",(
                            ordnungszahl
                        ))
                        connection.commit()
                self.console.log(f"[green]Deleted element '{ordnungszahl}'")
                return True
            else:
                raise Exception(f"The element '{ordnungszahl}' does not exist!")
        except Exception as error:
            self.console.log(f"[red]Couldn't add an element:[bold red] {str(error)}")
            return False