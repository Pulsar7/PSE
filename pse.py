"""
Author: Benedikt Fichtner
Python-Version: 3.8.10
PSE (Periodensystem) / German
"""
import sys,os,argparse
sys.dont_write_bytecode = True
from rich import (pretty,console as cons)
from tkinter import *
import customtkinter
from src import (config,database)

class GUI():
    def __init__(self,console,conf,db) -> None:
        (self.console,self.conf,self.db) = (console,conf,db)
        
    def show_info_of_element(self,ordnungszahl:int) -> None:
        info_window = customtkinter.CTkToplevel(self.root)
        element_data = self.db.get_one_element(ordnungszahl = ordnungszahl)
        if isinstance(element_data,bool):
            self.root.destroy()
            sys.exit()
        ### Element data
        element_name:str = element_data[2]
        element_symbol:str = element_data[1]
        ###
        info_window.title(self.conf.get("Content","Info","title")%(element_symbol))
        info_window.minsize(self.conf.get("Style","Info","min_width"),self.conf.get("Style","Info","min_height"))
        # info_window.resizable(False, False)
        label_font:list[str] = self.conf.get("Style","Info","title_element","font")
        customtkinter.CTkLabel(info_window,text=f"{element_name} ({element_symbol})",
            font = (label_font[0],label_font[1])).pack(
            side=TOP, fill=X, ipady = 3
        )
        tabview = customtkinter.CTkTabview(info_window)
        tabs:dict = self.conf.get("Content","Info","tabview","tabs")
        for tab in tabs:
            tabview.add(tab)
        tab_keys:list[str] = list(tabs.keys())
        tabview.set(tab_keys[0])
        tabview.pack(padx=50, pady=20, fill = BOTH, expand=True)
        
        # Basis-Infos
        textbox_style:dict = self.conf.get("Style","Info","tabview","tabs",tab_keys[0],"textbox")
        basis_infos_textbox = customtkinter.CTkTextbox(tabview.tab(tab_keys[0]), border_spacing=3,
            border_color = textbox_style['border_color'],
            font = (textbox_style['font'][0],textbox_style['font'][1]), border_width = 0
        )
        basis_infos_textbox.insert(END,"Name: %s\nOrdnungszahl: %s\nAggregatzustand: %s\nMasse u: %s\nSerie: %s"%(
            element_name,element_data[0],
            element_data[4],element_data[3],element_data[5])
        )
        basis_infos_textbox.pack(side=TOP,fill=BOTH,expand=True,padx=10,pady=10)
        basis_infos_textbox.configure(state=DISABLED)
        element_data.clear()
        # Vorkommen & Entdeckung
        element_data = self.db.get_element_infos(ordnungszahl = ordnungszahl)
        textbox_style:dict = self.conf.get("Style","Info","tabview","tabs",tab_keys[1],"textbox")
        vor_entd_textbox = customtkinter.CTkTextbox(tabview.tab(tab_keys[1]), border_spacing=3,
            border_color = textbox_style['border_color'],
            font = (textbox_style['font'][0],textbox_style['font'][1]), border_width = 0
        )
        vor_entd_textbox.insert(END,"%s\n%s"%(element_data[2],element_data[1]))
        vor_entd_textbox.pack(side=TOP,fill=BOTH,expand=True,padx=10,pady=10)
        vor_entd_textbox.configure(state=DISABLED)
        # Nebeninfos
        textbox_style:dict = self.conf.get("Style","Info","tabview","tabs",tab_keys[1],"textbox")
        nebeninfos_textbox = customtkinter.CTkTextbox(tabview.tab(tab_keys[2]), border_spacing=3,
            border_color = textbox_style['border_color'],
            font = (textbox_style['font'][0],textbox_style['font'][1]), border_width = 0
        )
        nebeninfos_textbox.insert(END,"%s"%(element_data[3]))
        nebeninfos_textbox.pack(side=TOP,fill=BOTH,expand=True,padx=10,pady=10)
        nebeninfos_textbox.configure(state=DISABLED)
        element_data.clear()
        
    def show_legend(self) -> None:
        legend_window = customtkinter.CTkToplevel(self.root)
        legend_window.title(self.conf.get("Content","Legend","title"))
        legend_window.resizable(False, False)
        element_series:dict = self.conf.get("PSE","element_series")
        aggregate_states:dict = self.conf.get("PSE","aggregate_states")
        
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
        customtkinter.set_appearance_mode(self.conf.get("Style","Main","appearance_mode"))
        customtkinter.set_default_color_theme(self.conf.get("Style","Main","default_color_theme"))
        self.root = customtkinter.CTk()
        self.root.title(self.conf.get("Content","Main","title"))
        self.root.minsize(self.conf.get("Style","Main","min_width"),self.conf.get("Style","Main","min_height"))
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
        all_elements = self.db.get_all_elements()
        if isinstance(all_elements,bool):
            self.root.destroy()
            sys.exit()
        element_series:dict = self.conf.get("PSE","element_series")
        aggregate_states:dict = self.conf.get("PSE","aggregate_states")
        #
        (x,y) = (0,0)
        element_counter:int = 0
        for element in all_elements:
            if element[1] != "0":
                if element[0] == 57:
                    x += 77*2
                    y += 65
                if element[0] == 89:
                    x += 77*2
                if element[0] == 71:
                    element_counter = 17
                if element[0] == 103:
                    element_counter = 17
                
                Button(pse_frame, width = 6, bg = element_series[element[5]]['bg'], relief = FLAT,
                    activebackground=element_series[element[5]]['active_bg'], highlightthickness=0,
                    fg = aggregate_states[element[4]]['fg'],
                    text = f"{element[0]}\n    {element[1]}\n{element[3]}",
                    command = lambda element=element:self.show_info_of_element(
                        ordnungszahl = element[0])).place(
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
default_conf_filepath:str = 'src/conf/config.json'
#
parser = argparse.ArgumentParser("python3 pse.py")
parser.add_argument('-c','--config', help=f"Config-filepath (default = '{default_conf_filepath}'",
    default = default_conf_filepath, type = str
)
args = parser.parse_args()

if ".json" not in args.config:
    console.log(f"[red]Invalid arguments!")
    parser.print_help()
    sys.exit()
    
conf = config.CONFIG(filepath = args.config, console = console)
db = database.DATABASE(conf = conf, console = console)
#

if __name__ == '__main__':
    os.system("clear") # 
    gui = GUI(console = console, conf = conf, db = db)
    gui.run()