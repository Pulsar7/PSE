"""
Author: Benedikt Fichtner
Python-Version: 3.8.10
PSE (Periodensystem) / German
"""
import sys,os,argparse,json
from tkinter import *
from rich import (pretty,console as cons)

class CONFIG():
    def __init__(self) -> None:
        pass
    
    def get(self,*args:list):
        data = None
        with open(self.conf_filepath,'r') as json_file_data:
            data = json.load(json_file_data)
            for arg in args: data = data[arg]
        return data

class GUI(CONFIG):
    def __init__(self,conf_filepath:str,console) -> None:
        (self.conf_filepath,self.console) = (conf_filepath,console)
        super().__init__()
        
    def open_info_window(self,element:str) -> None:
        info_window = Toplevel(self.root)
        element_infos = self.get("Content","PSE","elements",element)
        info_window.configure(bg = self.get("Style","Info","bg"))
        title:str = self.get("Content","Info","title")%(element_infos['name'],element)
        info_window.title(title)
        info_window.maxsize(self.get("Style","Info","width"),self.get("Style","Info","height"))
        info_window.minsize(self.get("Style","Info","width"),self.get("Style","Info","height"))
        Label(info_window,text=title,anchor=CENTER,bg = self.get("Style","Info","title","bg"),
            font = self.get("Style","Info","title","font")
        ).pack(side=TOP,fill=X,ipady=5)
        # Typ
        Label(info_window,text=f"Typ = {element_infos['typ']}",
            anchor = W, bg = self.get("Style","Info","bg"),
            font = self.get("Style","Info","information","font")
        ).pack(side=TOP,fill=X,padx=20)
        # Ordnungszahl
        Label(info_window,text=f"Ordnungszahl = {element_infos['ordnungszahl']}",
            anchor = W, bg = self.get("Style","Info","bg"),
            font = self.get("Style","Info","information","font")
        ).pack(side=TOP,fill=X,padx=20)
        # Masse u
        Label(info_window,text=f"Masse (u) = {element_infos['masse_u']}",
            anchor = W, bg = self.get("Style","Info","bg"),
            font = self.get("Style","Info","information","font")
        ).pack(side=TOP,fill=X,padx=20)
        # Aggregatzustand
        Label(info_window,text=f"Aggregatzustand = {element_infos['aggregatzustand']}",
            anchor = W, bg = self.get("Style","Info","bg"),
            font = self.get("Style","Info","information","font")
        ).pack(side=TOP,fill=X,padx=20)
        #
    
    def run(self) -> None:
        self.root = Tk()
        self.root.configure(bg = self.get("Style","Main","bg"))
        self.root.title(self.get("Content","Main","title"))
        self.root.minsize(self.get("Style","Main","min_width"),self.get("Style","Main","min_height"))
        self.root.maxsize(self.get("Style","Main","min_width"),self.get("Style","Main","min_height"))
        self.root.columnconfigure(19, weight=1)
        self.root.rowconfigure(8,weight=1)
        
        elements = self.get("Content","PSE","elements")
        types = self.get("Style","PSE","element_types")
        aggregate_state = self.get("Style","PSE","aggregate_states")
        for element in elements:
            Button(self.root, width = 6, bg = types[elements[element]['typ']]['bg'], relief = FLAT,
                activebackground=types[elements[element]['typ']]['active_bg'],
                fg = aggregate_state[elements[element]['aggregatzustand']]['fg'], highlightthickness = 0,
                text=f"{elements[element]['ordnungszahl']}\n    {element}\n{elements[element]['masse_u']}",
                command = lambda element=element:self.open_info_window(element)).grid(
                    column = elements[element]['column'],row = elements[element]['row'], 
                    sticky = W, ipady = 0, pady = 0, padx = 0)
        
        self.root.mainloop()
        
        
#
pretty.install()
console = cons.Console()

default_config_filepath:str = 'config.json'
#
parser = argparse.ArgumentParser("python3 pse.py")
parser.add_argument('-c','--config', help=f"Config-filepath (default = '{default_config_filepath}'",
    default = default_config_filepath, type = str                   
)
args = parser.parse_args()
#

if __name__ == '__main__':
    os.system("clear") # 
    gui = GUI(console = console, conf_filepath = args.config)
    gui.run()