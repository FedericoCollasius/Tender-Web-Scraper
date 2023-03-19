import re
import requests
import xlsxwriter
from datetime import  datetime, timedelta 

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
    'Accept': '*/*',
    'Accept-Language': 'es-AR,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://www.aysa.com.ar',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.aysa.com.ar/proveedores/licitaciones/Licitaciones-Obras-Expansion/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}

data = {
    'current': '1',
    'rowCount': '500',
    'searchPhrase': '',
    'FechaPublicacionDesde': '',
    'FechaPublicacionHasta': '',
    'PalabrasClave': '',
}

response = requests.post(
    'https://www.aysa.com.ar/api/licitaciones/getLicitacionesObraByFiltersPublic',
    headers=headers,
    data=data,
    verify=False
)

licitaciones = response.json()['rows']


def aysa (keywords, weeks):

    interes = []
    # We are only interested in tenders that are not older than two weeks old. We will also define the keywords we will be searching for. 
    delta = datetime.now() - timedelta(weeks=weeks)

    for l in licitaciones: 
        # At least here we have valid dates. For now... 

        # The date is given as a string in the format YYYY-MM-DDTHoursMinutesSecondsMiliseconds. This standard is a annoying so we will 
        # parse it into YYYY/MM/DD and then into a datetime object. 

        opening_date = l['FechaPublicacion']
        opening_date = datetime.strptime(opening_date, '%Y-%m-%dT%H:%M:%S.%fZ')
            
        # Check if the date is not older than delta weeks old.
        if opening_date >= delta:
            object_lower = l['Objeto'].lower()
            if any (keyword in object_lower for keyword in keywords):
                id = l['Id']
                url_licitacion = f'https://www.aysa.com.ar/proveedores/licitaciones/Licitaciones-Obras-Expansion/Detalle_de_Licitaciones_Obras?id={id}'
                interes.append((l['Objeto'], url_licitacion))


    #Create a workbook and add a worksheet to add the tenders we are interested in.
    workbook = xlsxwriter.Workbook('Aysa.xlsx') 
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})

    worksheet.write("A1", "Nombre de la licitacion", bold)
    worksheet.write("B1", "Link a la licitacion", bold)

    row = 1 
    col = 0 
    for nombre, link in interes:
        worksheet.write(row, col, nombre)
        worksheet.write_url(row, col + 1, link)
        row += 1

    workbook.close()
