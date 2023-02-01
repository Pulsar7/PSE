"""
Author: Benedikt Fichtner
Python-Version: 3.8.10
PSE (Periodensystem) / German
"""
import sys,os,argparse,json
from rich import (pretty,console as cons)
from tkinter import *
import customtkinter


class CONFIG():
    def __init__(self) -> None:
        pass
    
    def get(self,args:list,filepath:str):
        data = None
        with open(filepath,'r') as json_file_data:
            try:
                data = json.load(json_file_data)
                for arg in args: data = data[arg]
            except Exception as error:
                self.console.log(f"[red]An error occured while reading '{filepath}':[bold red] {str(error)}")
        return data
    
    def get_gui(self,*args):
        return self.get(args = args, filepath = self.gui_conf_filepath)
    
    def get_pse(self,*args):
        return self.get(args = args, filepath = self.pse_conf_filepath)
    

class GUI(CONFIG):
    def __init__(self,console,gui_conf_filepath:str,pse_conf_filepath:str) -> None:
        (self.console,self.gui_conf_filepath,self.pse_conf_filepath) = (console,gui_conf_filepath,
            pse_conf_filepath)
        super().__init__()
        
    def show_info_to_element(self,element:str) -> None:
        info_window = customtkinter.CTkToplevel(self.root)
        info_window.title(self.get_gui("Content","Info","title")%(element))
        info_window.resizable(False, False)
        element_data:dict = self.get_pse("Elements",element)
        tabview = customtkinter.CTkTabview(info_window)
        tabview.add("Basisinformationen")
        tabview.set("Basisinformationen") 
        tabview.pack(padx=20, pady=20)
        
        # Basis-Infos
        customtkinter.CTkLabel(tabview.tab("Basisinformationen"),
            text="Name: %s\nOrdnungszahl: %s\nAggregatzustand: %s\nMasse u: %s"%(
                element_data['name'],element_data['ordnungszahl'],
                element_data['aggregatzustand'],element_data['masse_u']), font = ("Serif",15)).pack(
            side = TOP
        )
        #
        # data_frame = customtkinter.CTkFrame(info_window)
        # data_frame.pack(side=TOP,fill=BOTH,pady=30,padx=30,expand=True)
        
    def show_legend(self) -> None:
        legend_window = customtkinter.CTkToplevel(self.root)
        legend_window.title(self.get_gui("Content","Legend","title"))
        legend_window.resizable(False, False)
        element_series:dict = self.get_pse("element_series")
        aggregate_states:dict = self.get_pse("aggregate_states")
        
        # Serien
        series_frame = customtkinter.CTkFrame(legend_window)
        series_frame.pack(side=TOP,fill=BOTH,pady=30,padx=30,expand=True)
        for serie in element_series:
            customtkinter.CTkLabel(series_frame,text=f"{serie}",
                bg_color=element_series[serie]['bg']).pack(side=TOP,fill=X,ipady=3)
        
        # Aggregatzustände
        aggregate_frame = customtkinter.CTkFrame(legend_window)
        aggregate_frame.pack(side=BOTTOM,fill=BOTH,pady=30,padx=30,expand=True)
        for aggr in aggregate_states:
            customtkinter.CTkLabel(aggregate_frame,text=f"{aggr}",
                text_color=aggregate_states[aggr]['fg']).pack(side=TOP,fill=X,ipady=3)
        
    def run(self) -> None:
        customtkinter.set_appearance_mode(self.get_gui("Style","Main","appearance_mode"))
        customtkinter.set_default_color_theme(self.get_gui("Style","Main","default_color_theme"))
        self.root = customtkinter.CTk()
        self.root.title(self.get_gui("Content","Main","title"))
        self.root.minsize(self.get_gui("Style","Main","min_width"),self.get_gui("Style","Main","min_height"))
        self.root.resizable(False, False)
        x:int = 65
        pse_main_frame = customtkinter.CTkFrame(self.root)
        pse_main_frame.pack(side=TOP,fill=BOTH,pady=30,padx=30,expand=True)
        # Gruppen
        for i in range(1,19):
            customtkinter.CTkLabel(pse_main_frame,text=f"{i}").place(x = x, y = 0)
            x += 77
        # Perioden
        y:int = 50
        for i in range(1,8):
            customtkinter.CTkLabel(pse_main_frame,text=f"   {i}").place(x = 0, y = y)
            y += 66
        pse_frame = customtkinter.CTkFrame(pse_main_frame, bg_color = "transparent")
        pse_frame.pack(side=TOP,pady=30,padx=30,fill=BOTH,expand=True)
        # Element informations
        elements:dict = self.get_pse("Elements")
        element_series:dict = self.get_pse("element_series")
        aggregate_states:dict = self.get_pse("aggregate_states")
        #
        (x,y) = (0,0)
        element_counter:int = 0
        for element in elements:
            if elements[element] != 0:
                if elements[element]['ordnungszahl'] == 57:
                    x += 77*2
                    y += 65
                if elements[element]['ordnungszahl'] == 89:
                    x += 77*2
                if elements[element]['ordnungszahl'] == 71:
                    element_counter = 17
                if elements[element]['ordnungszahl'] == 103:
                    element_counter = 17
                Button(pse_frame, width = 6, bg = element_series[elements[element]['typ']]['bg'], relief = FLAT,
                    activebackground=element_series[elements[element]['typ']]['active_bg'], highlightthickness=0,
                    fg = aggregate_states[elements[element]['aggregatzustand']]['fg'],
                    text = f"{elements[element]['ordnungszahl']}\n    {element}\n{elements[element]['masse_u']}",
                    command = lambda element=element:self.show_info_to_element(element)).place(
                        x = x, y = y
                    )
            element_counter += 1
            x += 77
            if element_counter == 18:    
                x = 0
                element_counter = 0
                y += 65
        
        customtkinter.CTkButton(pse_frame,text="Legende zeigen",command=self.show_legend).pack(side=BOTTOM,pady=10)
        self.show_legend()
        
        self.root.mainloop()
    
#
pretty.install()
console = cons.Console()
#
default_pse_conf_filepath:str = 'src/pse.json'
default_gui_conf_filepath:str = 'src/gui_conf.json'
#
parser = argparse.ArgumentParser("python3 pse.py")
parser.add_argument('-g','--gui_config', help=f"GUI-Config-filepath (default = '{default_gui_conf_filepath}'",
    default = default_gui_conf_filepath, type = str
)
parser.add_argument('-p','--pse_config', help=f"PSE-Config-filepath (default = '{default_pse_conf_filepath}'",
    default = default_pse_conf_filepath, type = str
)
args = parser.parse_args()

if ".json" not in args.gui_config or ".json" not in args.pse_config:
    console.log(f"[red]Invalid arguments!")
    parser.print_help()
    sys.exit()
#

if __name__ == '__main__':
    # os.system("clear") # 
    gui = GUI(console = console, gui_conf_filepath = args.gui_config,
        pse_conf_filepath = args.pse_config          
    )
    gui.run()