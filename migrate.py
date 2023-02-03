"""
Not permanent part of this project
"""
import os,sys,sqlite3,json,requests
sys.dont_write_bytecode = True
from src import (config,database)
from rich import (pretty,console as cons)
from bs4 import BeautifulSoup


def get_from_json(filepath:str):
    with open(filepath,'r') as json_data:
        data = json.load(json_data)
    return data

def get_element_infos(element_name:str) -> dict:
    element_infos:dict = {
        "entdeckung": "",
        "vorkommen": "",
        "nebeninfos": f"Quelle: {element_infos_url}"
    }
    resp = requests.get(element_infos_url+element_name.lower(),headers = headers)
    soup = BeautifulSoup(resp.text, 'html')
    # Entdecker, Entdeckungsjahr & Vorkommen
    for daten in soup.findAll("table",{"class":"daten"}):
        for tr in daten.find_all('tr'):
            if "</td>" in str(tr) and "<td>" in str(tr):
                el:str = f"{str(tr).split('<td>')[1].split('</td>')[0]}"
                if "Entdecker" in str(tr):
                    element_infos['entdeckung'] += f"Entdecker: {el}\n"
                if "Entdeckungsjahr" in str(tr):
                    element_infos['entdeckung'] += f"Entdeckungsjahr: {el}\n"
                if "Vorkommen" in str(tr):
                    element_infos['vorkommen'] += f"Vorkommen: {el}\n"
    if len(element_infos['vorkommen']) == 0:
        element_infos['vorkommen'] = "Vorkommen: Unbekannt"
    if len(element_infos['entdeckung']) == 0:
        element_infos['entdeckung'] = "Entdecker & Entdeckungsjahr: Unbekannt"
    #
    return element_infos

def main(json_filepath:str) -> None:
    empty_element_values:list = conf.get("Database","tables","elements","empty_element_values")
    data = get_from_json(filepath = json_filepath)
    zero_counter:int = 0
    for element_symbol in data:
        with console.status(f"[yellow]Creating element '{element_symbol}'..."):
            if data[element_symbol] == 0:
                zero_counter += 1
                empty_element_values['ordnungszahl'] += 118+zero_counter
                state = db.add_element(element_data = empty_element_values)
            else:
                element_infos:dict = get_element_infos(data[element_symbol]['name'])
                element_data:dict = {
                    "ordnungszahl": data[element_symbol]['ordnungszahl'],
                    "entdeckung": element_infos['entdeckung'],
                    "vorkommen": element_infos['vorkommen'],
                    "nebeninfos": element_infos['nebeninfos'],
                    "symbol": element_symbol,
                    "name": data[element_symbol]['name'],
                    "masse_u": data[element_symbol]['masse_u'],
                    "aggregatzustand": data[element_symbol]['aggregatzustand'],
                    "serie": data[element_symbol]['typ']
                }
                state = db.add_element(element_data = element_data)
            if state == False:
                break
    

#
pretty.install()
console = cons.Console()
#
conf = config.CONFIG(filepath = 'src/conf/config.json', console = console)
db = database.DATABASE(conf = conf, console = console)
state:bool = db.create_tables()
if state == False:
    sys.exit()
element_infos_url:str = "https://www.periodensystem.info/elemente/"
headers:list[str] = []
#

if __name__ == '__main__':
    # os.system("clear") # 
    main(json_filepath = 'data.json')