"""
Author: Benedikt Fichtner
Python-Version: 3.8.10
PSE (Periodensystem) / German / CONFIG
"""
import json

class CONFIG():
    def __init__(self,filepath:str,console) -> None:
        (self.filepath,self.console) = (filepath,console)
    
    def get(self,*args:list):
        data = None
        with open(self.filepath,'r') as json_file_data:
            try:
                data = json.load(json_file_data)
                for arg in args: data = data[arg]
            except Exception as error:
                self.console.log(f"[red]An error occured while reading '{self.filepath}':[bold red] {str(error)}")
        return data