import requests
from bs4 import BeautifulSoup

url = "https://comprar.gob.ar/BuscarAvanzadoPublicacion.aspx"

with requests.session() as s: 
    soup = BeautifulSoup(s.get(url).content, "html.parser")

    data = {}
    

